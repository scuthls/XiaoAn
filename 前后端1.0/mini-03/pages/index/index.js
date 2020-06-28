const app = getApp()
 
 
Page({
 
  /**
   * 页面的初始数据
   */
  data: {
    tittle: "Let's Chat",
    syas: [{
        'robot': '我是小安，来跟我聊天吧！'
        
      }
    ],
    headLeft: 'https://pics.images.ac.cn/image/5ef488962a422.html',
    headRight: '',
 
  },
 
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function() {
    let that = this
      wx.getUserInfo({
        success:function(e){
          let header = e.userInfo.avatarUrl
          that.setData({
            headRight:header
          })
        }
      })
 
  },
 
 
  converSation: function(e) {
    let that = this
    var obj = {},
    isay = e.detail.value.says,
    syas=that.data.syas,
    length = syas.length
    
    //console.log(length)
    wx.request({
      url: 'http://localhost:8000/xiaoan/xiaoan/',
      data: {que:isay},
      method: "POST",
      success:function(res){
        console.log(res)
        let tuling = res.data.text;
        obj.robot=tuling;
        obj.isay=isay;
        syas[length] = obj;
        that.setData({
          syas:syas
        })
    }})
    
   
  },
  delectChat:function(){
    let that = this
    that.setData({
      syas:[]
    })
  }
 
})