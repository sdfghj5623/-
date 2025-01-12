const db=wx.cloud.database();
const placeCollection=db.collection('placelist1')
Page({
  data: {
    placeList: [], // 存储获取到的视频列表
    count:0
  },

  navigateToDifferentPage: function (event) {
    // 获取被点击的块的索引
    const index = event.currentTarget.dataset.index;
  
    // 获取对应的块数据
    const item = this.data.placeList[index];
  console.log("789",this.data.placeList[index])
    // 根据块数据判断要跳转的页面，并执行相应的跳转逻辑
    if (item._id === '0553c3616698c78a0096281e21346d75') {
      // 跳转到第一个页面
      wx.navigateTo({
        url: '/pages/guilin/guilin',
      });
    } else if (item._id === '61a71b6e6698c83700976c1679a4eec3') {
      // 跳转到第二个页面
      wx.navigateTo({
        url: '/pages/wan/wan',
      });
    } else if (item._id === '61a71b6e6698c8b80097781719fa9a19') {
      // 跳转到第三个页面
      wx.navigateTo({
        url: '/pages/su/su',
      });
    } else if (item._id === '7f201d406698c915009872e148ece505') {
      // 跳转到第四个页面
      wx.navigateTo({
        url: '/pages/hu/hu',
      });
    }
  },

  onLoad: function() {
    // 页面加载时调用云函数 "getVideos" 或使用数据库查询获取视频列表数据，更新 data 中的 videoList
    // 示例代码：
    wx.cloud.callFunction({
      name: 'getPlace',
      success: res => {
        console.log("1",res)
        const placeList = res.result.data; // 假设云函数返回的数据格式为 [{ src: '文件ID' }, ...]
        this.setData({
          placeList: placeList,
        });
        console.log(this.data.placeList)
      },
      fail: err => {
        console.error(err);
      }
    });
  },

  handleImageTap: function() {
    // 在这里编写图片点击事件的逻辑代码
    // 跳转到百度地图
    wx.openLocation({
      latitude: 39.908823,
      longitude: 116.397470,
      name: '河源东源县',
      address: '目标位置的详细地址'
    })
     
    },
  
  onPullDownRefresh() {
      wx.showLoading({
        title: '请稍后...',
        mask:true
      });
    setTimeout(() => {
      wx.hideLoading();
      wx.stopPullDownRefresh();
    }, 500);
  },

  

  onInputChange: function(event) {
    var keyword = event.detail.value; 
    console.log("输入文字",keyword)
    placeCollection.where({
      'place.position':db.RegExp({
        regexp: keyword,
        options: 'i', // 忽略大小写
      })
    }).get().then(res => { 
      this.setData({
        placeList:res.data,
      });
      console.log("返回结果",res);
     
    }).catch(err => {
      console.log(err);
    });
  },
});