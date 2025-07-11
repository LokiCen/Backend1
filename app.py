from flask import Flask, jsonify  # 导入 Flask 和 jsonify 模块
from flask_cors import CORS  # 导入 CORS 模块用于处理跨域请求
from routes.user import user  # 导入用户蓝图
from routes.search_history import search_history  # 导入检索历史蓝图
from routes.search import search  # 导入搜索蓝图
from routes.faq import faq  # 导入 FAQ 蓝图
from routes.admin import admin  # 导入管理员蓝图
from config import app  # 从 config.py 导入应用实例

# 注册蓝图
with app.app_context():
    app.register_blueprint(user, url_prefix="/user")  # 注册用户蓝图，设置 URL 前缀为 /user
    app.register_blueprint(search, url_prefix="/search")  # 注册搜索蓝图，设置 URL 前缀为 /search
    app.register_blueprint(faq, url_prefix="/faq")  # 注册 FAQ 蓝图，设置 URL 前缀为 /faq
    app.register_blueprint(admin, url_prefix="/admin")  # 注册管理员蓝图，设置 URL 前缀为 /admin
    app.register_blueprint(search_history, url_prefix="/search_history")  # 注册检索历史蓝图，设置 URL 前缀为 /search_history

# 启用跨域资源共享（CORS）配置
CORS(app, resources={
    r"/*": {
    "origins": ["http://10.242.6.160:3030"],  # 允许前端IP访问
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# 测试路由
@app.route('/test')
def test():
    return jsonify({"status": "success", "message": "Backend connected"})

if __name__ == '__main__':
    # 启动 Flask 应用
    app.run(host="0.0.0.0", port=8000, debug=True)
