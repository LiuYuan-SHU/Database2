import pymysql
from flask import Blueprint, render_template, request
import configparser

# 创建一个名为login_bp的蓝图
login_bp = Blueprint('login', __name__)


def login_sql_query(username, password):
    """
    连接MySQL数据库，并执行查询操作，查询是否有对应的用户名和密码。

    Args:
        username (str): 用户名字符串。
        password (str): 密码字符串。

    Returns:
        result (tuple): 查询结果。如果查询成功，返回一个元组对象，每个元素代表查询的记录行（一条记录是一个元组）；否则返回一个空元组()。
    """
    # 读取配置文件中的数据库连接信息
    config = configparser.ConfigParser()
    config.read('backend/source codes/config.ini')

    database_host = config.get('database', 'host')
    database_user = config.get('database', 'user')
    database_password = config.get('database', 'password')
    database_database = config.get('database', 'database')

    # 连接MySQL数据库
    mydb = pymysql.connect(
        host=database_host,
        user=database_user,
        password=database_password,
        database=database_database
    )

    # 获取数据库游标
    mycursor = mydb.cursor()

    # 执行查询
    sql = "SELECT student_id, username, password FROM student WHERE username = %s AND password = %s UNION " \
          "SELECT staff_id, username, password FROM teacher WHERE username = %s AND password = %s"
    val = (username, password, username, password)
    mycursor.execute(sql, val)

    # 获取查询结果
    result = mycursor.fetchall()

    # 关闭数据库连接
    mycursor.close()
    mydb.close()

    return result


def get_user_type(user_id):
    """
    根据用户ID判断用户类型，返回用户类型。

    Args:
        user_id (str): 用户ID字符串。

    Returns:
        user_type (str): 用户类型字符串。如果用户ID以'0100'开始，则为'admin'；如果以'01'开始，则为'teacher'；如果以'11'开始，则为'student'；否则返回'unknown'。
    """
    if user_id == '0100':
        return 'admin'
    elif user_id.startswith('01'):
        return 'teacher'
    elif user_id.startswith('11'):
        return 'student'
    else:
        return 'unknown'


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

    result = login_sql_query(username, password)
    if len(result) > 0:
        # 登录成功，可以根据不同角色进行不同操作
        role = get_user_type(result[0][0])
        if role == 'student':
            return '欢迎登录学生账户'
        elif role == 'teacher':
            return '欢迎登录教师账户'
        elif role == 'admin':
            return '欢迎登录管理员账户'
    else:
        # 登录失败
        return '登录失败，请检查用户名和密码'
