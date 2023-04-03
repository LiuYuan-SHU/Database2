from flask import Flask, redirect, url_for
from login import login_bp
from system import system

app = Flask(__name__, template_folder='../templates')

# 注册名为login_bp的蓝图
app.register_blueprint(login_bp)


# 主页面路由
@app.route('/')
def index():
    return redirect(url_for('login.login_form'))


if __name__ == '__main__':
    app.run()
