from datetime import timedelta, datetime
from flask import jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity
from config import db_init as db
from zhipuai import ZhipuAI
import bcrypt
from Crypto.Cipher import AES
import base64
import os

# AES解密配置
AES_KEY = os.getenv('AES_KEY', 'your-secret-key-123').encode('utf-8')
IV = os.getenv('AES_IV', 'initial-vector-123').encode('utf-8')

def decrypt_password(encrypted_password):
    cipher = AES.new(AES_KEY, AES.MODE_CBC, IV)
    decrypted = cipher.decrypt(base64.b64decode(encrypted_password))
    return decrypted.rstrip(b'\0').decode('utf-8')

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
from models.smart_qa import smartQA # 导入 smartQA 模型
from models.user import User  # 导入 User 模型
import time  # 导入 time 用于生成订单号
from file_download import generate_image, send_image  # 导入图片生成和发送函数


# 用户登录函数
def user_login(username, password):
    """
    用户登录

    参数:
        username (str): 用户名
        password (str): 密码

    返回:
        JSON 响应: 包含登录结果和 JWT 令牌的 JSON 对象
    """
    # 查询用户是否存在
    u = User.query.filter_by(username=username, delete_flag=0).first()
    if not u:
        return jsonify({
            'code': -1,
            'message': 'User does not exist',
            'data': None
        })

    # 解密并比较密码
    decrypted_password = decrypt_password(password)
    if not check_password(decrypted_password, u.password):
        return jsonify({
            'code': -2,
            'message': 'Incorrect password, please try again',
            'data': None
        })

    u_dict = u.to_dict()  # 将用户对象转换为字典
    # 创建JWT访问令牌
    access_token = create_access_token(identity={'username': u.username, 'user_id': u.id},
                                       expires_delta=timedelta(hours=1))

    return jsonify({
        'code': 0,
        'message': 'Login successful',
        'access_token': access_token,
        'data': u_dict
    })


# 用户注册函数
def user_register(email, username, password):
    """
    用户注册

    参数:
        email (str): 用户邮箱
        username (str): 用户名
        password (str): 用户密码

    返回:
        JSON 响应: 包含注册结果的 JSON 对象
    """
    # 检查用户名是否已存在
    if User.query.filter_by(username=username, delete_flag=0).first():
        return jsonify({
            'code': -1,
            'message': 'This username already exists',
            'data': None
        })

    # 检查电子邮件是否已存在
    if User.query.filter_by(email=email, delete_flag=0).first():
        return jsonify({
            'code': -2,
            'message': 'Email already exists',
            'data': None
        })

    # 解密并哈希密码后创建用户
    decrypted_password = decrypt_password(password)
    hashed_password = hash_password(decrypted_password)
    new_user = User(email=email, username=username, password=hashed_password.decode('utf-8'), delete_flag=0, permission_level=1)

    try:
        db.session.add(new_user)  # 添加新用户到数据库会话
        db.session.commit()  # 提交数据库会话
        return jsonify({
            'code': 0,
            'message': 'User registration successful',
            'data': new_user.to_dict()
        })
    except Exception as e:
        db.session.rollback()  # 回滚数据库会话
        return jsonify({
            'code': -3,
            'message': 'User registration failed, please try again',
            'data': None
        })

# 用户重置密码函数
def user_reset_password(username, password):
    """
    重置用户密码

    参数:
        username (str): 用户名
        password (str): 新的用户密码

    返回:
        JSON 响应: 包含编辑结果的 JSON 对象
    """
    # 查询用户是否存在
    u = User.query.filter_by(username=username, delete_flag=0).first()
    if not u:
        return jsonify({
            'code': -1,
            'message': 'User does not exist',
            'data': None
        })

    # 解密并哈希新密码
    decrypted_password = decrypt_password(password)
    u.password = hash_password(decrypted_password).decode('utf-8')

    try:
        db.session.commit()  # 提交数据库会话
        return jsonify({
            'code': 0,
            'message': 'User password reset successfully',
            'data': None
        })
    except Exception as e:
        db.session.rollback()  # 回滚数据库会话
        return jsonify({
            'code': -3,
            'message': 'Password reset failed',
            'data': None
        })


# 用户信息编辑函数
def user_edit(email, password, avatar, nickname, sex, birthday, description):
    """
    编辑用户信息

    参数:
        email (str): 新的用户邮箱
        username (str): 用户名
        password (str): 新的用户密码
        avatar (str): 新的用户头像
        nickname (str): 新的用户昵称
        sex (str): 新的用户性别
        birthday (str): 新的用户生日
        description (str): 新的用户描述

    返回:
        JSON 响应: 包含编辑结果的 JSON 对象
    """
    # 查询用户是否存在
    current_user_id = get_jwt_identity().get('user_id')  # 获取当前用户ID
    u = User.query.filter_by(id=current_user_id, delete_flag=0).first()
    if not u:
        return jsonify({
            'code': -1,
            'message': 'User does not exist',
            'data': None
        })

    updated = False  # 标记是否有字段更新

    # 更新用户信息字段
    if email and u.email != email:
        u.email = email
        updated = True
    if password and u.password != password:
        u.password = password
        updated = True
    if avatar and u.avatar != avatar:
        u.avatar = avatar
        updated = True
    if nickname and u.nickname != nickname:
        u.nickname = nickname
        updated = True
    if sex and u.sex != sex:
        u.sex = sex
        updated = True
    if birthday and u.birthday != birthday:
        u.birthday = birthday
        updated = True
    if description and u.description != description:
        u.description = description
        updated = True

    # 如果没有更新任何字段，返回未修改信息提示
    if not updated:
        return jsonify({
            'code': -100,
            'message': 'User information not updated',
            'data': None
        })

    try:
        db.session.commit()  # 提交数据库会话
        return jsonify({
            'code': 0,
            'message': 'User information updated successfully',
            'data': None
        })
    except Exception as e:
        db.session.rollback()  # 回滚数据库会话
        return jsonify({
            'code': -3,
            'message': 'Update failed',
            'data': None
        })


# 用户删除函数
def user_delete(username, password):
    """
    删除用户

    参数:
        username (str): 用户名
        password (str): 用户密码

    返回:
        JSON 响应: 包含删除结果的 JSON 对象
    """
    # 查询用户是否存在
    u = User.query.filter_by(username=username, delete_flag=0).first()
    if not u:
        return jsonify({
            'code': -1,
            'message': 'User does not exist',
            'data': None
        })

    # 比较密码是否正确
    if u.password != password:
        return jsonify({
            'code': -2,
            'message': 'Incorrect password, please try again',
            'data': None
        })

    u.delete_flag = 1  # 标记用户为已删除
    try:
        db.session.commit()  # 提交数据库会话
        return jsonify({
            'code': 0,
            'message': 'User deleted successfully',
            'data': None
        })
    except Exception as e:
        db.session.rollback()  # 回滚数据库会话
        return jsonify({
            'code': -3,
            'message': 'User deletion failed',
            'data': None
        })




# 用户下载图片函数
def user_download_picture(filename, format, resolution):
    """
    用户下载图片

    参数:
        filename (str): 图片文件名
        format (str): 图片格式
        resolution (str): 图片分辨率

    返回:
        图片文件: 发送图片文件作为响应
    """
    # 从请求中获取参数
    base_image_path = 'D:/code/RetrievalSystemBackend/return_image/'
    temp_image_path = 'D:/code/RetrievalSystemBackend/return_image/'

    # 调用生成图片的函数
    new_filename, new_filepath = generate_image(filename, format, resolution, base_image_path, temp_image_path)

    # 使用发送图片的函数
    return send_image(new_filepath, new_filename)
