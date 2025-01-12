<template>
	<view>
		<view class="comment-item" @click="goReply">
			<view class="avatar">
<!-- 					<view>{{item.user_id[0]._id}}</view>
					<view>123</view> -->
				 <image src="../../static/images/joker.svg" style="width: 25rpx;height: 25rpx;right: -2.5rpx;bottom: 0rpx;" v-if="item.user_id[0]._id === '65e431ab9755e3283074fbf8'"></image>
				<u-avatar :src="giveAvatar(item)" size="26"></u-avatar>
			</view>
			<view class="wrap">
				<view class="username">
					{{giveName(item)}}
					<text v-if="!closeBtn" class="iconfont icon-a-43-guanbi" @click.stop="delComment"></text>
				</view>
	<!-- 			<view class="comment-content">{{item.comment_content}}</view> -->
				<view :class="['comment-content', {'red-text': item.user_id && item.user_id[0] && item.user_id[0]._id === '65e431ab9755e3283074fbf8'}]">
				  {{ item.comment_content }}
				</view>

				<view class="info">
					<view class="reply-btn" v-if="!childState">{{item.totalReply || ''}}回复 </view>
					<view>
						<uni-dateformat :date="item.comment_date" :threshold="[60000,3600000*24*30]">
						</uni-dateformat>
					</view>
					<view>{{item.province}}</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	import {giveName,giveAvatar} from "../../utils/tools.js"
	const db=uniCloud.database();
	const utilsObj=uniCloud.importObject("utilsObj",{
		customUI: true
	});	
	
	
	export default {
		name: "comment-item",
		data() {
			return {
				showIcon1:false,	

			};
		},
		props:{
			item:{
				type:Object,
				default(){
					return {}
				}
			},
			childState:{
				type:Boolean,
				default:false
			},
			closeBtn:{
				type:Boolean,
				default:false
			}
			
		},
		  mounted() {
		    this.showIcon();
			console.log(this.item)
		  },
		methods:{
			giveName,giveAvatar,
			//跳转去回复页面
			goReply(){
				if(this.childState) return;
				uni.setStorageSync("replyItem",this.item)
				uni.navigateTo({
					url:"/pages/reply/reply"
				})
			},
			
			showIcon(){
				console.log(uniCloud.getCurrentUserInfo().uid)
				let uid = uniCloud.getCurrentUserInfo().uid
				if(uid == '65e431ab9755e3283074fbf8'){
					this.showIcon1 = true
				}		
			},
			
			delComment(){
				let uid=uniCloud.getCurrentUserInfo().uid
				if(uid == this.item.user_id[0]._id ||
				 uid == '65e431ab9755e3283074fbf8' ||
				this.uniIDHasRole('admin') || 
				this.uniIDHasRole('webmaster')){				
					uni.showModal({
						title:"是否确认删除",
						success:res=>{
							if(res.confirm){
								this.removeComment();
							}
						}
					})					
					return;	
				}
				
				uni.showToast({
					title:"权限不够",
					icon:"error"
				})				
				
				
			},
			
			removeComment(){
				db.collection("quanzi_comment").doc(this.item._id).remove()
				.then(res=>{
					uni.showToast({
						title:"删除成功"
					})
					this.$emit("removeEnv",{id:this.item._id})
					if(this.item.comment_count>0){
						utilsObj.operation("quanzi_article","comment_count",this.item.article_id,-1)
					}				
					
				})
			}
		}
	}
</script>

<style lang="scss" scoped>
	.comment-item {
		display: flex;
				.wrap {
			flex: 1;
			padding-left: 20rpx;
			padding-bottom: 20rpx;

			.username {
				font-size: 26rpx;
				color: #666;
				padding: 10rpx 0;
				display: flex;
				align-items: center;
				justify-content: space-between;
				.iconfont{
					font-size: 20rpx;					
					padding:10rpx;
					color:#999;
				}
			}

			.comment-content {
				font-size: 34rpx;
				color: #111;
				line-height: 1.8em;
			}
			
			.red-text {
			  color: red;
			}


			.info {
				font-size: 26rpx;
				color: #666;
				display: flex;
				padding: 10rpx 0;
				align-items: center;

				view {
					margin-right: 25rpx;
				}

				.reply-btn {
					padding: 6rpx 18rpx;
					background: #e4e4e4;
					border-radius: 30rpx;
				}
			}
		}
	}
</style>
