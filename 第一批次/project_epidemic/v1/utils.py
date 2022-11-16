import time
import pymysql


# 获取当前时间
def get_time():
    time_str = time.strftime("%Y{}%m{}%d{} %X")
    return time_str.format("年", "月", "日")


# 获取连接
def get_conn():
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="20110728", charset="utf8", db="epidemic")
    curcor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    return conn, curcor


# 关闭连接
def close_conn(conn, curcor):
    if curcor:
        curcor.close()
    if conn:
        conn.close()


# 通用查询
def query(sql, *args):
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    close_conn(conn, cursor)
    return res


# 获取累计信息
def get_sum_data():
    sql = "select confirm_all, import_all, heal_all, dead_all from total " \
          "where ds = (select ds from details order by update_time desc limit 1)"
    res = query(sql)
    return res[0]


# 读取各省数据
def get_map_data():
    sql = "select province, sum(confirm_add) from details " \
          "where update_time=(select update_time from details order by update_time desc limit 1) " \
          "group  by province"
    res = query(sql)
    return res


def get_north_data():
    """
    :return:  返回华北地区省份新增确诊人数前5名
    """
    sql = 'SELECT province,confirm_add FROM (select province,sum(confirm_add) as confirm_add from details where ' \
          'update_time=(select update_time from details order by update_time desc limit 1) group by province) as a ' \
          'where province="黑龙江" or province="吉林" or province="辽宁" or province="北京" or province="天津" or province="河北" ' \
          'or province="河南" or province="山东" or province="山西" or province="陕西" or province="内蒙古" or province="安徽" ' \
          'ORDER BY confirm_add ' \
          'DESC LIMIT 5 '
    res = query(sql)
    return res


def get_south_data():
    """
    :return:  返回华南地区省份新增确诊人数前5名
    """
    sql = 'SELECT province,confirm_add FROM (select province,sum(confirm_add) as confirm_add from details where ' \
          'update_time=(select update_time from details order by update_time desc limit 1) group by province) as a ' \
          'where province="江苏" or province="上海" or province="浙江" or province="湖北" or province="湖南" or province="福建" ' \
          'or province="广东" or province="广西" or province="江西" or province="台湾" or province="海南" or province="香港" or ' \
          'province="澳门" ' \
          'ORDER BY confirm_add ' \
          'DESC LIMIT 5 '
    res = query(sql)
    return res


def get_west_data():
    """
    :return:  返回西部地区省份新增确诊人数前5名
    """
    sql = 'SELECT province,confirm_add FROM (select province,sum(confirm_add) as confirm_add from details where ' \
          'update_time=(select update_time from details order by update_time desc limit 1) group by province) as a ' \
          'where province="新疆" or province="青海" or province="西藏" or province="甘肃" or province="宁夏" or province="四川" ' \
          'or province="重庆" or province="贵州" or province="云南" ORDER BY confirm_add ' \
          'DESC LIMIT 5 '
    res = query(sql)
    return res


def get_predict_data():
    sql = "select ds,l_confirm_add,l_confirmWzz_add from total"
    res = query(sql)
    return res


def get_predict_config():
    sql = "select x1,x2,x3,x4,x5,c,base_number from config"
    res = query(sql)
    return res


# 登录
def login(username, password, ifRoot):
    sql1 = "select * from user where username = %s"
    res1 = query(sql1, username)
    if res1 == ():
        return 1  # 用户名不存在
    sql2 = "select * from user where username = %s and password = %s"
    res2 = query(sql2, username, password)
    if res2 == ():
        return 2  # 密码错误
    else:
        if ifRoot == "1":
            sql3 = "select * from user where username = %s and password = %s and ifRoot = 1"
            res3 = query(sql3, username, password)
            if res3 == ():
                return 4  # 当前用户非管理员用户
            else:
                return 5  # 管理员登录成功
        else:
            return 3  # 普通用户登录成功


# 注册
def register(username, password):
    sql1 = "select * from user where username = %s"
    res1 = query(sql1, username)
    if res1 == ():
        conn = None
        cursor = None
        try:
            conn, cursor = get_conn()
            sql2 = "INSERT INTO user VALUES(%s, %s, 0)"
            cursor.execute(sql2, [username, password, ])
            conn.commit()
        finally:
            close_conn(conn, cursor)
        return 1  # 注册成功
    else:
        return 2  # 用户名已存在


# 更改密码
def change_password(now_password, new_password, now_username):
    sql1 = "select * from user where username = %s and password = %s"
    res1 = query(sql1, now_username, now_password)
    if res1 == ():
        return 1  # 密码错误
    else:
        conn = None
        cursor = None
        try:
            conn, cursor = get_conn()
            sql2 = "UPDATE USER SET PASSWORD = %s WHERE username = %s"
            cursor.execute(sql2, [new_password, now_username, ])
            conn.commit()
        finally:
            close_conn(conn, cursor)
        return 2  # 更新成功


# 新增管理员
def add_root(username, password):
    sql1 = "select * from user where username = %s"
    res1 = query(sql1, username)
    if res1 == ():
        conn = None
        cursor = None
        try:
            conn, cursor = get_conn()
            sql2 = "INSERT INTO user VALUES(%s, %s, 1)"
            cursor.execute(sql2, [username, password, ])
            conn.commit()
        finally:
            close_conn(conn, cursor)
        return 1  # 注册成功
    else:
        return 2  # 用户名已存在


def change_parameter(x1, x2, x3, x4, x5, c, base_number):
    conn = None
    cursor = None
    try:
        conn, cursor = get_conn()
        sql2 = "update config SET x1=%s,x2=%s,x3=%s,x4=%s,x5=%s,c=%s,base_number=%s"
        cursor.execute(sql2, [x1, x2, x3, x4, x5, c, base_number, ])
        conn.commit()
        return 1  # 修改成功
    except ValueError :
        return 2  # 修改失败
    finally:
        close_conn(conn, cursor)



# 查看评论
def view_comments():
    conn = None
    cursor = None
    try:
        conn, cursor = get_conn()
        sql = "select * from comments order by id desc "
        cursor.execute(sql)
        data_list = cursor.fetchall()
    finally:
        close_conn(conn, cursor)
    return data_list  # 更新成功
    # 列表形式


# 新增评论
def insert_com(tittle, comment, publisher, p_time):
    if publisher == None or publisher == "":
        publisher = "匿名"
    conn = None
    cursor = None
    try:
        conn, cursor = get_conn()
        sql = "INSERT INTO comments VALUES(null, %s, %s, %s, %s)"
        cursor.execute(sql, [comment, publisher, p_time, tittle, ])
        conn.commit()
    finally:
        close_conn(conn, cursor)
    return 1  # 添加成功
