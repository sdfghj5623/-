<template>
	<view>
		<view class="image-container">
		<image class="img" src="https://mp-3d51cb50-4358-420b-bf23-e19be7555bda.cdn.bspapp.com/微信图片_20240302004843.jpg" style="width: 100%;height: 400px;"></image>
	</view>
	
	<view class="apple-box">
		<text class="apple">番茄</text>
	</view>
	<view class="bigbox">
	<view class="view diser">
		<text class="bing">斑枯病</text>
	</view>
	<view class="view idea">
		<view class="o">
		<view class="headline">预防措施</view>
	化学防治。发病前，喷施75%百菌清可湿性粉剂1200倍液，或70%
	代森猛锌1500倍液进行喷洒，隔10~15天喷1次，连喷2~3次。发病
	高峰期，喷施80%新万生可湿性粉剂1000倍液，或64%杀毒可湿性
	粉剂500倍液，或58%甲霜灵？话锌500倍液，隔7~9天喷1次，连喷2~3次</view>
	</view>
	<button class="view but" @click="an">提交反馈</button>
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
  
  if (this.ljh === '1') {
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
