// pages/question1/question1.js
Page({

  data: {
    boxColor: 'rgb(225,225,225,0.7)',
    boxColor1: 'rgb(225,225,225,0.7)',
    boxColor2: 'rgb(225,225,225,0.7)',
    isColorChanged: false,
    isColorChanged1: false,
    isColorChanged2: false
  },
  changeColor: function() {
    if (!this.data.isColorChanged) {
      this.setData({
        boxColor: '#ff0000',
        isColorChanged: true
      });
    }
    wx.showToast({
      title:'再想想哦~-5',
      icon:'none',
      duration:1000,
    });
    setTimeout(() => {
      this.setData({
        boxColor: 'rgb(225,225,225,0.7)',
        isColorChanged: false
      });
    }, 200);
    // 获取用户的openid
  const openid = getApp().globalData.openid;

  // 使用云开发调用数据库API
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
          points: user.points-5
        }
      }).then(() => {
        console.log('用户points字段更新成功');
      }).catch(err => {
        console.error('用户points字段更新失败', err);
      });
    } else {
      console.log('未找到对应的用户');
    }
  }).catch(err => {
    console.error('根据openid查询用户失败', err);
  });
  },
  changeColor1: function() {
    if (!this.data.isColorChanged1) {
      this.setData({
        boxColor1: '#00b26a',
        isColorChanged1: true
      });
    }
    wx.showToast({
      title:'真厉害~+10',
      icon:'none',
      duration:1000,
    });
    wx.redirectTo({
      url: '/pages/photo/photo'
    });
    // 获取用户的openid
  const openid = getApp().globalData.openid;

  // 使用云开发调用数据库API
  const db = wx.cloud.database();
  const userCollection = db.collection('user');

  // 根据openid找到对应的用户
  userCollection.where({
    _openid: openid
  }).get().then(res => {
    // 找到了对应的用户
    if (res.data.length > 0) {
      const user = res.data[0];
      // 更新用户的points字段
      userCollection.doc(user._id).update({
        data: {
          points: user.points + 10
        }
      }).then(() => {
        console.log('用户points字段更新成功');
      }).catch(err => {
        console.error('用户points字段更新失败', err);
      });
    } else {
      console.log('未找到对应的用户');
    }
  }).catch(err => {
    console.error('根据openid查询用户失败', err);
  });
  },
  changeColor2: function() {
    if (!this.data.isColorChanged2) {
      this.setData({
        boxColor2: '#ff0000',
        isColorChanged2: true
      });
    }
    wx.showToast({
      title:'再想想哦~-5',
      icon:'none',
      duration:1000,
    });
    setTimeout(() => {
      this.setData({
        boxColor2: 'rgb(225,225,225,0.7)',
        isColorChanged: false
      });
    }, 200);
    // 获取用户的openid
  const openid = getApp().globalData.openid;

  // 使用云开发调用数据库API
  const db = wx.cloud.database();
  const userCollection = db.collection('user');

  // 根据openid找到对应的用户
  userCollection.where({
    _openid: openid
  }).get().then(res => {
    // 找到了对应的用户
    if (res.data.length > 0) {
      const user = res.data[0];
      // 更新用户的points字段
      userCollection.doc(user._id).update({
        data: {
          points: user.points-5
        }
      }).then(() => {
        console.log('用户points字段更新成功');
      }).catch(err => {
        console.error('用户points字段更新失败', err);
      });
    } else {
      console.log('未找到对应的用户');
    }
  }).catch(err => {
    console.error('根据openid查询用户失败', err);
  });
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
  }
})