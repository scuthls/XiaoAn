from py2neo import Graph

class AnswerSearcher:
    def __init__(self):
        self.g = Graph(
            host="39.100.119.153",    #127.0.0.1
            http_port=7474,    #7687
            user="neo4j",   #neo4j
            password="hsbc123456")    #admin
        self.num_limit = 20

    # 执行cypher查询，并返回相应结果
    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls['sqls']:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.g.run(query).data()
                # .data返回的是一个字典组成的列表[{"n.name":"xx", "m.name":"xx", "r.name":"xx(关系名称，如"宜吃")"
                # print("ress:", ress)
                answers += ress
            final_answer = self.answer_prettify(question_type, answers, sqls['question'])
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    # 根据对应的qustion_type，调用相应的回复模板
    def answer_prettify(self, question_type, answers, question):
        final_answer = ''
        if not answers:
            return ''
        if question_type == 'check':
            desc = answers[0]['m.产品名称']
            subject = answers[0]['m.登记编码']
            if desc:
                final_answer = '{0}在“全国银行业理财产品登记系统”的登记编号为：{1}，是银行发行的正规理财产品。'.format(desc,subject)
            else:
                final_answer = '该产品未在理财系统查询到登记编码，无登记编码均不属于正规银行理财产品！'

        elif question_type == 'explanation_attribution':
            name = answers[0]['m.名词']
            desc = ''
            nature = ''
            user = ''
            for i in answers:
                if i['m.定义']:
                    desc = '定义为' + i['m.定义'] + '\n'
                elif i['m.特性']:
                    nature = '特性为' + i['m.特性'] + '\n'
                elif i['m.适用人群']:
                    user = '适用人群为' + i['m.适用人群'] + '\n'
            final_answer = '{0}：\n{1}{2}{3}'.format(name, desc, nature, user)

        elif question_type == 'explanation_noun':
            name = answers[0]['m.名词']
            desc = answers[0]['m.定义']
            final_answer = '{0}的定义为：{1}'.format(name, desc)

        elif question_type == 'notice_attribution':
            print(question_type)
            print(answers)
            name = answers[0]['m.名词']
            desc = ''
            nature = ''
            user = ''
            openform=''
            type=''

            for i in answers:
                try:
                    desc = '定义为' + i['m.定义'] + '\n'
                except:
                    pass
                try:
                    nature = '特性为' + i['m.特性'] + '\n'
                except:
                    pass
                try:
                    user = '适用人群为' + i['m.适用人群']+ '\n'
                except:
                    pass
                try:
                    openform = '开放形态为' + i['m.开放形态'] + '\n'
                except:
                    pass
                try:
                    type = '产品类型为' + i['m.产品类型']
                except:
                    pass

                final_answer += '{0}产品需要注意的事项有:\n{1}{2}{3}{4}{5}'.format(name, desc, nature, user, openform, type)

        elif question_type == 'notice_product':
            name = answers[0]['m.产品名称']
            print(answers)
            desc = ''
            desc1 = ''
            nature = ''
            user = ''
            openform=''
            type=''
            for i in answers:
                try:
                    desc = i['n.名词']
                except:
                    pass
                try:
                    desc1 = '的定义为' + i['n.定义'] + '\n'
                except:
                    pass
                try:
                    nature = '特性为' + i['n.特性'] + '\n'
                except:
                    pass
                try:
                    user = '适用人群为' + i['n.适用人群']+ '\n'
                except:
                    pass
                try:
                    openform = '开放形态为' + i['n.开放形态'] + '\n'
                except:
                    pass
                try:
                    type = '产品类型为' + i['n.产品类型']
                except:
                    pass

            order = 1
            if nature !='':
                nature = '({})'.format(order) + nature
                order = order + 1
            if user !='':
                user = '({})'.format(order) + user
                order = order + 1
            if openform !='':
                openform = '({})'.format(order) + openform
                order = order + 1
            if type !='':
                type = '({})'.format(order) + type
                order = order + 1

            final_answer += '{0}属于{1}的产品，需要注意的事项有：\n{1}{2}{3}{4}{5}{6}'.format(name, desc, desc1,nature, user, openform, type)

        elif question_type == 'call_number':
            name = answers[0]['m.名称']
            subject = ''
            print(answers)
            try:
                subject = answers[0]['m.客服电话']
            except:
                pass
            try:
                subject = answers[1]['m.咨询电话']
            except:
                pass
            final_answer = '{0}的咨询电话为：{1}。'.format(name, subject)

        elif question_type == 'product_desc':
            name = answers[0]['m.产品名称']
            djbm = answers[0]['m.登记编码']
            qxlx = answers[0]['m.期限类型']
            yjbjbz = answers[0]['m.业绩比较基准']
            try:
                fxjg = answers[1]['n.名称']
            except:
                fxjg = ''
            try:
                mjfs = answers[2]['n.名词']
            except:
                mjfs=''
            try:
                yxms = answers[3]['n.名词']
            except:
                yxms=''
            try:
                tzxz = answers[4]['n.名词']
            except:
                tzxz=''
            final_answer = '{0}的简介如下：\n登记编码：{1}\n期限类型：{2}\n业绩比较基准：{3}\n发行机构：{4}\n募集方式：{5}\n运作模式：{6}\n投资性质：{7}'.format(
                name, djbm, qxlx, yjbjbz, fxjg, mjfs, yxms, tzxz)

        elif question_type == 'bank_desc':
            name = answers[0]['m.名称']
            time = answers[0]['m.营业时间']
            call = answers[0]['m.客服电话']
            url = answers[0]['m.官网链接']
            final_answer = '下面为您介绍{0}的相关信息：\n营业时间:{1}\n客服电话:{2}\n官网链接:{3}'.format(name, time, call, url)

        elif question_type == 'url':
            name = answers[0]['m.名称']
            url = answers[0]['m.官网链接']
            final_answer = '{0}的官网链接为：\n{1}'.format(name, url)

        elif question_type == 'area_subbank_addr':
            bank = answers[0]['n.名称']
            areas =[i['m.区域'] for i in answers]
            area = set(areas)
            final_answer += '{0}在{1}的网点分布如下：'.format(bank, area)
            subbank = [i['m.名称'] for i in answers]
            addr = [i['m.具体地址'] for i in answers]
            list_zip = list(zip(subbank, addr,areas))
            for a in set(areas):
                for i in list_zip:
                    if i[2] !=a:
                        continue
                    if i[2] != area:
                        area = i[2]
                        final_answer+= '\n{0}在{1}的网点分布如下：'.format(bank, area)
                    final_answer+= '\n{0},具体地址：{1}'.format(i[0], i[1])


        elif question_type == 'area_subbank':
            bank = answers[0]['n.名称']
            areas =[i['m.区域'] for i in answers]
            area = set(areas)
            subbank = [i['m.名称'] for i in answers]
            final_answer += '{0}在{1}的支行有:'.format(bank, area)
            list_zip = list(zip(subbank, areas))
            for a in set(areas):
                for i in list_zip:
                    if i[1] != a:
                        continue
                    if i[1] != area:
                        area = i[1]
                        final_answer += '\n{0}在{1}的支行有:'.format(bank, area)
                    final_answer += '\n{0}'.format(i[0])

        elif question_type == 'attribution_infos':
            attribution = answers[0]['m.名称']
            subject = [i['n.名词'] for i in answers]
            final_answer = '{0}含有的类别有：{1}'.format(attribution, '、'.join(list(set(subject))))

        elif question_type == 'product_number':
            bank = answers[0]['m.名称']
            print(answers)
            state = [i['n.产品状态'] for i in answers]
            count = [i['count(n)'] for i in answers]
            final_answer += '{0}：'.format(bank)
            list_zip = list(zip(state, count))
            count_all = 0
            for i in list_zip:
                count_all +=i[1]
                final_answer += '\n{0}产品有{1}个，'.format(i[0], i[1])
            final_answer += '\n所有产品总数为{0}个。'.format(count_all)

        elif question_type == 'subbank_number':
            print(answers)
            for i in answers:
                bank = i['n.名称']
                area = i['m.区域']
                count = i['count(r)']
                count_all = 0
                if i == answers[0]:
                    count_all += count
                    final_answer += '{0}\n在{1}共有{2}个网点，\n'.format(bank, area, count)
                elif i == answers[-1]:
                    count_all += count
                    final_answer += '在{0}共有{1}个网点，\n'.format(area, count)
                else:
                    count_all += count
                    final_answer += '在{0}共有{1}个网点，\n'.format(area, count)
            final_answer += '{0}在所查询地区的网点总共有{1}个。'.format(bank, count_all)


        elif question_type == 'product_area':
            name = answers[0]['m.产品名称']
            area = [i['n.名称'] for i in answers]
            final_answer = '{}的销售区域为{}。'.format(name, '、'.join(list(set(area))))

        elif question_type == 'product_attribution':
            print(answers)
            desc = [list(i.values())[-1] for i in answers]
            desc1 = ['' if x == None else x for x in desc]
            final_answer = ';'.join(list(set(desc1))[:self.num_limit])

        elif question_type == 'product_user':
            print(answers)
            name = answers[0]['m.产品名称']
            user = [i['n.适用人群'] for i in answers if i['n.适用人群'] !=None]
            print(user)
            final_answer = '{0}的适用人群为：\n{1}'.format(name, '\n'.join(list(set(user))))

        elif question_type == 'investment_category':
            name = [i['m.名词'] for i in answers]
            desc = [i['n.名词'] for i in answers]
            list_zip = list(zip(name, desc))
            for i in list_zip:
                if i != list_zip[-1]:
                    final_answer += '{0}所属类型为{1}\n'.format(i[0], i[1])
                else:
                    final_answer += '{0}所属类型为{1}\n'.format(i[0], i[1])

        elif question_type == 'if_investment_category':
            name = answers[0]['m.名词']
            desc = answers[0]['n.名词']
            if desc:
                final_answer = '是的！'
            else:
                final_answer = '不对哦！'  # 功能还需改进返回准确答案（下方，未# test）
                try:
                    ansname = answers[1]['m.名词']
                    ansdesc = answers[1]['n.名词']
                    final_answer += '{0}所属类型为{1}。'.format(ansname, ansdesc)
                except:
                    pass

        elif question_type == 'institution_category':
            print(answers)
            name = answers[0]['m.名称']
            desc = answers[0]['n.名词']
            final_answer = '{}所属机构类别为{}。'.format(name, desc)

        elif question_type == 'institution_bank':
            name = answers[0]['m.名称']
            desc = answers[0]['n.名称']
            final_answer = '{}所属总行为{}。'.format(name, desc)

        elif question_type == 'if_category':
            name = answers[0]['m.产品名称']
            desc = answers[0]['p.名词']
            if desc:
                final_answer = '是的！'
            else:
                final_answer = '不对哦！'  # 功能还需改进返回准确答案
                try:
                    ansname = answers[1]['m.产品名称']
                    anstype = answers[1]['p.名词']
                    ansattr = answers[1]['n.名称']
                    final_answer += '{0}的{1}属性的类别为{2}。'.format(ansname, ansattr, anstype)
                except:
                    pass


        elif question_type == 'bank_time':
            bank = answers[0]['m.名称']
            time = answers[0]['m.营业时间']
            final_answer = '{}的营业时间为{}'.format(bank, time)

        elif question_type == 'production_time':
            #name = answers[0]['m.产品名称']
            time = list(answers[0].values())[-1]
            final_answer = '{}'.format(time)

        elif question_type == 'attribution_different':
            name = answers[0]['m.名称']
            desc = answers[0]['m.类别差异']
            final_answer = '{}不同类别之间的差异如下：\n{}'.format(name, desc)

        elif question_type == 'category_different':
            name = answers[0]['m.名词']
            for i in answers:
                name1 = i['m.名词']
                rela = i['r.different']
                name2 = i['n.名词']
                if i != answers[-1]:
                    final_answer += '{}与{}之间的差异为{}。\n'.format(name1, rela, name2)
                else:
                    final_answer += '{}与{}之间的差异为{}。'.format(name1, rela, name2)

        elif question_type == 'other_category':
            name = answers[0]['m.名词']
            desc = [i['n.名词'] for i in answers]
            final_answer = '除了{}，还有：{}'.format(name, '、'.join(list(set(desc))))

        elif question_type == 'category_nature':
            name = answers[0]['m.名词']
            desc = answers[0]['m.特性']
            final_answer = '{}产品的特性为{}'.format(name, desc)

        elif question_type == 'recommend_category':
            final_answer = '为你推荐的产品有：'
            for i in answers:
                desc = i['m.名词']
                if i != answers[-1]:
                    final_answer = + '{1}产品、'.format(desc)
                else:
                    final_answer = + '{1}产品。'.format(desc)


        elif question_type == 'if_recommend_category':
            name = answers[0]['m.名词']
            desc = answers[0]['n.名词']
            if desc:
                final_answer = '是的！'
            else:
                final_answer = '不对哦！'  # 功能还需改进返回准确答案（下方，未# test）
                final_answer += '为你推荐的产品有：'
                try:
                    for i in answers:
                        desc = i['m.名词']
                        if i == answers[0]:
                            pass
                        else:
                            if i != answers[-1]:
                                final_answer = + '{1}产品、'.format(desc)
                            else:
                                final_answer = + '{1}产品。'.format(desc)
                except:
                    pass

        elif question_type == 'if_buy':
            name = answers[0]['m.产品名称']
            state = answers[0]['m.产品状态']
            final_answer = '{}目前状态为{}，'.format(name, state)
            if state == '在售':
                final_answer += '现在可以购买哦！'
            else:
                final_answer += '现在不可以购买哦！'


        return final_answer

if __name__ == '__main__':
    searcher = AnswerSearcher()
    res_sql1 = [{'question_type': 'check',
                'sql': [
                    "MATCH (m:理财产品) where m.登记编码 = 'C3132420000047' or m.产品名称 = 'C3132420000047' return m.产品名称, m.登记编码"]}]
    res_sql = [{'question_type': 'subbank_number',
                'sql': ["MATCH (m:支行)-[r:所属总行]->(n:银行) where (n.名称 = '汇丰银行' or '汇丰银行' in n.别名) and m.区域 CONTAINS '广东' return n.名称,m.区域,count(r)"]}]

    sqls = {'sqls':res_sql,'question':[]}
    print(searcher.search_main(sqls))




