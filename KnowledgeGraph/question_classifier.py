import ahocorasick
import re
import jieba
from fuzzywuzzy import process


product_dict = ''

class QuestionClassifier:
    def __init__(self):
        # 加载特征词，把txt文件加载成一个大list
        self.product_wds = [i.strip() for i in open('./dict/product.txt', encoding="utf-8") if i.strip()]
        self.bank_wds = [i.strip() for i in open('./dict/bank.txt', encoding="utf-8") if i.strip()]
        self.area_wds = [i.strip() for i in open('./dict/area.txt', encoding="utf-8") if i.strip()]
        self.subbank_wds = [i.strip() for i in open('./dict/subbank.txt', encoding="utf-8") if i.strip()]
        self.investment_wds = [i.strip() for i in open('./dict/investment.txt', encoding="utf-8") if i.strip()]
        self.investment_type_wds = [i.strip() for i in open('./dict/investment_type.txt', encoding="utf-8") if
                                    i.strip()]
        self.operation_wds = [i.strip() for i in open('./dict/operation.txt', encoding="utf-8") if
                                    i.strip()]
        self.raise_way_wds = [i.strip() for i in open('./dict/raise_way.txt', encoding="utf-8") if i.strip()]
        self.risk_level_wds = [i.strip() for i in open('./dict/risk_level.txt', encoding="utf-8") if i.strip()]
        self.investment_nature_wds = [i.strip() for i in open('./dict/investment_nature.txt', encoding="utf-8") if
                                      i.strip()]
        self.income_type_wds = [i.strip() for i in open('./dict/income_type.txt', encoding="utf-8") if i.strip()]
        self.institution_category_wds = [i.strip() for i in open('./dict/institution_category.txt', encoding="utf-8") if
                                         i.strip()]
        self.institution_wds = [i.strip() for i in open('./dict/institution.txt', encoding="utf-8") if i.strip()]
        self.proper_noun_wds = [i.strip() for i in open('./dict/proper_noun.txt', encoding="utf-8") if i.strip()]
        self.open_form_wds = [i.strip() for i in open('./dict/open_form.txt', encoding="utf-8") if i.strip()]
        self.type_wds = [i.strip() for i in open('./dict/type.txt', encoding="utf-8") if i.strip()]
        self.attribution_wds = [i.strip() for i in open('./dict/attribution.txt', encoding="utf-8") if i.strip()]
        self.category_wds = [i.strip() for i in open('./dict/category.txt', encoding="utf-8") if i.strip()]
        self.user_wds = [i.strip() for i in open('./dict/user.txt', encoding="utf-8") if i.strip()]

        # 把上面所有的放在一起构造一个领域字典
        self.region_words = set(
            self.product_wds + self.bank_wds + self.area_wds + self.subbank_wds + self.investment_wds + self.investment_type_wds + self.operation_wds + self.raise_way_wds + self.risk_level_wds + self.investment_nature_wds + self.income_type_wds + self.institution_category_wds + self.institution_wds + self.proper_noun_wds + self.open_form_wds + self.type_wds+self.attribution_wds+self.category_wds+self.user_wds)

        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))

        # 构建词典 类似   {'骶骨裂': ['symptom'], '豆腐烧胡萝卜': ['food'], '喉角化症': ['disease']}
        self.wdtype_dict = self.build_wdtype_dict()

        # print("wdtype_dict", self.wdtype_dict)
        # 问句疑问词、关键词
        self.explanation_qwds = ['理财知识', '知识', '名词', '词', '内容', '意思', '理解', '定义', '含义', '解释', '科普', '普及',
                                 '怎么理解', '怎样理解', '咋样理解', '咋理解', '明白', '了解', '知道', '是什么']  # 询问理财知识的解释或者产品介绍

        self.product_qwds = ['产品', '查询', '询问', '查找', '你怎么看', '分析', '看下', '看一下', '怎样的', '评价']

        self.notice_qwds = ['注意', '坑', '事项', '关注', '怎么看', '怎样看', '咋样看', '咋看', '看什么', '看啥']  # 询问购买理财产品需要注意事项

        self.check_qwds = ['靠谱', '合规', '有效', '合法', '真', '假', '辨别', '识别', '鉴别']  # 根据产品名称或者登记编号识别产品是否合规

        self.recommend_qwds = ['适合', '哪一种', '哪种', '哪一款', '哪款', '合适', '推荐']  # 根据风险偏好 推荐适合的产品类型、性质等

        self.belong_qwds = ['属于哪', '属于什么', '所属', '归属', '归于', '是什么', '是哪','是']  # 询问产品属性

        self.if_qwds = ['是', '为']  # 判断

        self.when_qwds = ['什么时候', '什么时间', '哪时', '哪个时间', '关闭', '结束', '截止', '停止', '开始', '起', '时候卖', '时候执行', '生效', '多久',
                          '多长时间', '多少时间', '几天', '几年', '多少天', '多少年', '期限', '有效期', '时长','营业时间','时间']

        self.state_qwds = ['还可以买', '还赶得上', '在售', '卖完', '售完', '能买', '还可以购买','还能购买','还可购买','还卖','还有卖','现在可以买','现在能买','现在卖','现在可以购买','现在可购买','现在可买']  # 询问产品状态

        self.how_qwds = ['怎么可', '怎样可', '咋样可', '咋可', '如何可', '怎么才', '怎样才', '咋样才', '咋才', '如何才', '要怎么', '要怎样', '要咋样', '要咋',
                         '要如何',
                         '什么方法', '什么方式', '什么途径', '什么法', '什么法子', '哪里', '去哪', '咋样可', '如何可']

        self.nature_qwds = ['特征', '特性', '特点', '特色', '性质']

        self.different_qwds = ['不同', '区别', '差别', '不一样']

        self.other_qwds = ['还有', '其他', '其它', '相关', '有关', '除了']

        self.perform_qwds = ['表现', '形势', '发展', '态势', '趋势']  # 询问投资资产表现

        self.new_qwds = ['讯息', '信息', '新闻', '咨询']

        self.who_qwds = ['对象', '哪些人', '什么人', '谁', '客户','群体','人群']

        self.rule_qwds = ['规定', '规则', '规章', '法规', '法律', '规范']

        self.where_qwds = ['位置', '分布', '地址', '哪里', '在哪', '地方', '地区','区域']

        self.call_qwds = ['联系', '电话', '号码']

        self.url_qwds = ['网站', '官网', '网址', '网页', '链接']

        self.have_qwds = ['有哪些', '哪些是', '哪几种', '哪几类', '分为', '包含', '拥有']

        self.howmany_qwds = ['多少', '几个', '几类', '几种','数量','数目','个数','总数']

        #self.high_item_qwds = ['最高', '几个', '几类', '几种']

        #self.low_item_qwds = ['', '', '']

        print('model init finished ......')

        return

    # 分类主函数
    def classify(self, question):
        data = {}
        data['question'] = question
        finance_dict = self.check_finance(question)
        # medical_dict: {'净值型': ['产品类型',属性类别'], '非净值型': ['产品类型',属性类别']}
        # print(medical_dict)

        if not finance_dict:  # 如果当前问题没有查到实体，就查看之前问题有没有保存实体
            if product_dict != '':
                finance_dict = product_dict
            else:
                return {}

        data['args'] = finance_dict
        # 收集问句当中所涉及到的实体类型
        types = []
        for type_ in finance_dict.values():
            types += type_
        question_type = 'others'

        question_types = []

        print(types)

        ## 简单的判断问句中是否有字典里的词语
        # 检查产品合法问题     #C1080919000230靠谱吗？
        if self.check_words(self.check_qwds, question) and ('product' in types):
            question_type = 'check'
            question_types.append(question_type)

        # 名词解释问题      #你可以解释一下净值型产品是什么吗？
        if self.check_words(self.explanation_qwds, question) and ('attribution' in types):
            question_type = 'explanation_attribution'
            question_types.append(question_type)
        elif self.check_words(self.explanation_qwds, question) and ('proper_noun' in types):
            question_type = 'explanation_noun'
            question_types.append(question_type)
        elif self.check_words(self.explanation_qwds, question):
            question_type = 'explanation_common'
            question_types.append(question_type)

        # 询问产品注意事项问题   #针对与购买产品的注意事项   针对与某一属性产品的注意事项   #C1080919000230需要注意什么？#封闭式净值型产品需要注意什么？ √
        if self.check_words(self.notice_qwds, question) and ('proper_noun' in types):
            question_type = 'notice_attribution'
            question_types.append(question_type)
        elif self.check_words(self.notice_qwds, question) and ('product' in types):
            question_type = 'notice_product'
            question_types.append(question_type)
        elif self.check_words(self.notice_qwds, question):
            question_type = 'notice_common'
            question_types.append(question_type)

        # 询问银行电话   #汇丰银行的电话？    √
        if self.check_words(self.call_qwds, question) and ('bank' in types or 'subbank' in types):
            question_type = 'call_number'
            question_types.append(question_type)

        # 介绍产品概要信息    #你能给我介绍一下C1080919000230吗？ √
        if self.check_words(self.product_qwds, question) and ('product' in types):
            question_type = 'product_desc'
            question_types.append(question_type)

        # 询问银行官网链接 #汇丰银行的官网通道？   √
        if self.check_words(self.url_qwds, question) and ('bank' in types):
            question_type = 'url'
            question_types.append(question_type)

        # 询问某区域某银行的支行  “广东哪里有汇丰银行” √
        if self.check_words(self.where_qwds, question) and ('bank' in types and 'area' in types):
            question_type = 'area_subbank_addr'
            question_types.append(question_type)

            # 询问银行在某地区的支行信息  “汇丰银行在广东有哪些支行/网点”√    #不能问 汇丰 有多少
        if self.check_words(self.have_qwds, question) and ('bank' in types and 'area' in types):
            question_type = 'area_subbank'
            question_types.append(question_type)

        # 询问理财产品某属性有哪些类  #募集方式有哪几种？     #未test
        if self.check_words(self.have_qwds, question) and ('attribution' in types):
            question_type = 'attribution_infos'
            question_types.append(question_type)

        # 询问某银行理财产品的数量 返回在售、预售、续存的数量以及总数 #汇丰银行理财产品的总数？ √
        if self.check_words(self.howmany_qwds, question) and ('bank' in types and 'area' not in types):
            question_type = 'product_number'
            question_types.append(question_type)

        # 询问某银行在某地区的总数   #汇丰银行在广东的总数？√
        if self.check_words(self.howmany_qwds, question) and ('bank' in types and 'area' in types):
            question_type = 'subbank_number'
            question_types.append(question_type)

        # 询问某理财产品销售区域   #C3132420000047的销售地点在哪？√
        if self.check_words(self.where_qwds, question) and ('product' in types):
            question_type = 'product_area'
            question_types.append(question_type)

        # 询问产品的某属性所属类别    #C3132420000047的募集方式是   #C3132420000047的业绩比较基准是 √     单独列出来的属性查询未检验
        if self.check_words(self.belong_qwds, question) and ('product' in types and 'attribution' in types):
            question_type = 'product_attribution'
            question_types.append(question_type)

        # 询问某产品的面向的用户  #C3132420000047销售对象是？ √
        if self.check_words(self.who_qwds, question) and ('product' in types):
            question_type = 'product_user'
            question_types.append(question_type)

        # 询问某投资资产所属资产类别     #未test
        if self.check_words(self.belong_qwds, question) and ('investment' in types):
            question_type = 'investment_category'
            question_types.append(question_type)

        # 确认某投资资产是否属于某资产类别    #未test
        if self.check_words(self.if_qwds, question) and ('investment' in types and 'investment_type' in types):
            question_type = 'if_investment_category'
            question_types.append(question_type)

        # 询问某发行机构所属的机构类别     询问某发行机构所属的总行   #盛京银行股份有限公司所属机构类别    #未test  由于之前未创建联系
        if self.check_words(self.belong_qwds, question) and ('institution' in types):
            if '类' in question or '机构' in question or '种' in question:
                question_type = 'institution_category'
            elif '行' in question:
                question_type = 'institution_bank'
            question_types.append(question_type)

        # 判断某产品的某属性是否为某类别      #C1088220000926的募集方式是否为公募？   #未test
        if self.check_words(self.if_qwds, question) and ('product' in types and 'proper_noun' in types):
            question_type = 'if_category'
            question_types.append(question_type)

        # 判断某银行营业时间 #汇丰银行的营业时间是？ √
        if self.check_words(self.when_qwds, question) and ('bank' in types):
            question_type = 'bank_time'
            question_types.append(question_type)

        # 询问某产品的时间属性   #C3132420000047的募集起始时间？ √
        if self.check_words(self.when_qwds, question) and ('product' in types and 'attribution' in types):
            question_type = 'production_time'
            question_types.append(question_type)

        # 询问某属性的不同类之间的差别  问：“某个属性的不同类别之间的差异，” “某个类别和其他类别的差异”    #未test
        if self.check_words(self.different_qwds, question) and ('proper_noun' in types):
            question_type = 'category_different'
            question_types.append(question_type)
        elif self.check_words(self.different_qwds, question) and ('attribution' in types and 'proper_noun' not in types):
            question_type = 'attribution_different'
            question_types.append(question_type)

        # 询问某属性的下的其他类别      #请问除了净值型还有什么类型？   #未test
        if self.check_words(self.other_qwds, question) and ('proper_noun' in types):
            question_type = 'other_category'
            question_types.append(question_type)

        # 询问某类型的特性    #净值型产品的特性是什么？   √
        if self.check_words(self.nature_qwds, question) and ('proper_noun' in types):
            question_type = 'category_nature'
            question_types.append(question_type)

        # 判断某类产品是否适合某类人群    #高风险偏好人群适合净值型产品吗？     #未test
        if self.check_words(self.recommend_qwds, question)  and ('user' in types) and ('proper_noun' in types):
            question_type = 'if_recommend_category'
            question_types.append(question_type)
        # 寻求产品类型推荐    具体产品不做推荐哦！     #哪一种产品适合高风险偏好的我呢？   #未test
        elif self.check_words(self.recommend_qwds, question) and ('user' in types):
            question_type = 'recommend_category'
            question_types.append(question_type)

        # 询问某产品现在可以购买否       #C3132420000047现在可以购买吗?   √
        if self.check_words(self.state_qwds, question) and ('product' in types):
            question_type = 'if_buy'
            question_types.append(question_type)

        # 若没有查到相关的外部查询信息，那么则将该产品的描述信息返回
        if question_types == [] and ('product' in types) and ('attribution' not in types):
            question_types = ['product_desc']

        # 若没有查到相关的外部查询信息，那么则将该属性的描述信息返回
        if question_types == [] and ('attribution' in types) and ('product' not in types) and ('proper_noun' not in types):
            question_types = ['attribution_infos']

        # 若没有查到相关的外部查询信息，那么则将该类别的描述信息返回
        if question_types == [] and ('proper_noun' in types):
            question_types = ['explanation_noun']

        # 若没有查到相关的外部查询信息，那么则将该银行的描述信息返回
        if question_types == [] and ('bank' in types):
            question_types = ['bank_desc']

        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types

        return data

    # 构造actree，加速过滤
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree


    #模糊匹配
    def finders(self,user_input):
        self.region_words
        sugge = []
        pat = '.*'.join(user_input)
        regex = re.compile(pat)
        for item in data:
            match = regex.search(item)
            if match:
                sugge.append(item)
        return sugge



    # 构造词对应的类型
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.product_wds:
                wd_dict[wd].append('product')
            if wd in self.bank_wds:
                wd_dict[wd].append('bank')
            if wd in self.area_wds:
                wd_dict[wd].append('area')
            if wd in self.subbank_wds:
                wd_dict[wd].append('subbank')
            if wd in self.investment_wds:
                wd_dict[wd].append('investment')
            if wd in self.investment_type_wds:
                wd_dict[wd].append('investment_type')
            if wd in self.operation_wds:
                wd_dict[wd].append('operation')
            if wd in self.raise_way_wds:
                wd_dict[wd].append('raise_way')
            if wd in self.risk_level_wds:
                wd_dict[wd].append('risk_level')
            if wd in self.investment_nature_wds:
                wd_dict[wd].append('investment_nature')
            if wd in self.income_type_wds:
                wd_dict[wd].append('income_type')
            if wd in self.institution_category_wds:
                wd_dict[wd].append('institution_category')
            if wd in self.institution_wds:
                wd_dict[wd].append('institution')
            if wd in self.proper_noun_wds:
                wd_dict[wd].append('proper_noun')
            if wd in self.open_form_wds:
                wd_dict[wd].append('open_form')
            if wd in self.type_wds:
                wd_dict[wd].append('type')
            if wd in self.attribution_wds:
                wd_dict[wd].append('attribution')
            if wd in self.category_wds:
                wd_dict[wd].append('category')
            if wd in self.user_wds:
                wd_dict[wd].append('user')
        return wd_dict

    # 问句过滤
    def check_finance(self, question):
        region_wds = []
        # iter方法返回一个元组形如(1, (5822, '净值型'))
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)

        '''
        #模糊匹配，提取出句子中对应的实体
        ls = jieba.lcut(question)   #精确模式
        for i in ls:
            if len(i) == 1:
                continue
            choices = self.region_words
            pro = process.extract(i, choices)
            for p in pro:
                if p[1] != 0:
                    wd1=p[0]
                    region_wds.append(wd1)
        '''

        # 这一步操作用来去掉，例如["净值", "净值型"]，因为想要的明显是长的那个词，所以把属于子集的词给去掉。
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i: self.wdtype_dict.get(i) for i in final_wds}
        global product_dict
        if final_dict:  # 如果当前的问题里有新的实体，则更新
            product_dict = final_dict
        # final_dict形如：{'净值型': ['属性类别']}
        return final_dict

        '''
        stop_wds = []
        for wd1 in region_wds:
            stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i: self.wdtype_dict.get(i) for i in final_wds}
        global diseases_dict
        if final_dict:  # 如果当前的问题里有新的实体，则更新
            diseases_dict = final_dict
        # final_dict形如：{'乙肝': ['disease']}
        return final_dict
        '''

    # 基于特征词进行分类
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                print(wd)
                return True
        return False

if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)