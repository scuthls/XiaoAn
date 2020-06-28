这个文件夹主要是展示前后端初期交互成果<br>
=
* mini-03 是前端文件，里面已经初步完成了小程序的雏形，在机器人问答功能模块中负责将客户输入的数据post给后端<br>
* ChatRobot 是后端文件，里面已经完成了当前阶段后端需要做到的和前端交互、调用数据库的数据进行问答等功能
----
前端在index.js里面编辑了用户登录，授权获取信息，之后会将用户图像传递给问答机器人功能页面，用于对机器人提出问题的客户头像<br>
客户在聊天框里输入想问的信息，pages/index/index.js会自动将信息post到后端<br>
此处填入为指定的url<br>
![](https://github.com/guodongxiaren/ImageCache/raw/master/Logo/foryou.gif) 
