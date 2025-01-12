<template>
	<view class="blogitem">
		<view class="head">
			<view class="userinfo">
				<view class="avatar">
					<image 
					:src="giveAvatar(item)"  
					mode="aspectFill"></image>
				</view>
				<view class="name">
					{{giveName(item)}}
				</view>
				<view class="time">
					<uni-dateformat :date="item.publish_date" format="MM月dd hh:mm" :threshold="[60000,3600000*24*30]"></uni-dateformat>
				</view>
			</view>
			
			<view class="more" @click="clickMore">
				<text class="iconfont icon-ellipsis"></text>
			</view>
		</view>
		
		<view class="body">
			<view class="title" @click="goDetail">{{item.title}}</view>
			<view class="text" @click="goDetail" v-if="item.description">
				<view class="t">{{item.description}}</view>
			</view>
			<view class="piclist" v-if="item.picurls.length">
				<view class="pic" :class="item.picurls.length==1 ? 'only': ''" v-for="(pic,index) in item.picurls" 
				:key="pic">
					<image @click="clickPic(index)" :src="pic" mode="aspectFill"></image>
				</view>					
			</view>
		</view>
		
		
		<view class="info">
			<view class="box">
				<text class="iconfont icon-a-27-liulan"></text> <text>{{item.view_count}}</text>
			</view>
			<view class="box" @click="goDetail">
				<text class="iconfont icon-a-5-xinxi"></text> 
				<text>{{item.comment_count && item.comment_count>0 ? item.comment_count : '评论'}}</text>
			</view>
			<view class="box" :class="item.isLike ? 'active' : ''" @click="clickLike">
				<text class="iconfont icon-a-106-xihuan"></text> 
				<text>{{item.like_count ? item.like_count : '点赞'}}</text>
			</view>
		</view>
		
		
		
		<u-action-sheet :actions="list" cancelText="取消" :show="sheetShow" 
		:closeOnClickOverlay="true" :closeOnClickAction="true" 
		@select="sheetSelect"
		@close="onClose"
		></u-action-sheet>
	</view>
</template>

<script>
	import pageJson from "@/pages.json"
	import {giveName,giveAvatar,likeFun} from "../../utils/tools.js"	
	import {
		store		
	} from '@/uni_modules/uni-id-pages/common/store.js'
	const db=uniCloud.database()
	export default {
		name:"blog-item",
		props:{
			item:{
				type:Object,
				default(){
					return {
						
					}
				}
			},
			isLike:false,
			like_count:Number
		},
		data() {
			return {
				sheetShow:false,
				list:[
					{
						name:"删除",
						type:"del",
						color:"#F56C6C",
						disabled:true
					}
				]
			};
		},
methods: {
  giveName,
  giveAvatar,
  // 点赞操作
  // clickLike() {
  //   if (!store.hasLogin) {
  //     uni.showModal({
  //       title: "登录后才可进行后续操作",
  //       success: res => {
  //         if (res.confirm) {
  //           uni.navigateTo({
  //             url: "/" + pageJson.uniIdRouter.loginPage
  //           });
  //         }
  //       }
  //     });
  //     return;
  //   }

  //   let time = Date.now();
  //   if (time - this.likeTime < 2000) {
  //     uni.showToast({
  //       title: "操作太频繁，请稍后...",
  //       icon: "none"
  //     });
  //     return;
  //   }

  //   this.likeTime = time;

  //   // 这里我们在本地状态中进行修改，而不是直接修改 props
  //   let like_count = this.item.like_count;
  //   let isLike = !this.item.isLike;

  //   // 更新本地状态并发射事件通知父组件
  //   this.item.isLike = isLike;
  //   this.item.like_count = isLike ? like_count + 1 : like_count - 1;

  //   this.$emit("update:isLike", this.item.isLike);
  //   this.$emit("update:like_count", this.item.like_count);

  //   likeFun(this.item._id);
  // },
  // 点赞操作
  clickLike() {
    if (!store.hasLogin) {
      uni.showModal({
        title: "登录后才可进行后续操作",
        success: res => {
          if (res.confirm) {
            uni.navigateTo({
              url: "/" + pageJson.uniIdRouter.loginPage
            });
          }
        }
      });
      return;
    }
  
    // 防止频繁点击
    let time = Date.now();
    if (time - this.likeTime < 2000) {
      uni.showToast({
        title: "操作太频繁，请稍后...",
        icon: "none"
      });
      return;
    }
  
    this.likeTime = time;
  
    // 更新本地状态
    this.item.isLike = !this.item.isLike;
    this.item.like_count += this.item.isLike ? 1 : -1;
  
    // 向父组件发出事件，更新父组件中的数据
    this.$emit("update:isLike", this.item.isLike);
    this.$emit("update:like_count", this.item.like_count);
  
    // 调用点赞接口
    likeFun(this.item._id);
  },


  // 点击更多操作
  clickMore() {
    let uid = uniCloud.getCurrentUserInfo().uid;
    if (uid == "65e431ab9755e3283074fbf8") {
      this.list.forEach(item => {
        item.disabled = false;
      });
    }
    this.sheetShow = true;
  },

  // 点击选择
  sheetSelect(e) {
    this.sheetShow = false;
    let type = e.type;
    if (type == "del") {
      this.delFun();
    }
  },

  delFun() {
    uni.showLoading({
      title: "加载中..."
    });
    db.collection("quanzi_article")
      .doc(this.item._id)
      .update({
        delState: true
      })
      .then(res => {
        uni.hideLoading();
        uni.showToast({
          title: "删除成功",
          icon: "none"
        });
        this.$emit("delEvent", true);
      })
      .catch(err => {
        uni.hideLoading();
      });
  },

  // 取消弹窗
  onClose() {
    this.sheetShow = false;
  },

  // 点击跳转到详情
  goDetail() {
    uni.navigateTo({
      url: "/pages/detail2/detail2?id=" + this.item._id
    });
  },

  // 单击图片
  clickPic(index) {
    uni.previewImage({
      urls: this.item.picurls,
      current: index
    });
  }
}

	}
</script>

<style lang="scss">
.blogitem{
	.head{
		display:flex;
		font-size: 32rpx;
		align-items: center;
		justify-content: space-between;
		.userinfo{
			display: flex;
			align-items: center;
			.avatar{ 
				width: 40rpx;
				height: 40rpx;
				border-radius: 50%;
				border-radius: 50%;
				overflow: hidden;
				image{ 
					width: 100%;
					height: 100%;
					display: block;
				}
			}
			.name{				
				color:#222;				
				padding-left:10rpx;
			}
			.time{
				color:#888;
				font-size: 22rpx;
				padding-left:20rpx;
			}
		}
		.more{
			padding:5rpx;			
			.iconfont{ 
				font-size: 50rpx;
				color:#888;
			}
		}
	}
	
	
	
	.body{
		padding:15rpx 0 30rpx;
		.title{
			font-size: 44rpx;
			color:#000;
			font-weight: 600;	
			text-align: justify;
			text-overflow: -o-ellipsis-lastline;
			overflow: hidden;				
			text-overflow: ellipsis;		
			display: -webkit-box;			
			-webkit-line-clamp: 2;			
			line-clamp: 2;					
			-webkit-box-orient: vertical;	
		}
		.text{
			padding-top:10rpx;
			padding-bottom:10rpx;
			font-size: 30rpx;
			text-align: justify;
			color:#888;				
			.t{
				text-overflow: -o-ellipsis-lastline;
				overflow: hidden;				
				text-overflow: ellipsis;		
				display: -webkit-box;			
				-webkit-line-clamp: 2;			
				line-clamp: 2;					
				-webkit-box-orient: vertical;	
			}
		}
		.piclist{
			display: flex;
			padding-top:20rpx;
			.pic{
				width: 225rpx;
				height: 225rpx;
				margin-right: 6rpx;
				overflow: hidden;
				image{
					width: 100%;
					height: 100%;
				}	
				&:first-child{
					border-radius: 20rpx 0 0 20rpx;					
				}
				&:last-child{
					border-radius: 0 20rpx 20rpx 0;					
				}
				&.only{
					border-radius: 20rpx;
				}
				
			}
			
		}
	}
	
	
	
	
	.info{
		display: flex;
		align-items: center;
		justify-content:space-around;
		font-size: 26rpx;	
		color:#333;
		.box{
			display: flex;
			align-items: center;			
			padding:15rpx 0 5rpx;
			flex:1;
			display: flex;
			justify-content: center;
			.iconfont{
				font-size: 40rpx;
				padding-right: 10rpx;
			}
		}
		.box.active{
			color:#0199FE
		}
		
	}
	
	
}
</style>