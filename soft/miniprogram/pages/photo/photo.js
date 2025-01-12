// pages/photo/photo.js
Page({
   

takePhoto: function() {
  wx.chooseImage({
    count: 1, 
    sourceType: ['camera'],
    success: function(res) {
      console.log(res.tempFilePaths);  // 选择成功后的临时文件路径
    },
    fail: function(err) {
      console.error(err); 
    }
  });
  setTimeout(() => {
     wx.redirectTo({
    url: '/pages/question2/question2'
  });
  }, 1000);

},
 

  /**
   * 页面的初始数据
   */
  data: {

  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {

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