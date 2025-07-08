import os
import io
import base64
import datetime
import torch
import open_clip
import re
import time
import json
import requests
import torch.nn.functional as F
import traceback
traceback.print_exc()
from PIL import Image
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from werkzeug.utils import secure_filename
from concurrent.futures import ThreadPoolExecutor
from models.image import Image
from models.search_history import SearchHistory
from models.text import Text
from config import db_init as db
from open_clip import create_model_and_transforms
from ITR.model.Loss import Loss
from openai import OpenAI
from datetime import datetime  
from urllib.parse import urlparse
from PIL import Image as PILImage




# 设置图片上传文件夹路径，并确保文件夹存在
UPLOAD_FOLDER = 'D:\\code\\RetrievalSystemBackend\\pictures'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # 如果文件夹不存在则创建

# 检查GPU是否可用，并将设备设置为GPU，否则使用CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model_path = "ITR\open_clip\open_clip_pytorch_model.bin"

# 加载预训练的 openclip 模型
model, _, preprocess = create_model_and_transforms('ViT-B-32')

# 加载本地预训练权重
checkpoint = torch.load(model_path, map_location=device,weights_only=True)

# 加载权重到模型
model.load_state_dict(checkpoint)

# 设置模型到设备并设为评估模式
model = model.to(device)
model.eval()

# 读取 output.pt 文件
data = torch.load("ITR\dataset\output.pt", map_location=device,weights_only=True)

# 从 data 中提取出 image_tensor 和 text_tensor
image_list = data["images"]  # 假设这是一个 list，其中每个元素是 shape 为 [1, 512] 的张量
text_list = data["texts"]    # 假设这是一个 list，其中每个元素是 shape 为 [1, 512] 的张量
image_list_filtered = [image_list[i] for i in range(0, len(image_list), 5)]

# 将 image_list 和 text_list 转换为张量
image_tensor = torch.stack(image_list_filtered).squeeze(1)  # 将形状从 [N, 1, 512] 转换为 [N, 512]
text_tensor = torch.stack(text_list).squeeze(1)    # 将形状从 [N, 1, 512] 转换为 [N, 512]

# 确保张量在正确的设备上
image_tensor = image_tensor.to(device)
text_tensor = text_tensor.to(device)

# 定义数据文件路径
captions_file = 'ITR\dataset\captions.txt'
image_paths = []
text_descs = []

# 使用 torch.no_grad() 以节省内存
with torch.no_grad():
    with open(captions_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()[1:]  # 跳过标题行
        for line in lines:
            # 使用第一个逗号分隔图像路径和文本
            image_path, text = line.strip().split(',', 1)
            image_path = "ITR/dataset/images/" + image_path.strip()
            image_paths.append(image_path)
            text_descs.append(text)

# 加载Loss模型
loss_model = Loss()
# 加载模型权重并调整到当前设备
checkpoint = torch.load("saved_models\Best_model.pth", map_location=device,weights_only=True)
loss_model.load_state_dict(checkpoint)
# 提取image_text_cross_attention子模型
model_a = loss_model.image_text_cross_attention.to(device)
model_a.eval()

API_KEY = os.getenv('ALIYUN_API_KEY', 'sk-47dac4749e0b4ef3bfc92b77ff0cb3a8')

def get_top_k_similar_images_fast(text_input, image_tensor, top_k=3):
    # 将文本输入转换为张量
    with torch.no_grad():
        text_features = model.encode_text(open_clip.tokenize([text_input]).to(device))

    # 对图像特征和文本特征进行 L2 正则化
    text_features = F.normalize(text_features, dim=-1)
    image_tensor = F.normalize(image_tensor, dim=-1)

    # 计算相似度
    similarities = torch.matmul(image_tensor, text_features.T).squeeze(1)

    # 获取相似度最高的 top_k 个图像索引
    top_k_indices = similarities.topk(top_k).indices

    return top_k_indices, similarities[top_k_indices]

def get_top_k_similar_image_slow(top_k_indices, image_paths, user_input, previous_confidence, top_k=1):
    
    # 五个相同图片处理一次
    top_k_image_paths = [image_paths[i * 5] for i in top_k_indices]

    user_input = [user_input] * len(top_k_indices)

    res = model_a(user_input, top_k_image_paths) + previous_confidence

    # 找到相似度的最大的 top_k 个元素的下标
    _, top_k_res_indices = torch.topk(res, top_k)

    # 使用这些下标查询 top_k_indices 以获得最终的结果
    final_top_k_indices = [top_k_indices[i] for i in top_k_res_indices]

    # 这里只使用flickr8k
    final_top_k_results = [image_paths[i * 5] for i in final_top_k_indices]
    
    return final_top_k_results,res


def ali_generate_image_http(prompt):
    """
    使用 HTTP 请求调用阿里通义万象 API 生成图片
    
    参数:
        prompt (str): 图片生成提示词
        
    返回:
        dict: 包含图片 URL 和状态信息的字典
    """
    # API 端点
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"
    
    # 请求头
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable"  # 启用异步模式，避免超时
    }
    
    # 请求体
    payload = {
        "model": "wanx-v1",  # 使用万相模型
        "input": {
            "prompt": prompt
        },
        "parameters": {
            "size": "1024*1024",  # 图片尺寸
            "n": 1,               # 生成数量
        }
    }
    
    try:
        # 发送 POST 请求
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # 检查 HTTP 错误
        
        # 解析响应
        result = response.json()
        
        # 检查 API 错误
        if result.get('code') is not None:
            return {
                "success": False,
                "error": f"API Error: {result.get('message', 'Unknown error')}",
                "code": result.get('code')
            }
        
        # 获取任务 ID
        task_id = result.get('output', {}).get('task_id')
        if not task_id:
            return {
                "success": False,
                "error": "No task ID in response",
                "response": result
            }
        
        # 查询任务结果
        return get_task_result(task_id)
    
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"HTTP request failed: {str(e)}"
        }
    except json.JSONDecodeError:
        return {
            "success": False,
            "error": "Invalid JSON response",
            "response_text": response.text
        }

def get_task_result(task_id, max_retries=20, delay=2):
    """
    查询异步任务结果
    
    参数:
        task_id (str): 任务 ID
        max_retries (int): 最大重试次数
        delay (int): 重试间隔(秒)
        
    返回:
        dict: 任务结果
    """
    url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            result = response.json()
            
            # 检查任务状态
            task_status = result.get('output', {}).get('task_status')
            message=result.get('output', {}).get('message')
            
            if task_status == 'SUCCEEDED':
                # 获取图片 URL
                image_url = result.get('output', {}).get('results', [{}])[0].get('url')
                if image_url:
                    return {
                        "success": True,
                        "image_url": image_url
                    }
                else:
                    return {
                        "success": False,
                        "error": "No image URL in response",
                        "response": result
                    }
            
            elif task_status in ['PENDING', 'RUNNING']:
                # 任务仍在处理中，等待后重试
                time.sleep(delay)
                continue
            
            else:  # FAILED 或其他状态
                print(message)
                return {
                    "success": False,
                    "error": f"Task failed with status: {task_status}",
                    "response": result
                }
                
                
        except requests.exceptions.RequestException as e:
            # 网络错误，稍后重试
            time.sleep(delay)
            continue
    
    # 超过最大重试次数
    return {
        "success": False,
        "error": f"Task not completed after {max_retries} retries"
    }

def download_image(image_url):
    """下载图片并返回二进制数据"""
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"下载图片失败: {str(e)}")
        return None

def image_to_base64(image_data):
    """将图片二进制数据转换为Base64字符串"""
    if image_data:
        return base64.b64encode(image_data).decode('utf-8')
    return None
    

def read_and_encode_image(image_path):
    """
    读取图片文件并进行 Base64 编码

    参数:
        image_path (str): 图片文件路径

    返回:
        str: 图片的 Base64 编码字符串，如果读取失败则返回 None
    """
    try:
        with open(image_path, 'rb') as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
            return img_base64
    except Exception as e:
        return None

#服务函数
def text_search(keywords,choice_generate=0):
    """
    根据关键词执行文本检索,相似度低时调用API生成图片
    
    参数:
        keywords (str): 检索关键词
    
    返回:
        JSON响应: 包含检索结果或生成图片的Base64数据
    """
    try:
        # 用户选择
        if choice_generate !="0":
            generation_result = ali_generate_image_http(
                f"为自媒体文案配图：{keywords}，小红书风格，有文字排版空间"
            )
            
            if generation_result.get('success'):
                image_url=generation_result['image_url']#获取生成的结果URL
                # 解析 URL 获取文件名
                parsed_url = urlparse(image_url)
                path = parsed_url.path  # 获取路径部分，如 "/images/pic.jpg"
                
                # 从路径中提取文件名
                filename = os.path.basename(path)  # 得到 "pic.jpg"
                
                # 安全处理文件名
                filename = secure_filename(filename)
                
                # 如果文件名包含查询参数，需要进一步清理
                if '?' in filename:
                    filename = filename.split('?')[0]
                
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                            
                image_data = download_image(image_url)
                img = PILImage.open(io.BytesIO(image_data))
    
                # 保存为文件
                img.save(file_path)

                if image_data:
                    # 转换为Base64
                    img_base64 = image_to_base64(image_data)
                    current_user_id = get_jwt_identity()
                    new_history = SearchHistory(
                        user_id=int(current_user_id),
                        date=datetime.now(),
                        search_type=0,
                        search_text=keywords,
                        search_pictur=filename
                    )
                    db.session.add(new_history)
                    db.session.commit()
                            
                    return jsonify({
                        'code': 0,
                        'message': 'Image generated successfully',
                        'data': [img_base64],
                        'source': 'generated'
                    })
            return jsonify({
                'code': -2,
                'message': f"Failed to generate image: {generation_result.get('error', 'Unknown error')}",
                'data': None
            })
        else:
            top_k_indices, top_k_similarities = get_top_k_similar_images_fast(
                keywords, 
                image_tensor=image_tensor,
                top_k=3
            )
            
            # 获取最相似图片和相似度
            final_image_paths, similarity_scores= get_top_k_similar_image_slow(
                top_k_indices,
                image_paths,
                keywords,
                top_k_similarities,
                top_k=1
            )
            cleaned_paths = [os.path.basename(path) for path in final_image_paths]
            images = Image.query.filter(
                Image.path.in_([os.path.join(UPLOAD_FOLDER, path) for path in cleaned_paths])
            ).all()
            
            # 去重处理
            unique_images = list({image.path: image for image in images}.values())
            
            # 使用线程池并行处理图片编码
            image_list = []
            with ThreadPoolExecutor() as executor:
                futures = {executor.submit(read_and_encode_image, image.path): image for image in unique_images}
                for future in futures:
                    image = futures[future]
                    img_base64 = future.result()
                    if img_base64:
                        image_list.append({
                            'id': image.id,
                            'path': image.path,
                            'description': image.description,
                            'source': image.source,
                            'format': image.format,
                            'resolution': image.resolution,
                            'image_data': img_base64
                        })
            
            image_out = [image["image_data"] for image in image_list]

            # 记录检索历史
            search_pictur = ','.join(cleaned_paths)
            current_user_id = get_jwt_identity()
            new_history = SearchHistory(
                user_id=int(current_user_id),
                date=datetime.now(),
                search_type=0,
                search_text=keywords,
                search_pictur=search_pictur
            )
            db.session.add(new_history)
            db.session.commit()
                    
            return jsonify({
                'code': 0,
                'message': 'Retrieval successfully',
                'data': image_out,
                'source': 'database'  # 添加来源标识
            })
    except Exception as e:
        return jsonify({
            'code': -1,
            'message': f'Error: {str(e)}',
            'data': None
        })


def init_tongyi_client():
    return OpenAI(
        api_key='sk-47dac4749e0b4ef3bfc92b77ff0cb3a8',
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

# 生成图片配文（增加prompt参数）
def generate_image_caption(image_path, prompt=None):
    """调用通义API生成图片描述文案"""
    client = init_tongyi_client()

    #  base 64 编码格式
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    base64_image = encode_image(image_path)
    
    # 使用自定义prompt或默认prompt
    if not prompt:
        prompt = ("请为这张图片生成适合自媒体平台的配文，要求："
                  "1. 包含2-3个热门话题标签 "
                  "2. 语言风格活泼生动 "
                  "3. 长度在50-100字之间")
    
    try:
        response = client.chat.completions.create(
            model="qwen-vl-plus",  # 使用通义视觉语言模型
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{base64_image}"}
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ],
            stream=False,  # 非流式获取完整回复
            max_tokens=100
        )
        
        # 提取生成的文案内容
        if response.choices and response.choices[0].message.content:
            return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"通义API调用失败: {str(e)}")
        traceback.print_exc()
    
    return "未能生成配文，请稍后再试"

def image_search(image_file,prompt):
    """
    根据上传的图片文件生成配文（替换原来的检索功能）
    
    参数:
        image_file (FileStorage): 上传的图片文件对象
    
    返回:
        JSON 响应: 包含配文结果的 JSON 对象
    """
    
    # 保存上传的文件
    filename = secure_filename(image_file.filename) #取文件名：filename
    file_path = os.path.join(UPLOAD_FOLDER, filename) #获得完整路径D：\...\filename
    image_file.save(file_path)#将image_file存入file_path指定的磁盘中
    
    # 调用通义API生成图片配文
    caption = generate_image_caption(file_path, prompt)
    

    #记录生成历史
    new_history = SearchHistory(
        user_id=1,
        date=datetime.now(),
        search_type=3,  # 3表示图配文生成
        search_text=prompt or "默认配文生成指令",  # 存储使用的prompt
        search_pictur=file_path,
        generated_caption=caption
    )
    
    try:
        db.session.add(new_history)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 0,
            'message': '数据库提交失败',
            'caption': caption
        })

    
    # 返回结果（简化返回结构）
    return jsonify({
        'code': 0,
        'message': '配文生成成功',
        'caption': caption,
        'prompt_used': prompt or "默认指令",
        'search_history_id': new_history.id
    })
