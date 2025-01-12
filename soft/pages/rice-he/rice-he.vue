<template>
	<view>
		<view class="image-container">
		<!-- <image class="img" src="https://mp-3d51cb50-4358-420b-bf23-e19be7555bda.cdn.bspapp.com/图片3.png" style="width: 100%;height: 400px;"></image> -->
		<image :src="retrievedImageUrl" class="img" style="width: 100%;height: 400px;" />
	</view>
	
	<view class="apple-box">
		<text class="apple">草莓</text>
	</view>
	<view class="bigbox">
	<view class="view diser">
		<text class="bing">健康</text>
	</view>
	<view class="view idea">
		<view class="o">
		<view class="headline">护理建议  精度：{{score}}%</view>
	1. 选择合适的土壤和位置
	土壤：草莓喜欢排水良好、富含有机质的土壤。pH值在6.0到6.5之间最为适宜。
	位置：选择充足的阳光照射位置，每天至少需要6小时的直射阳光。同时，确保种植区域通风良好，避免积水。
	2. 种植
	时间：春季是种植草莓的最佳时间，但具体时间取决于当地的气候条件。
	深度：草莓苗的根部应与土壤表面齐平，不要覆盖过深。
	间距：草莓植株之间应保持足够的间距，大约30-45厘米，以便于通风和管理。
	3. 浇水与施肥
	浇水：保持土壤湿润但不过湿。避免在草莓植株上直接浇水，以免导致病害。
	施肥：草莓生长期间需要适量的氮、磷、钾等营养元素。使用平衡的植物肥料，遵循肥料包装上的指导进行施肥。
	4. 病虫害管理
	预防：定期检查草莓植株，避免病虫害的发生。使用有机防治方法，如引入天敌、使用生物农药等。
	治疗：一旦发现病虫害，应立即采取措施控制，避免病害扩散。
	5. 剪枝与修剪
	修剪：定期修剪枯萎或病叶，促进新叶生长。草莓植株生长过程中，适时剪除过密的枝条，保持植株通风良好。
	收获：草莓成熟后，轻轻用手或剪刀摘下，避免损伤植株。
	6. 收获与储存
	收获：草莓成熟时颜色会变深，果面光滑，轻轻触摸时感觉坚实。成熟后应立即收获，避免长时间暴露在阳光下。
	储存：新鲜草莓应存放在冰箱中，可以使用保鲜膜包裹，以延长保鲜期。
	7. 病害预防
	轮作：不同年份在不同的地块种植草莓，以减少病害的传播。
	土壤管理：保持土壤健康，避免过度使用化肥和农药，有助于增强草莓植株的抵抗力。</view>
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