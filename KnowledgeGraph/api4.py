from KDaily import *

if __name__ == '__main__':
    ts_code = input("请在股票代码后加上交易所缩写如000001.SZ、600000.SH（仅支持这两个交易所的股票查询）：")   #例如输入000001.SZ
    #画年K线图
    K(ts_code,0)  #0代表画年K线图
    #画月K线图
    K(ts_code,1)   #1代表画月K线图
    #画周K线图
    K(ts_code,2)   #1代表画月K线图