这个文件夹主要是展示前后端初期交互成果<br>
=
* mini-03 是前端文件，里面已经初步完成了小程序的雏形，在机器人问答功能模块中负责将客户输入的数据post给后端<br>
* ChatRobot 是后端文件，里面已经完成了当前阶段后端需要做到的和前端交互、调用数据库的数据进行问答等功能
----
前端在index.js里面编辑了用户登录，授权获取信息，之后会将用户图像传递给问答机器人功能页面，用于对机器人提出问题的客户头像<br>
客户在聊天框里输入想问的信息，pages/index/index.js会自动将信息post到后端<br>
此处填入为指定的url<br><br>
![](https://github.com/scuthls/XiaoAn/blob/master/images/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20200628121112.png) <br><br>
ChatRobot文件夹运行的前提是在本地部署了MySQL数据库，利用Navicat在本地进行可视化编辑。<br>
打开Navicat，新建数据库，在ChatRobot文件夹下的settings.py里面修改指定的数据库如下<br><br>
![](https://github.com/scuthls/XiaoAn/blob/master/images/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20200628122017.png) <br><br>
修改相应的数据库名称，cmd打开命令行，迁移数据库，在指定表下导入文件夹中的excel表格数据<br>
运行python manage.py runserver<br>
打开微信开发者工具，登录，授权，在问答界面输入数据库中理财产品名字，小安会自动返回理财产品的有效期<br>
<font color=#DC143C face="微软雅黑">2.0版本计划：当前版本略有不足，小安只能回答客户一条疑问，下一步准备增强机器人问答功能，形成你问我答的界面，满足用户的个性化需求:smirk:。</font>


