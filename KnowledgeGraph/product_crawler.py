import requests
import re
import pandas as pd
import numpy as np

class ProductInfo:
    def find(self,text,投资性质):
        Finacing = []
        登记编码 = re.findall('"cpdjbm":"(.*?)",',text)
        len(登记编码)
        产品ID = re.findall('"cpid":"(.*?)",',text)
        len(产品ID)
        产品名称 = re.findall('"cpms":"(.*?)",',text)
        len(产品名称)
        期限类型 = re.findall('"qxms":"(.*?)",',text)
        len(期限类型)
        业绩比较基准 = re.findall('"yjbjjzlast":"(.*?)",',text)
        len(业绩比较基准)
        发行机构 = re.findall('"fxjgms":"(.*?)",',text)
        len(发行机构)
        发行机构代码 = re.findall('"fxjgdm":"(.*?)",',text)
        len(发行机构代码)
        募集方式 = re.findall('"mjfsms":"(.*?)",',text)
        len(募集方式)
        运作模式 = re.findall('"cpyzmsms":"(.*?)",',text)
        len(运作模式)
        产品类别代码 = re.findall('"tzzlxdm":"(.*?)",',text)   #产品类别代码 一般个人客户 高资产净值客户 私人银行客户专属 机构客户专属 金融同业客户专属
        len(产品类别代码)
        募集币种 = re.findall('"mjbz":"(.*?)",',text)
        len(募集币种)
        风险等级编号 = re.findall('"cpfxdj":"(.*?)",',text)
        len(风险等级编号)
        风险等级 = re.findall('"fxdjms":"(.*?)",',text)
        len(风险等级)
        募集起始日期 = re.findall('"mjqsrq":"(.*?)",',text)
        len(募集起始日期)
        募集结束日期 = re.findall('"mjqsrq":"(.*?)",',text)
        len(募集结束日期)
        产品起始日期 = re.findall('"cpqsrq":"(.*?)",',text)
        len(产品起始日期)
        产品终止日期 = re.findall('"cpyjzzrq":"(.*?)",',text)
        len(产品终止日期)
        产品状态 = re.findall('"cpztms":"(.*?)",',text)
        len(产品状态)
        业务起始日 = re.findall('"kfzqqsr":"(.*?)",',text)
        len(业务起始日)
        业务结束日 = re.findall('"kfzqjsr":"(.*?)",',text)
        len(业务结束日)
        实际天数 = re.findall('"cpqx":"(.*?)",',text)   #实际天数（天）
        len(实际天数)
        初始净值 = re.findall('"csjz":"(.*?)",',text)
        len(初始净值)
        产品净值 = re.findall('"cpjz":"(.*?)",',text)
        len(产品净值)
        累计净值 = re.findall('"ljjz":"(.*?)",',text)
        len(累计净值)
        最近一次兑付收益率 = re.findall('"syl":"(.*?)",',text)     ##最近一次兑付收益率（%）
        len(最近一次兑付收益率)
        收益类型 = re.findall('"cpsylxms":"(.*?)",',text)
        len(收益类型)
        投资资产类型  = re.findall('"tzlxms":"(.*?)",',text)
        len(投资资产类型)
        预期最高收益率 = re.findall('"yjkhzdnsyl":"(.*?)",',text)   #预期最高收益率（%）
        len(预期最高收益率)
        预期最低收益率 = re.findall('"yjkhzdnsyl":"(.*?)",',text)   #预期最低收益率（%）
        len(预期最低收益率)
        产品销售区域 = re.findall('"cpxsqy":"(.*?)",',text)
        len(产品销售区域)
        机构类别 = re.findall('"cpjglb":"(.*?)",',text)    #机构类别 01国有银行 #02股份制银行 #03城商行 #04外资银行 #05农村合作金融机构 #理财子公司 #其他
        len(机构类别)
        认购价格 = re.findall('"qdxsjef":"(.*?)",',text)
        len(认购价格)
        Finacing.append({'登记编码':登记编码,
                     '产品ID':产品ID,
                     '产品名称':产品名称,
                     '期限类型':期限类型,
                     '业绩比较基准':业绩比较基准,
                     '发行机构':发行机构,
                     '发行机构代码':发行机构代码,
                     '募集方式':募集方式,
                     '运作模式':运作模式,
                     '投资性质':投资性质,
                     '产品类别代码':产品类别代码,
                     '募集币种':募集币种,
                     '风险等级编号':风险等级编号,
                     '风险等级':风险等级,
                     '募集起始日期':募集起始日期,
                     '募集结束日期':募集结束日期,
                     '产品起始日期':产品起始日期,
                     '产品终止日期':产品终止日期,
                     '产品状态':产品状态,
                     '业务起始日':业务起始日,
                     '业务结束日':业务结束日,
                     '实际天数':实际天数,
                     '初始净值':初始净值,
                     '产品净值':产品净值,
                     '累计净值':累计净值,
                     '最近一次兑付收益率':最近一次兑付收益率,
                     '收益类型':收益类型,'投资资产类型':投资资产类型,
                     '预期最高收益率':预期最高收益率,
                     '预期最低收益率':预期最低收益率,
                     '产品销售区域':产品销售区域,
                     '机构类别':机构类别,
                     '认购价格':认购价格})
        return Finacing

    def crawler(self,n):
        data = {'pagenum': '{}'.format(n), 'sySearch': '-1'}
        headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                   'Accept-Encoding': 'gzip, deflate, br',
                   'Accept-Language': 'zh-CN,zh;q=0.9',
                   'Connection': 'keep-alive',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                   'Cookie': 'BIGipServerPool_licai_webapp=44373258.31011.0000; JSESSIONID=0000VKXtySvgXPRmzw-UmPtrJAZ:-1; _pk_ses.3.8bc7=*; _pk_id.3.8bc7=2de17a7086d71866.1594808682.5.1598024869.1597999180.',}
        n1 = n
        url = 'https://www.chinawealth.com.cn/LcSolrSearch.go'
        try:
            res = requests.post(url, data=data, headers=headers)
        except:
            self.crawler(n1)
        text = res.text
        投资性质 = []
        try:
            for i in res.json().get('List'):
                try:
                    投资性质.append(i['cptzxzms'])
                except:
                    投资性质.append("NA")
            Finacing = self.find(text,投资性质)
            for data in Finacing:
                CMB_Finance2 = pd.DataFrame(data)
                Finance_Pro = pd.concat([Finance_Pro, CMB_Finance2])
        except:
            self.crawler(n1)


    def process(self):
        Finance_Pro = pd.DataFrame()
        n = 0
        for i in range(1, 90):
            data = {'pagenum': '{}'.format(i), 'sySearch': '-1'}

            headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                       'Accept-Encoding': 'gzip, deflate, br',
                       'Accept-Language': 'zh-CN,zh;q=0.9',
                       'Connection': 'keep-alive',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                       'Cookie': 'BIGipServerPool_licai_webapp=44373258.31011.0000; JSESSIONID=0000VKXtySvgXPRmzw-UmPtrJAZ:-1; _pk_ses.3.8bc7=*; _pk_id.3.8bc7=2de17a7086d71866.1594808682.5.1598024869.1597999180.',}

            url = 'https://www.chinawealth.com.cn/LcSolrSearch.go'
            try:
                res = requests.post(url, data=data, headers=headers)
            except:
                self.crawler(n)

            text = res.text
            投资性质 = []
            try:
                for i in res.json().get('List'):
                    try:
                        投资性质.append(i['cptzxzms'])
                    except:
                        投资性质.append("NA")
                Finacing = self.find(text,投资性质)
                for data in Finacing:
                    CMB_Finance2 = pd.DataFrame(data)
                    Finance_Pro = pd.concat([Finance_Pro, CMB_Finance2])
            except:
                self.crawler(n)
            n = n + 1
            print(n)
        Finance_Pro.drop_duplicates(keep='first', inplace=True)
        Finance_Pro = Finance_Pro.reset_index(drop='true')
        Finance_Pro['产品类别'] = Finance_Pro['产品类别代码'].replace(['03', '05', '01', '02', '04'],
                                                            ['一般个人客户', '高资产净值客户', '私人银行客户专属', '机构客户专属', '金融同业客户专属'])
        Finance_Pro['机构类别'] = Finance_Pro['机构类别'].replace(['01', '02', '03', '04', '05', '06', '10'],
                                                          ['国有银行', '股份制银行', '城商行', '外资银行', '农村合作金融机构', '理财子公司', '其他'])
        areadata = {"": [{'name': '全国', 'code': '000000'}, {'name': '不限', 'code': 'NA'}],
                    "A-F": [{'name': '澳门', 'code': '820000'}, {'name': '安徽', 'code': '340000'},
                            {'name': '北京', 'code': '110000'}, {'name': '重庆', 'code': '500000'},
                            {'name': '大连', 'code': '210200'}, {'name': '福建', 'code': '350000'}],
                    "G": [{'name': '甘肃', 'code': '620000'}, {'name': '广东', 'code': '440000'},
                          {'name': '广西', 'code': '450000'}, {'name': '贵州', 'code': '520000'}],
                    "H": [{'name': '河南', 'code': '410000'}, {'name': '河北', 'code': '130000'},
                          {'name': '湖南', 'code': '430000'}, {'name': '湖北', 'code': '420000'},
                          {'name': '黑龙江', 'code': '230000'}, {'name': '海南', 'code': '460000'}],
                    "J-N": [{'name': '吉林', 'code': '220000'}, {'name': '辽宁', 'code': '210000'},
                            {'name': '江苏', 'code': '320000'}, {'name': '江西', 'code': '360000'},
                            {'name': '宁波', 'code': '330200'}, {'name': '内蒙古', 'code': '150000'},
                            {'name': '宁夏', 'code': '640000'}],
                    "Q-S": [{'name': '上海', 'code': '310000'}, {'name': '山东', 'code': '370000'},
                            {'name': '山西', 'code': '140000'}, {'name': '深圳', 'code': '440300'},
                            {'name': '四川', 'code': '510000'}, {'name': '青岛', 'code': '370200'},
                            {'name': '青海', 'code': '630000'}, {'name': '陕西', 'code': '610000'},
                            {'name': '其他国家或地区', 'code': '900000'}],
                    "T-Z": [{'name': '天津', 'code': '120000'}, {'name': '台湾', 'code': '710000'},
                            {'name': '浙江', 'code': '330000'}, {'name': '厦门', 'code': '350200'},
                            {'name': '云南', 'code': '530000'}, {'name': '新疆', 'code': '650000'},
                            {'name': '香港', 'code': '810000'}, {'name': '西藏', 'code': '540000'}]};
        areadata1 = []
        for i in areadata:
            areadata1.extend(areadata[i])
        areadata_pd = pd.DataFrame(areadata1)
        for i in range(len(areadata_pd)):
            Finance_Pro['产品销售区域'] = Finance_Pro['产品销售区域'].replace(re.compile(areadata_pd.loc[i, 'code']),
                                                                  areadata_pd.loc[i, 'name'])
        Finance_Pro = pd.concat([Finance_Pro[Finance_Pro['产品状态'] == '预售'], Finance_Pro[Finance_Pro['产品状态'] == '在售']])
        Finance_Pro = Finance_Pro.replace(['NA', 'N/A'], np.nan)
        Finance_Pro['产品名称'] = Finance_Pro['产品名称'].apply(lambda x: x.replace('\\', ''))
        Finance_Pro.to_excel('product.xlsx', index=False)
        return

if __name__ == '__main__':
    handler = ProductInfo()
    handler.process()
