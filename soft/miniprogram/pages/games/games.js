// pages/games/games.js
Page({

  data: {
    boxColor: 'rgb(225,225,225,0.7)',
    boxColor1: 'rgb(225,225,225,0.7)',
    boxColor2: 'rgb(225,225,225,0.7)',
    isColorChanged: false,
    isColorChanged1: false,
    isColorChanged2: false,
    poinsts:0,
  },
  changeColor: function() {
    if (!this.data.isColorChanged) {
      this.setData({
        boxColor: '#ea4a07',
        isColorChanged: true
      });
    }
  },
  changeColor1: function() {
    if (!this.data.isColorChanged1) {
      this.setData({
        boxColor1: '#ea4a07',
        isColorChanged1: true
      });
    }
  },
  changeColor2: function() {
    if (!this.data.isColorChanged2) {
      this.setData({
        boxColor2: '#ea4a07',
        isColorChanged2: true
      });
    }
  },
  onShow: function() {
    if (this.data.isColorChanged) {
      this.setData({
        boxColor: 'rgb(225,225,225,0.7)',
        isColorChanged: false,
      });
    }
    if (this.data.isColorChanged1) {
      this.setData({
        boxColor1: 'rgb(225,225,225,0.7)',
        isColorChanged1: false
      });
    }
    if (this.data.isColorChanged2) {
      this.setData({
        boxColor2: 'rgb(225,225,225,0.7)',
        isColorChanged2: false
      });
    }
  },
  onLoad:function(){
    const openid = getApp().globalData.openid;
    const db = wx.cloud.database();
    const userCollection = db.collection('user');
  
 
    userCollection.where({
      _openid: openid
    }).get().then(res => {
    
      console.log("123",res)
      if (res.data.length > 0) {
      this.setData({
        points:res.data[0].points
      })
    }
  }
    )
   }


        

})