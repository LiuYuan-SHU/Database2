from flask import Blueprint, render_template, request

from system import system
from person import Person

# 创建一个名为login_bp的蓝图
login_bp = Blueprint('login', __name__)


def login_sql_query(username, password):
    """
    从数据库中查询用户名和密码，并返回查询结果。

    :param username: 包含用户名的字符串。
    :param password: 包含密码的字符串。
    :return: 包含查询结果的列表，其元素为字典，每个字典包含三个值：{'id', 'username', 'password'}。
    :raises: 若在执行查询时发生异常，则会抛出相关的异常。
    """
    # 从连接池中获取一个数据库连接
    with system.get_database_connection() as conn:
        # 获取数据库游标
        with conn.cursor() as cursor:
            # 执行查询
            sql = "SELECT student_id AS id, username, password FROM student WHERE username = %s AND password = %s UNION " \
                  "SELECT staff_id AS id, username, password FROM teacher WHERE username = %s AND password = %s"
            val = (username, password, username, password)
            cursor.execute(sql, val)

            # 获取查询结果
            result = cursor.fetchall()

    return result


def get_user_type(user_id) -> str:
    """
    获取用户类型。

    根据给定的用户 ID，返回相应的用户类型。

    :param user_id: 包含用户 ID 的字符串。
    :return: 包含用户类型的字符串，可能的取值为 'admin'、'teacher'、'student' 或 'unknown'。
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
        user_id = result[0]['id']
        role = get_user_type(user_id)
        system.set_person_info(Person(user_id=user_id, user_name=username, password=password, user_type=role))
        if role == 'student':
            return '欢迎登录学生账户'
        elif role == 'teacher':
            return '欢迎登录教师账户'
        elif role == 'admin':
            return '欢迎登录管理员账户'
    else:
        # 登录失败
        return '登录失败，请检查用户名和密码'
