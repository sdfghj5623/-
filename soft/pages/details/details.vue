<template>
	<view class="detail">		
		<view v-if="loadState">			
			<view class="title">{{detail.title}}</view>
			<view class="info">
		<!-- 		<text>{{detail.author}}</text> -->
<text>{{ formatDate(detail.time) }}</text>
			</view>
			<view class="content">
				{{detail.content}}
			</view>
			<view class="picurls" v-if="detail.pictures && detail.pictures.length">
				<image v-for="item in detail.pictures" :src="item" mode="widthFix"></image>
			</view>
			<view class="btnGroup">
				<button size="mini" @click="goEdit" v-if="showIcon1">修改</button>
				<button size="mini" type="warn" @click="onRemove" v-if="showIcon1">删除</button>
			</view>
		</view>
		
		<view v-else>
			<uni-load-more status="loading"></uni-load-more>
		</view>
		
		
	</view>
</template>

<script>
	let id;
	export default {
		data() {
			return {
				detail:{},
				loadState:false,
				showIcon1:false,
			};
		},
		onLoad(e){			
			id=e.id,
			this.showIcon();
		},
		onShow(){
			this.getDetail();
		},
		methods:{
			
			formatDate(timestamp) {
			  console.log(timestamp);
			  const validTimestamp = Number(timestamp);  // 转换为数字
			  const date = new Date(validTimestamp);
			
			  // 获取月份、日期、小时、分钟和秒，且都使用 padStart 补充0，确保是两位数
			  const month = (date.getMonth() + 1).toString().padStart(2, '0');  // 月份从0开始，所以+1，并补充0
			  const day = date.getDate().toString().padStart(2, '0');  // 补充0
			  const hours = date.getHours().toString().padStart(2, '0');  // 获取小时并补充0
			  const minutes = date.getMinutes().toString().padStart(2, '0');  // 获取分钟并补充0
			  const seconds = date.getSeconds().toString().padStart(2, '0');  // 获取秒数并补充0
			
			  return `${month}-${day} ${hours}:${minutes}:${seconds}`;  // 格式化为 MM-DD HH:mm:ss
			},

	            //跳转到修改页面
	            goEdit(){
	            	uni.navigateTo({
	            		url:"/pages/edit1/edit1?id="+id
	            	})
	            },
				
				showIcon(){
					let user = uni.getStorageSync('user');
					if(user.id == 1){
						this.showIcon1 = true
					}		
				},
	            
	            //删除一条记录
	            onRemove(){
	            	uni.showModal({
	            		content:"是否确认删除？",
	            		success:res=>{						
	            			if(res.confirm){
	            				this.removeFun()
	            			}
	            		}					
	            	})			
	            	
	            },
	            
	            removeFun(){		
					      uni.request({
					        url: `http://127.0.0.1:5000/api/article/${id}`, // 后端接口地址，替换为实际地址
					        method: 'DELETE',
					        success(res) {
					          // 请求成功，处理返回数据
					          if (res.statusCode === 200) {
					            uni.showToast({
					              title: '删除成功',
					              icon: 'success'
					            });
								setTimeout(()=>{
									uni.reLaunch({
										url:"/pages/news/news"
									})
								},800)
					          } else {
					            that.message = '删除失败：' + res.data.error;
					            uni.showToast({
					              title: '删除失败',
					              icon: 'none'
					            });
					          }
					        },
					        fail(err) {
					          // 请求失败，处理错误
					          that.message = '请求失败：' + err.errMsg;
					          uni.showToast({
					            title: '请求失败',
					            icon: 'none'
					          });
					        }
					      });
	            },
	
			
			
			
			//获取详情
			getDetail(){
				console.log("iddididid")
				      uni.request({
				        url: `http://127.0.0.1:5000/api/article/${id}`, // 后端接口
				        method: 'GET',
				        success: (res) => {
							console.log(res)
				          if (res.data.article) {
				            this.detail = res.data.article; // 设置文章数据
							this.loadState=true
							this.detail.pictures = Array.isArray(this.detail.pictures) && this.detail.pictures.length > 0
							  ? this.detail.pictures.map(pic => {
							      if (pic && typeof pic === 'string') {
							        return `data:image/jpeg;base64,${pic.trim()}`;
							      }
							      return null;
							    }).filter(pic => pic !== null)
							  : null;


				          } else {
				            uni.showToast({
				              title: '文章未找到',
				              icon: 'none'
				            });
				          }
				        },
				        fail: (err) => {
				          console.log('请求失败:', err);
				          uni.showToast({
				            title: '请求失败，请稍后重试',
				            icon: 'none'
				          });
				        }
				      });
			}
		}
		
	}
</script>

<style lang="scss" scoped>
.detail{
	padding:30rpx;
	.title{
		font-size: 50rpx;
		color:#000;
		text-align: justify;
		line-height: 1.4em;
	}
	.info{
		font-size: 30rpx;
		color:#666;
		padding:30rpx 0 60rpx;
		text{
			padding-right: 30rpx;
		}
	}
	.content{
		font-size: 36rpx;
		line-height: 1.7em;
	}
	.picurls{
		padding-top: 50rpx;
		image{
			width: 100%;
			display: block;
			margin-bottom:30rpx;
		}
	}
	.btnGroup{
		padding:50rpx 0;	
		button{
			margin-right: 30rpx;
		}
	}
}
</style>
