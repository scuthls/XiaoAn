var app = getApp();

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
    headLeft: '',
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
    console.log(e)
    let that = this;
    var obj = {};
    var judge_status = app.globalData.status;
    var end = false;
    var needtoskip=false;

    var isay = e.detail.value.says;
    var syas=that.data.syas;
    var length = syas.length;
    isay = isay.replace(/[\r\n]/g, "");
    
    if(judge_status===0){
      getApp().globalData.text=isay;
      getApp().globalData.status = 1;
    }
    else if(judge_status===1&&isay.includes("不可以")){
      getApp().globalData.status = 2;
      console.log(app.globalData.status);
    }else if(judge_status===1&&isay.includes("可以")){
      end = true;
    }
    else if(judge_status===2&&(isay.includes("1")||isay.includes("2")||isay.includes("3")||isay.includes("4"))){
      if(isay.includes("1")){
        obj.robot=getApp().globalData.answers[0]
        console.log(getApp().globalData.answers[0])
          }
        if(isay.includes("2")){
          obj.robot=getApp().globalData.answers[1]
            }
            if(isay.includes("3")){
              obj.robot=getApp().globalData.answers[2]
                }
                if(isay.includes("4")){
                  obj.robot=getApp().globalData.answers[3]
                    }
      obj.robot= obj.robot+"\n这个答案能解决您的问题吗，能解决请输入可以，不能解决请输入不可以";
      obj.isay=isay;
      syas[length] = obj;
      that.setData({
        syas:syas
        })
      needtoskip=true;
      }

    else if(judge_status===2&&isay.includes("不可以")){
      getApp().globalData.status = 3;
    }else if(judge_status===2&&isay.includes("可以")){
      end = true;
    }else if(judge_status===3){
      getApp().globalData.status = 0;
      needtoskip=true;
    }


    if(end==true){
      getApp().globalData.status=0;
      obj.robot="感谢您的提问";
      obj.isay=isay;
      syas[length] = obj;
      that.setData({
        syas:syas
      })
    }
    else if(end===false&&needtoskip===false){
      console.log(getApp().globalData.text)
      console.log(getApp().globalData.status);
      wx.request({
        url: 'http://127.0.0.1:8000/xiaoan/xiaoan/',
        data: {que:getApp().globalData.text,status:getApp().globalData.status},
        method: "POST",
        success:function(res){
          console.log(res,'----------')
          let tuling = res.data.text;
          getApp().globalData.status=res.data.status;
          if(res.data.answer!=null){
            getApp().globalData.answers=res.data.answer
          }
          obj.robot=tuling;
          if(getApp().globalData.status===2){
            obj.robot=obj.robot+"\n请选择合适的问题编号"
          }else if(getApp().globalData.status!=2){
            obj.robot=obj.robot+"\n这个答案能解决您的问题吗，能解决请输入可以，不能解决请输入不可以"
          }
          obj.isay=isay;
          syas[length] = obj;
          that.setData({
            syas:syas
          })
      }})
     }
    
  },


  delectChat:function(){
    let that = this
    that.setData({
      syas:[]
    })
  }
 
})