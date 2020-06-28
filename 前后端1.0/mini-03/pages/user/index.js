// pages/user/index.js
Page({

  data: {
    userinfo:{}
  },
  onshow(){
    const userinfo = wx.getStorageSync("userinfo");
    this.setData({userinfo})
  }
})