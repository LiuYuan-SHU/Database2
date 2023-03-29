from flask import Blueprint, render_template, redirect, request, url_for

# 创建一个名为login_bp的蓝图
login_bp = Blueprint('login', __name__)

# 用于呈现登录表单的路由
@login_bp.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')

# 用于验证表单数据并重定向到主页面的路由
@login_bp.route('/login', methods=['POST'])
def login():
    # 取出表单中传来的用户名和密码
    username = request.form.get('username')
    password = request.form.get('password')

    # 判断用户名和密码是否正确
    if username == 'admin' and password == 'password':
        # 用户名和密码正确，重定向到主页面
        return redirect('/')
    else:
        # 用户名或密码错误，显示登录表单并给出错误提示
        return render_template('login.html', error='用户名或密码错误')