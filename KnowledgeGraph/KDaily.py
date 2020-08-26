#_*_ coding utf-8 _*_
#开发团队：17级金融科技汇丰班
#开发人员：DEL
#开发时间:2020/8/2520:41
#文件名称:ts
#开发工具:PyCharm
import tushare as ts
from datetime import *
# data = ts.get_hist_data('600848')

import matplotlib.pyplot as plt
import mpl_finance as mpf
import numpy as np
import pandas as pd
from matplotlib.pylab import date2num


def K(ts_code,type):
    if type == 0 :
        date = '年'
        end_date = datetime.now().strftime('%Y%m%d')
        delta = timedelta(days=365)
        start_date = (datetime.now() - delta).strftime('%Y%m%d')
    elif type == 1:
        date = '月'
        end_date = datetime.now().strftime('%Y%m%d')
        delta = timedelta(days=31)
        start_date = (datetime.now() - delta).strftime('%Y%m%d')
    else:
        date = '周'
        end_date = datetime.now().strftime('%Y%m%d')
        delta = timedelta(days=7)
        start_date = (datetime.now() - delta).strftime('%Y%m%d')
    token="d078bd5a718954f48ee1f41013279afae62d1affd0866b56658cd918"
    ts.set_token(token)
    pro = ts.pro_api()
    data = pro.query('daily', ts_code=ts_code, start_date=start_date, end_date=end_date)
    #删除空行
    data[data['vol']==0]=np.nan
    data=data.dropna()
    #按时间升序排列数据
    data.sort_values(by='trade_date',ascending=True,inplace=True)
    data=data[['trade_date','open','close','high','low']]#这里由于数据太多，仅取前3000行进行绘制
    data.trade_date=pd.to_datetime(data.trade_date)
    #将date转化为特定的时间戳数据
    data.trade_date=data.trade_date.apply(lambda x:date2num(x))
    #将 DataFrame 转为 matrix格式
    data_mat=data.values
    # print(data_mat)
    #绘制图片
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    fig,ax=plt.subplots(figsize=(1200/72,480/72))
    fig.subplots_adjust(bottom=0.1)
    fig.suptitle(r'{0}的{1}K线图'.format(ts_code,date), fontsize=20.00)
    mpf.candlestick_ochl(ax,data_mat,colordown='#53c156', colorup='#ff1717',width=0.3,alpha=1)
    ax.grid(True)
    ax.xaxis_date()
    plt.savefig(r'./{0}的{1}K线图.jpg'.format(ts_code,date))




if __name__ == '__main__':
    ts_code = input("请在股票代码后加上交易所缩写如000001.SZ、600000.SH（仅支持这两个交易所的股票查询）：")   #例如输入000001.SZ
    #画年K线图
    K(ts_code,0)  #0代表画年K线图
    #画月K线图
    K(ts_code,1)   #1代表画月K线图
    #画周K线图
    K(ts_code,2)   #1代表画月K线图