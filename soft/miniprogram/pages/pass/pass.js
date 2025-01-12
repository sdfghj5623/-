Page({
  data: {
    boxImageSrc: 'cloud://nodio-8go2apw3520fc13b.6e6f-nodio-8go2apw3520fc13b-1323726217/宝箱.png', // 宝箱关闭的图片路径
    isOpen: false // 默认宝箱为关闭状态
  },

  return:function(){
    wx.redirectTo({
      url: '/pages/games/games'
    });
  },
  
  openTreasureBox: function() {
    if (this.data.isOpen) {
      return;
    }
  
    // 切换图片路径，代表宝箱打开的状态
    this.setData({
      boxImageSrc: 'cloud://nodio-8go2apw3520fc13b.6e6f-nodio-8go2apw3520fc13b-1323726217/宝箱2.png', // 宝箱打开的图片路径
    
    });
    wx.showToast({
      title:'积分+50',
      icon:'none',
      duration:1000,
    });
    setTimeout(() => {
      this.setData({
     isOpen: true
      });
    }, 1000);
    const openid = getApp().globalData.openid;
    const db = wx.cloud.database();
    const userCollection = db.collection('user');
  
    // 根据openid找到对应的用户
    userCollection.where({
      _openid: openid
    }).get().then(res => {
      // 找到了对应的用户  
      console.log("123",res)
      if (res.data.length > 0) {
      
        const user = res.data[0];
        // 更新用户的points字段
        userCollection.doc(user._id).update({
          data: {
            points: user.points+50
          }
        }).then(() => {
          console.log('用户points字段更新成功');
        }).catch(err => {
          wx.showToast({
            title:'您未登录',
            icon:'none',
            duration:1000,
          });
          console.error('用户points字段更新失败', err);
        });
      } else {
        wx.showToast({
          title:'您未登录',
          icon:'none',
          duration:1000,
        });
        console.log('未找到对应的用户');
      }
    }).catch(err => {
      wx.showToast({
        title:'您未登录',
        icon:'none',
        duration:1000,
      });
      console.error('根据openid查询用户失败', err);
    });
  }
});