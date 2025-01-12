// index.js
// const app = getApp()
const { envList } = require('../../envList.js');

Page({
  data: {
    videoList: [], // 存储获取到的视频列表
    count:0
  },

  onLoad: function() {
    console.log("12");
    // 页面加载时调用云函数 "getVideos" 或使用数据库查询获取视频列表数据，更新 data 中的 videoList
    wx.cloud.callFunction({
      name: 'getVideos',
      success: res => {
        console.log("2",res)
        const videoList = res.result.data;
        this.setData({
          videoList: videoList,
        });
        console.log(this.data.videoList)
      },
      fail: err => {
        console.error('123',err);
      }
    });
  },
  onPullDownRefresh() {
    if(this.data.count<12){
      wx.showLoading({
        title: '请稍后...',
        mask:true
      });
    const current = this.data.count + 6;
    this.setData({
      count: current
    });
    setTimeout(() => {
      wx.hideLoading();
      wx.stopPullDownRefresh();
    }, 500);
    // wx.stopPullDownRefresh();
    // wx.hideLoading();
  }
  else{
    const current = 0;
    this.setData({
      count: current
    });
    wx.showToast({
      title: '视频加载完啦，客官不妨到实地领略乡村美景~',
      icon:'none',
      duration:2000,
    })
  }
  },
});
