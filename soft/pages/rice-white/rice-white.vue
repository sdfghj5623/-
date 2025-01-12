<template>
	<view>
		<view class="image-container">
		<!-- <image class="img" src="https://mp-3d51cb50-4358-420b-bf23-e19be7555bda.cdn.bspapp.com/图片3.png" style="width: 100%;height: 400px;"></image> -->
		<image :src="retrievedImageUrl" class="img" style="width: 100%;height: 400px;" />
	</view>
	
	<view class="apple-box">
		<text class="apple">玉米</text>
	</view>
	<view class="bigbox">
	<view class="view diser">
		<text class="bing">灰斑病</text>
	</view>
	<view class="view idea">
		<view class="o">
		<view class="headline">预防措施  精度：{{score}}%</view>
	1. 预防措施
	选择抗病品种：优先选择抗灰斑病的玉米品种。
	轮作：避免在同一地块连续种植玉米，实行至少3-4年的轮作，以减少病原菌的积累。
	清除病残体：收获后彻底清除病残体，减少病原菌的越冬场所。
	合理密植：适当降低种植密度，改善田间通风透光条件，减少病害发生。
	2. 化学防治
	早期监测：在病害发生初期开始防治，通常在玉米抽雄前后开始。
	选择药剂：使用有效的杀菌剂，如苯醚甲环唑、戊唑醇、多菌灵等。
	施药时机：根据天气预报和病害发展情况，选择无雨或降雨前后的晴天进行喷施。
	施药频率：根据病害的发展情况和药剂说明书推荐的频率进行施药。</view>
	</view>
<!-- 	<button class="view but" @click="an">提交反馈</button> -->
	</view>
	<view class="fixed-bottom">
	    <view class="fixed-bottom-button">
	        <button @click="an">提交反馈</button>
	    </view>
	</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				ljh:0
			}
		},
		methods: {
			an(){
				uni.navigateTo({
					url:"/pages/user_return/user_return"
				})
				console.log("1`2231")
			}
		},
onLoad(options) {
  this.ljh = options.ljh;
  this.pic = options.pic;
  this.sco = options.sco;
  
  let scoreFromStorage = uni.getStorageSync('score');
  
  if (this.ljh === '1'){
    this.retrievedImageUrl = this.pic;
    this.score = this.sco;
  } else {
	this.retrievedImageUrl = uni.getStorageSync('imageUrl');
	this.score = parseFloat(scoreFromStorage ? scoreFromStorage.toFixed(5) : '0.00000');
  }
  
  this.score = this.score * 100;  // 统一在最后乘以100
},

	}
</script>

<style>
.fixed-bottom {
    position: fixed;
    left: 50%;
    transform: translateX(-50%);
    bottom: 50rpx;
    width: 60%;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: blue;
    color: white;
    padding: 10rpx;
    border-radius: 10rpx;
    height: 5%;
    line-height: 50rpx;
}

.fixed-bottom-button button {
	background-color: blue;
	line-height: 50rpx; 
	color: white; 
}

.strong{
	font-size: 18px;
	color: #000;
	font-weight: bold;
	font-style: oblique;
}
.bigbox {
    position: relative;
    height: 1000px; /* 设置容器高度 */
}

.view {
    position: absolute;
    width: 100%;
    padding: 30rpx;
}

.but{
	background-color: blue;
/* 	margin-top: 500rpx; */
	width: 70%;
	height: 100rpx;
/* 	margin-left: 100rpx; */
/* 	text-align: center; */
	line-height: 50rpx; 
	color: white; 
}

.diser {
	text-align: center;
	background-color: #F0C9C9;
	width: 30%;
	margin-left: 1%;
	margin-top: 1%;
	border-radius: 40rpx;
    z-index: 2; /* 设置上面视图的层级更高 */
}

.idea {
	background-color: #F0C9C9;
	width: 80%;
	margin-left: 40rpx;
	border-radius: 0 72px 68px 73px ; 
	word-break: break-all; /* 在单词内的任意位置换行 */
	white-space: pre-wrap; /* 保留换行符，并允许换行 */
    top: 50px; /* 设置下面视图向下移动 50px，被上面视图部分盖住 */
}
	
.image-container{
	overflow:hidden;
}

.img{
	border-radius: 0 0 160px 160px;
	display: block;
}

.headline{
	font-size: 24px;
	color: #000;
	margin-top: 20rpx;
}

.apple-box{
	margin-top:30rpx;
	width: 50%;
	background-color: #DD4545;
	text-align: center;
}

.apple{
	color: #F1CBCB;
	font-size:48px;
	
}

.bing{
	font-size: 24px;
	color: #000;
	font-weight: bold;
}



.o{
	word-break: break-all; /* 在单词内的任意位置换行 */
	white-space: pre-wrap; /* 保留换行符，并允许换行 */
	margin-left: 20rpx;
}

.center-container {
  display: block;
  justify-content: center;
  align-items: center;
  height: 200rpx; 
}

.center-image {
  width: 500rpx;
  height: 500rpx;
}

</style>