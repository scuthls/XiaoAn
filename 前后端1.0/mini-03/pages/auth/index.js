// pages/auth/index.js
Page({
  //获取用户信息
  handleGetUserInfo(e){
    //获取用户信息
    const { encrytedData, rawData, iv, signature } = e.detail;
    //获取小程序登陆成功后的code
    wx.login({
      timeout: 10000,
      success: (result) => {
        const {code} = result;
      }
    });
  }
})