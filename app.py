from flask import Flask, render_template, redirect, request
import webbrowser

app = Flask(__name__)

# 用于呈现登录表单的路由
@app.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')

# 用于验证表单数据并重定向到主页面的路由
@app.route('/login', methods=['POST'])
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

# 主页面路由
@app.route('/')
def index():
    return '你已经成功登录了！'

if __name__ == '__main__':
    app.run()