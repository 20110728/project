function gettime() {
    $.ajax({
        url: "/time",
        timeout: 3000,
        success: function (data) {
            $("#tim").html(data)
        },
        error: function () {

        }
    })
}

// 获取总体数据
function get_sum_data() {
    $.ajax({
        url: "/sum_data",
        success: function (data) {
            $(".num span").eq(0).text(data[0])
            $(".num span").eq(1).text(data[1])
            $(".num span").eq(2).text(data[2])
            $(".num span").eq(3).text(data[3])
        },
        error: function () {

        }
    })
}

// 获取地图数据
function get_map_data() {
    $.ajax({
        url: "/map_data",
        success: function (data) {
            map_option.series[0].data = data.data
            map.setOption(map_option)
        },
        error: function () {

        }
    })
}

// 定时向后台发起更新数据的请求
function spider() {
    $.ajax({
        url: "/spider",
        success: function (data) {
            console.log(data)
        },
        error: function () {

        }
    })
}

// 定时关闭登录提示信息
setTimeout(function () {
    $("#user-login-message").addClass("hide")
    $("#admain-login-message").addClass("hide")
}, 1000);

gettime();
get_sum_data();
get_map_data();

setInterval(gettime, 1000);
setInterval(spider, 10000);
setInterval(get_sum_data, 10000);
setInterval(get_map_data, 10000);