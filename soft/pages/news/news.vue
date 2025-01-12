
<template>
  <view class="home">
    <view class="nav">
      <text class='item' @click="selectNav('policy')" :class="{ active: selectedNav === 'policy' }">政策</text>
      <text class="item" @click="selectNav('technology')" :class="{ active: selectedNav === 'technology' }">技术</text>
    </view>
	<view class="search-bar">
	  <input class="search-input" type="text" placeholder="🔍输入标题关键字" v-model="searchText" @input="handleSearch">
	</view>
    <view class="content">
      <view @click="goDetail(item._id)" class="item" v-for="(item,index) in filteredList" :key="index">
          <view class="text">
          	<view class="title">{{item.title}}</view>
<view class="info">
<!-- <text>{{ formatDate(item.posttime) }}</text> -->
   <text>
      <uni-dateformat
         :date="new Date(item.posttime)" 
         :threshold="[60000, 3600000]"
         format="MM-dd"
      ></uni-dateformat>
   </text>
</view>

          </view>        
<view class="pic">
  <image v-if="item.picurls && item.picurls.length > 0" 
       :src="item.picurls[0]" 
       alt="Article Image" mode="aspectFill"></image>
          	<image v-else mode="aspectFill" src="../../static/images/nopic.jpg"></image>
</view>
      </view>
    </view>
		<view class="goAdd" @click="goAdd" v-if="showIcon1">
			<uni-icons type="plusempty" size="30" color="#fff"></uni-icons>
		</view>
  </view>
</template>
<script>
import axios from 'axios'; // 引入axios库来发起HTTP请求

export default {
  data() {
    return {
      listArr: [],
      selectedNav: 'all',
      searchText: '', // 搜索框输入的内容
      showIcon1: false,
    };
  },

  onLoad() {
    this.getData();
    this.showIcon();
    const app = getApp(); // 获取全局应用实例
    console.log('id', app.globalData.userId);
  },
  onReachBottom() {
    this.getData();
  },
  onPullDownRefresh() {
    this.getData();
  },
  computed: {
    filteredList() {
      if (this.searchText.trim() !== '') {
        return this.listArr.filter(item => item.title.includes(this.searchText));
      } else if (this.selectedNav !== '') {
        if (this.selectedNav == 'all') {
          return this.listArr;
        } else {
          return this.listArr.filter(item => item.author.includes(this.selectedNav));
        }
      }
      return this.listArr;
    }
  },
  methods: {
	  
	      formatDate(timestamp) {
			  console.log(timestamp)
			  const validTimestamp = Number(timestamp);  // 转换为数字
	        const date = new Date(validTimestamp);

	        const month = (date.getMonth() + 1).toString().padStart(2, '0');  // 月份从0开始，所以+1，并补充0			
			console.log('date',date)
	        const day = date.getDate().toString().padStart(2, '0');  // 补充0
	        return `${month}-${day}`;
	      },
    showIcon() {
      let user = uni.getStorageSync('user');
      console.log('111',user);
      if (user.role === '超级用户') {
        this.showIcon1 = true;
      }
    },
    selectNav(nav) {
      this.selectedNav = nav; // 更新选中的导航项
      this.searchText = '';
    },
    goDetail(e) {
let user = uni.getStorageSync('user');
console.log(user);  // 输出存储的用户信息
console.log('e',e)
      if (user !== null) {
        uni.navigateTo({
          url: "/pages/details/details?id=" + e
        });
      } else {
        uni.showToast({
          title: '请登录',
          icon: 'none',
          duration: 2000,
        });
      }
    },
    handleSearch() {
      this.selectedNav = ''; // 清空指导类型
    },
getData() {
    const skip = this.listArr.length;

    axios.get('http://127.0.0.1:5000/api/articles', { 
      params: {
        skip: skip,
        limit: 10,
      }
    }).then(res => {
      console.log("API Response:", res.data); // 输出API响应以进行调试

      let articles = Array.isArray(res.data.articles) ? res.data.articles : [];

      // 更新listArr
      this.listArr = [...this.listArr, ...articles.map(article => ({
        _id: article.id,
        title: article.title,
        posttime: article.time,
        picurls: article.pictures.length > 0
          ? article.pictures.map(pic => {
              if (pic && typeof pic === 'string') {
                return `data:image/jpeg;base64,${pic.trim()}`;
              }
              return null;  // 如果 pic 不是有效的字符串，则返回 null
            }).filter(pic => pic !== null)  // 过滤掉无效的图片
          : ['../../static/images/nopic.jpg'],  // 如果没有图片则显示默认图
        author: article.leibie
      }))];

      console.log('Updated listArr:', this.listArr);

      uni.stopPullDownRefresh();
    }).catch(error => {
      console.error("Error fetching data:", error);
      uni.showToast({
        title: '加载失败，请稍后再试',
        icon: 'none',
        duration: 2000,
      });
    });
  },
    goAdd() {
      uni.navigateTo({
        url: "/pages/tianjia/tianjia"
      });
    },
  }
}
</script>
<style lang="scss" scoped>
.home{
	.nav{
		display: flex;
		justify-content: space-around;
		align-items: center;
		.item{
			flex: 1;
			text-align: center;
		}
	}
	.content{
		padding:30rpx;
		.item{
			display: flex;
			justify-content: space-between;
			padding:20rpx 0;
			border-bottom:1rpx solid #eee;
			.text{
				flex:1;
				display: flex;
				flex-direction: column;
				justify-content: space-between;
				padding-right: 20rpx;
				.title{
					font-size: 44rpx;
					color:#333;
					text-align: justify;
					text-overflow: -o-ellipsis-lastline;
					overflow: hidden;				
					text-overflow: ellipsis;		
					display: -webkit-box;			
					-webkit-line-clamp: 2;			
					line-clamp: 2;					
					-webkit-box-orient: vertical;					
				}
				.info{
					font-size: 28rpx;
					color:#888;
					text{
						padding-right: 20rpx;
					}
				}
			}
			.pic{
				width: 260rpx;
				height: 180rpx;
				image{
					width: 100%;
					height: 100%;
				}
			}
		}
	}

	.goAdd{
		width: 120rpx;
		height: 120rpx;
		background: #2B9939;
		color:#fff;
		display: flex;
		justify-content: center;
		align-items: center;
		border-radius: 50%;
		font-size: 50rpx;
		position: fixed;
		right: 60rpx;
		bottom:100rpx;
		box-shadow: 0 0 20rpx rgba(43,153,57,0.7);
	}
	
	.search-input{
	    border: 1rpx solid rgba(0, 0, 0,0.3);
	    margin-top:50rpx;
	  }
	
	  .search-bar{
	      margin-left: 10%;
	      margin-right:10%;
	  }
	  
	  .item.active{
	  	color:red;
	  }
	  

	  .item {
	    flex: 1;
	    margin: 0 70rpx;
	  }
}
</style>
