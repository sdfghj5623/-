<template>
	<view>
		<view class="image-container">
		<!-- <image class="img" src="https://mp-3d51cb50-4358-420b-bf23-e19be7555bda.cdn.bspapp.com/图片3.png" style="width: 100%;height: 400px;"></image> -->
		<image :src="retrievedImageUrl" class="img" style="width: 100%;height: 400px;" />
	</view>
	
	<view class="apple-box">
		<text class="apple">番茄</text>
	</view>
	<view class="bigbox">
	<view class="view diser">
		<text class="bing">晚疫病</text>
	</view>
	<view class="view idea">
		<view class="o">
		<view class="headline">预防措施  精度：{{score}}%</view>
	发病初期，可喷撒5%百菌清粉尘剂，或5%春雷·王铜粉尘剂，
			每次15 kg/hm2，隔9 d喷1次，连续防治3～4次。从定植时
			开始用药预防，可选用20%吡噻菌胺悬浮剂2 000倍液，或用
			70%代森锰锌可湿性粉剂500倍液、50%多菌灵可湿性粉剂500
			倍液、1∶1∶200波尔多液等喷雾预防。</view>
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