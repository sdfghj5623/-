// pages/tianqi/tianqi.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    date:'',
    tianqi:'',
    week:'',
    update:'',
    tem:'',
    tem1:'',
    tem2:'',
    leve:'',
    zhiliang:'',
    rain:'',
    weel:'',
    weel1:'',
    weel2:'',
    sugg:''
  },

  test:function(){
wx.request({
  url: 'http://v1.yiketianqi.com/api',
  method:"GET",
  data:{
    appid:'73113997',
    appsecret:'Jik6fNGv',
    version:'v62',
    city:'河源'
  },
  success:function(res){
console.log(res.data)
self.setData({

    date:res.data.date,
    tianqi:res.data.wea,
    week:res.data.week,
    update:res.data.update_time,
    tem:res.data.tem,
    tem1:res.data.tem1,
    tem2:res.data.tem2,
    leve:res.data.air_level,
    zhiliang:res.data.air,
    rain:res.data.rain_pcpn,
    weel:res.data.win_speed,
    weel1:res.data.win_meter,
    weel2:res.data.win,
    sugg:res.data.air_tips
})
  }
})
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {self =this

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  }
})