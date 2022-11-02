import traceback
import requests
import json
import pymysql
import time


# 获取数据
def get_data():
    # 爬取所有数据
    url = "https://api.inews.qq.com/" \
          "newsqa/v1/query/inner/publish/modules/list?modules=localCityNCOVDataList,diseaseh5Shelf"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    }

    res = requests.get(url, headers)  # res接收返回的结果
    d = json.loads(res.text)  # res.text是json格式，将其转为字典d
    data_all = d["data"]  # 获取d中所有数据
    data = data_all["diseaseh5Shelf"]  # 选中需要的数据

    # 提取时间
    ds = data["lastUpdateTime"][0: 10]

    # 提取总体数据
    total = {}
    l_confirm_add = data["chinaTotal"]["localConfirmAdd"]  # 新增本土
    l_confirmWzz_add = data["chinaAdd"]["noInfectH5"]  # 新增本土无症状
    confirm_add = data["chinaTotal"]["confirmAdd"]  # 新增确诊病例
    dead_add = data["chinaTotal"]["deadAdd"]  # 新增死亡
    l_confirm_now = data["chinaTotal"]["localConfirmH5"]  # 现有本土
    l_confirmWzz_now = data["chinaTotal"]["nowLocalWzz"]  # 现有本土无症状
    confirm_now = data["chinaTotal"]["nowConfirm"]  # 现有确诊
    confirm_all = data["chinaTotal"]["confirm"]  # 累计确诊
    import_all = data["chinaTotal"]["importedCase"]  # 累计境外
    heal_all = data["chinaTotal"]["heal"]  # 累计治愈
    dead_all = data["chinaTotal"]["dead"]  # 累计死亡

    total[ds] = (
        {"l_confirm_add": l_confirm_add, "l_confirmWzz_add": l_confirmWzz_add, "confirm_add": confirm_add,
         "dead_add": dead_add, "l_confirm_now": l_confirm_now, "l_confirmWzz_now": l_confirmWzz_now,
         "confirm_now": confirm_now, "confirm_all": confirm_all, "import_all": import_all, "heal_all": heal_all,
         "dead_all": dead_all})

    # 提取详细数据
    details = []
    update_time = data["lastUpdateTime"]
    province_data = data["areaTree"][0]["children"]
    for pro_infos in province_data:
        province = pro_infos["name"]  # 省名
        for city_infos in pro_infos["children"]:
            city = city_infos["name"]  # 市
            confirm = city_infos["total"]["confirm"]  # 累计确诊
            confirm_add = city_infos["today"]["confirm"]  # 新增确诊
            heal = city_infos["total"]["heal"]  # 累计治愈
            dead = city_infos["total"]["dead"]  # 累计死亡
            details.append([update_time, province, city, confirm, confirm_add, heal, dead])

    return total, details


# 获取连接
def get_conn():
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="123456", charset="utf8", db="epidemic")
    curcor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    return conn, curcor


# 关闭连接
def close_conn(conn, curcor):
    if curcor:
        curcor.close()
    if conn:
        conn.close()


# 更新details表
def update_details():
    curcor = None
    conn = None
    try:
        li = get_data()[1]
        conn, curcor = get_conn()
        sql = "insert into details(update_time, province, city, confirm, confirm_add, heal, dead) values (%s, %s, %s, %s, %s, %s, %s)"
        # 判断是不是最新数据
        sql_query = "select %s=(select update_time from details order by id desc limit 1)"
        curcor.execute(sql_query, li[0][0])
        d = curcor.fetchone()
        flag = None
        for key, value in d.items():
            if value == None:
                flag = True
            elif value == 0:
                flag = True
            else:
                flag = False
        if flag:
            print(f"{time.asctime()}    details表开始更新数据...")
            for item in li:
                curcor.execute(sql, item)
            conn.commit()
            print(f"{time.asctime()}    details表最新数据更新完毕！")
        else:
            print(f"{time.asctime()}    details表已是最新数据，无需更新!")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, curcor)


# 插入total表
def insert_total():
    curcor = None
    conn = None
    try:
        dic = get_data()[0]
        conn, curcor = get_conn()
        sql = "insert into total values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        # 判断是不是最新数据
        for key, value in dic.items():
            date = key
        sql_query = "select %s=(select ds from total order by ds desc limit 1)"
        curcor.execute(sql_query, date)
        d = curcor.fetchone()
        flag = None
        for key, value in d.items():
            if value == None:
                flag = True
            elif value == 0:
                flag = True
            else:
                flag = False
        if flag:
            print(f"{time.asctime()}    total表开始更新数据...")
            for key, v in dic.items():
                curcor.execute(sql, [key, v.get("l_confirm_add"), v.get("l_confirmWzz_add"), v.get("confirm_add"),
                                     v.get("dead_add"), v.get("l_confirm_now"), v.get("l_confirmWzz_now"),
                                     v.get("confirm_now"), v.get("confirm_all"), v.get("import_all"), v.get("heal_all"),
                                     v.get("dead_all")])
                conn.commit()
            print(f"{time.asctime()}    total表最新数据更新完毕！")
        else:
            print(f"{time.asctime()}    total表已是最新数据，无需更新！")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, curcor)



