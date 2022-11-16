import datetime

from flask import Flask, render_template, jsonify, request

import utils
import spider
import time

app = Flask(__name__)


# 评论区
@app.route("/comments", methods=["get", "post"])
def comments():
    data_list = utils.view_comments()
    username = request.form.get("now_username")
    if username == None or username == "":
        com_type = 1
    else:
        com_type = 2

    return render_template("comments.html", data_list=data_list, username=username, com_type=com_type)


# 发表评论
@app.route("/add/comments", methods=["get", "post"])
def add_comments():
    publisher = request.form.get("com_user")
    tittle = request.form.get("c_title")
    comment = request.form.get("c_content")
    p_time = get_time()

    if tittle == None or tittle == "":
        ac_type = -1
    elif comment == None or comment == "":
        ac_type = -2
    else:
        ac_type = utils.insert_com(tittle, comment, publisher, p_time)

    return render_template("comments.html", ac_type=ac_type)


# 获取时间
@app.route("/time", methods=["get", "post"])
def get_time():
    return utils.get_time()


# 获取总体数据
@app.route("/sum_data", methods=["get", "post"])
def get_sum_data():
    data = utils.get_sum_data()
    d = []
    for k, v in data.items():
        d.append(v)

    return d


# 获取地图数据
@app.route("/map_data")
def get_map_data():
    res = []
    for tup in utils.get_map_data():
        res.append({"name": tup["province"], "value": int(tup["sum(confirm_add)"])})
    return jsonify({"data": res})


@app.route("/north")
def get_north_data():
    data = utils.get_north_data()
    province = []
    confirm = []
    for k in data:
        dict1 = dict(k)
        province.append(dict1['province'])
        confirm.append(int(dict1['confirm_add']))
    return jsonify({"province": province, "confirm": confirm})


@app.route("/south")
def get_south_data():
    data = utils.get_south_data()
    province = []
    confirm = []
    for k in data:
        dict1 = dict(k)
        province.append(dict1['province'])
        confirm.append(int(dict1['confirm_add']))
    return jsonify({"province": province, "confirm": confirm})


@app.route("/west")
def get_west_data():
    data = utils.get_west_data()
    province = []
    confirm = []
    for k in data:
        dict1 = dict(k)
        province.append(dict1['province'])
        confirm.append(int(dict1['confirm_add']))
    return jsonify({"province": province, "confirm": confirm})


@app.route("/predict")
def get_predict_data():
    data = utils.get_predict_data()
    config = utils.get_predict_config()
    x1 = 0
    x2 = 0
    x3 = 0
    x4 = 0
    x5 = 0
    c = 1
    base_number = 1
    for conf in config:
        x1 = conf['x1']
        x2 = conf['x2']
        x3 = conf['x3']
        x4 = conf['x4']
        x5 = conf['x5']
        c = conf['c']
        base_number = conf['base_number']
        break

    day, confirm_add, suspect_add = [], [], []
    sum1 = 0
    time1 = datetime.datetime.now()
    for t in data[3:]:
        dict1 = dict(t)
        day.append(dict1['ds'].strftime("%m-%d"))  # a是datatime类型
        confirm_add.append(dict1['l_confirm_add'])
        suspect_add.append(dict1['l_confirmWzz_add'])
        sum1 = sum1 + dict1['l_confirm_add']
        time1 = dict1['ds']
    for j in range(4, 10):
        temp = time1
        for i in range(1, j):
            temp = (temp + datetime.timedelta(days=1))
        day.append(temp.strftime("%m-%d"))
        confirm_add.append(int(pow(sum1 / (3 * base_number), 1 / 10) * (
                x1 * pow(j, 1) + x2 * pow(j, 2) + x3 * pow(j, 3) + x4 * pow(j, 4) + x5 * pow(j, 5)) + c))
    return jsonify({"day": day, "confirm_add": confirm_add, "suspect_add": suspect_add})


# 注册
@app.route("/register", methods=["get", "post"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("re_username")
        password = request.form.get("re_password")
        if username == None or username == "":
            register_type = 3
        elif password == None or password == "":
            register_type = 4
        else:
            register_type = utils.register(username, password)

        return render_template("register.html", register_type=register_type)


# 登录
@app.route("/login", methods=["get", "post"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    ifRoot = request.form.get("ifRoot")
    if ifRoot == None:
        ifRoot = 0

    if username == None or username == "":
        login_type = -1
    elif password == None or password == "":
        login_type = -2
    else:
        login_type = utils.login(username, password, ifRoot)

    return render_template("index.html", login_type=login_type, username=username)


# 修改密码
@app.route("/change/password", methods=["get", "post"])
def change_password():
    now_password = request.form.get("now_password")
    new_password = request.form.get("new_password")
    now_username = request.form.get("now_username")

    if now_password == None or now_password == "":
        change_password_type = -1
    elif new_password == None or new_password == "":
        change_password_type = -2
    else:
        change_password_type = utils.change_password(now_password, new_password, now_username)

    return render_template("index.html", change_password_type=change_password_type)


# 添加管理员
@app.route("/add/root", methods=["get", "post"])
def add_root():
    if request.method == "GET":
        return render_template("index.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        if username == None or username == "":
            add_root_type = -1
        elif password == None or password == "":
            add_root_type = -2
        else:
            add_root_type = utils.add_root(username, password)

        return render_template("index.html", add_root_type=add_root_type)


@app.route("/change/parameter", methods=["get", "post"])
def change_parameter():
    if request.method == "GET":
        return render_template("index.html")
    else:
        x1 = request.form.get("x1")
        x2 = request.form.get("x2")
        x3 = request.form.get("x3")
        x4 = request.form.get("x4")
        x5 = request.form.get("x5")
        c = request.form.get("c")
        base_number = request.form.get("base_number")
        print(x1, x2, x3, x4, x5, c, base_number)
        if x1 is None or x1 == "" or x1 == "" or x2 == "" or x3 == "" or x4 == "" or x5 == "" or c == "" or base_number == "":
            change_parameter_type = -1
        else:
            change_parameter_type = utils.change_parameter(x1, x2, x3, x4, x5, c, base_number)

        return render_template("index.html", change_parameter_type=change_parameter_type)


# 主页
@app.route("/", methods=["get", "post"])
def index():
    if request.method == "GET":
        return render_template("index.html")


# 爬虫开启
@app.route("/spider", methods=["get", "post"])
def spider_start():
    spider.update_details()
    spider.insert_total()
    return "updating data..."


if __name__ == '__main__':
    spider_start()
    print(f"{time.asctime()}    正在启动...")
    app.run()
