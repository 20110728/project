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
