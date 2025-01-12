// app.js
App({
  onLaunch: function () {
    if (!wx.cloud) {
      console.error('请使用 2.2.3 或以上的基础库以使用云能力');
    } else {

      wx.cloud.init({
        env:'nodio-8go2apw3520fc13b',
        traceUser: true,
      });
      const db = wx.cloud.database();
   const postsCollection = db.collection('posts');
    }

 // 在这里获取用户openid，并存储在全局变量中
 wx.cloud.callFunction({
  name: 'getOpenid',
  complete: res => {
    // console.log('云函数获取到的openid: ', res.result.openid);
    this.globalData.openid = res.result.openid;
  }
});
},
globalData: {
openid: ''
}



  });