var ec_south = echarts.init(document.getElementById('south'),"dark");

var mydata = [{"province": "北京", "confirm_add": 0}, {"province": "上海", "confirm_add": 0}];

var ec_south_option = {
	//标题样式
	title : {
	    text : "华南新增确诊病例数量TOP5",
	    textStyle : {
	        color : 'white',
	    },
	    left : 'left'
	},
	  color: ['#3398DB'],
	    tooltip: {
	        trigger: 'axis',
	        axisPointer: {            // 坐标轴指示器，坐标轴触发有效
	            type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
	        }
	    },
    xAxis: {
        type: 'category',
        data: []
    },
    yAxis: {
        type: 'value'
    },
    series: [{
        data: mydata,
        type: 'bar',
		barMaxWidth:"50%"
    }]
};
ec_south.setOption(ec_south_option)