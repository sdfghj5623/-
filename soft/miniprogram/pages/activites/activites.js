const db=wx.cloud.database();
const placeCollection=db.collection('activites')
Page({
  data: {
    activiteList: [], // 存储获取到的视频列表
  },

  navigateToDifferentPage: function(event) {
    // 获取被点击的图片索引
    const index = event.currentTarget.dataset.index;
  

    const item = this.data.activiteList[index];
  console.log("789",this.data.activiteList[index])

    if (item._id === '2b13da7f65e1e4af00402c9278e13a8f') {

      wx.navigateTo({
        url: '/pages/plant/plant',
      });
    } else if (item._id === "5ca5d26765e1e562004119620ff876dd") {
 
      wx.navigateTo({
        url: '/pages/harvest/harvest',
      });
    } else if (item._id === "5ca5d26765e1e5be0041272675ee6f40") {

      wx.navigateTo({
        url: '/pages/pick/pick',
      });
    }
      else if (item._id === "3fa9b31265e1e60f0041484611f886cb") {

        wx.navigateTo({
          url: '/pages/pig/pig',
        });
      }
        else if (item._id === "4662441865e1e635000881bd579fba45") {
 
          wx.navigateTo({
            url: '/pages/tea/tea',
          })
  }
},

  onLoad: function() {

    wx.cloud.callFunction({
      name: 'getActivites',
      success: res => {
        console.log("1",res)
        const activiteList = res.result.data; // 假设云函数返回的数据格式为 [{ src: '文件ID' }, ...]
        this.setData({
          activiteList: activiteList,
        });
      },
      fail: err => {
        console.error(err);
      }
    });
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
      'activite.name':db.RegExp({
        regexp: keyword,
        options: 'i', // 忽略大小写
      })
    }).get().then(res => { 
      this.setData({
        activiteList:res.data,
      });
      console.log("返回结果",res);
     
    }).catch(err => {
      console.log(err);
    });
  },
});