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

// 获取华北地区数据
function get_north_data() {
    $.ajax({
        url: "/north",
        success: function (data) {
            ec_north_option.xAxis.data=data.province;
            ec_north_option.series[0].data=data.confirm;
            ec_north.setOption(ec_north_option);
        },
        error: function () {

        }
    })
}

// 获取华南地区数据
function get_south_data() {
    $.ajax({
        url: "/south",
        success: function (data) {
            ec_south_option.xAxis.data=data.province;
            ec_south_option.series[0].data=data.confirm;
            ec_south.setOption(ec_south_option);
        },
        error: function () {

        }
    })
}

// 获取西部地区数据
function get_west_data() {
    $.ajax({
        url: "/west",
        success: function (data) {
            ec_west_option.xAxis.data=data.province;
            ec_west_option.series[0].data=data.confirm;
            ec_west.setOption(ec_west_option);
        },
        error: function () {

        }
    })
}

function get_predict_data() {
    $.ajax({
        url:"/predict",
        success: function(data) {
			ec_predict_Option.xAxis[0].data=data.day
            ec_predict_Option.series[0].data=data.confirm_add
            ec_predict_Option.series[1].data=data.suspect_add
            ec_predict.setOption(ec_predict_Option)
		},
		error: function(xhr, type, errorThrown) {

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
get_north_data();
get_south_data();
get_west_data();
get_predict_data();

setInterval(gettime, 1000);
setInterval(spider, 10000);
setInterval(get_sum_data, 10000);
setInterval(get_map_data, 10000);
setInterval(get_north_data,10000);
setInterval(get_south_data,10000);
setInterval(get_west_data,10000);
setInterval(get_predict_data,10000);