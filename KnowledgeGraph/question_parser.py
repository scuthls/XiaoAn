
class QuestionPaser:

    # 构建实体节点
    def build_entitydict(self, args):
        entity_dict = {}
        # dict.items返回的是可遍历的(键-值)元组数组
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    # 解析主函数
    # res_classifer: {'args': {'乙肝': ['disease']}, 'question_types': ['disease_cureway'], 'question' : []}
    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        # entity_dict: {'food': ['鸡蛋']}
        # print("entity_dict:", entity_dict)
        question_types = res_classify['question_types']
        res_sql = {}
        res_sql['question'] = res_classify['question']
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            if question_type == 'check':
                sql = self.sql_transfer(question_type, [entity_dict.get('product')])

            elif question_type == 'explanation_attribution':
                sql = self.sql_transfer(question_type, [entity_dict.get('attribution')])

            elif question_type == 'explanation_noun':
                sql = self.sql_transfer(question_type, [entity_dict.get('proper_noun')])

            elif question_type == 'explanation_common':
                sql = []

            elif question_type == 'notice_attribution':
                sql = self.sql_transfer(question_type, [entity_dict.get('proper_noun')])

            elif question_type == 'notice_product':
                sql = self.sql_transfer(question_type, [entity_dict.get('product')])

            elif question_type == 'notice_common':
                sql = []

            elif question_type == 'call_number':
                if 'bank' in entity_dict:
                    entity = entity_dict.get('bank')
                else:
                    entity = entity_dict.get('subbank')
                sql = self.sql_transfer('call_number', [entity])

            elif question_type == 'product_desc':
                sql = self.sql_transfer(question_type, [entity_dict.get('product')])

            elif question_type == 'bank_desc':
                sql = self.sql_transfer(question_type, [entity_dict.get('bank')])

            elif question_type == 'url':
                sql = self.sql_transfer(question_type, [entity_dict.get('bank')])

            elif question_type == 'area_subbank_addr':
                sql = self.sql_transfer(question_type, [entity_dict.get('area'), entity_dict.get('bank')])

            elif question_type == 'area_subbank':
                sql = self.sql_transfer(question_type, [entity_dict.get('area'), entity_dict.get('bank')])

            elif question_type == 'attribution_infos':
                sql = self.sql_transfer(question_type, [entity_dict.get('attribution')])

            elif question_type == 'product_number':
                sql = self.sql_transfer(question_type, [entity_dict.get('bank')])

            elif question_type == 'subbank_number':
                sql = self.sql_transfer(question_type, [entity_dict.get('area'), entity_dict.get('bank')])

            elif question_type == 'product_area':
                sql = self.sql_transfer(question_type, [entity_dict.get('product')])

            elif question_type == 'product_attribution':
                sql = self.sql_transfer(question_type, [entity_dict.get('product'), entity_dict.get('attribution')])

            elif question_type == 'product_user':
                sql = self.sql_transfer(question_type, [entity_dict.get('product')])

            elif question_type == 'investment_category':
                sql = self.sql_transfer(question_type, [entity_dict.get('investment')])

            elif question_type == 'if_investment_category':
                sql = self.sql_transfer(question_type,
                                        [entity_dict.get('investment'), entity_dict.get('investment_type')])

            elif question_type == 'institution_category':
                sql = self.sql_transfer(question_type, [entity_dict.get('institution')])

            elif question_type == 'institution_bank':
                sql = self.sql_transfer(question_type, [entity_dict.get('institution')])

            elif question_type == 'if_category':
                sql = self.sql_transfer(question_type, [entity_dict.get('product'), entity_dict.get('proper_noun')])

            elif question_type == 'bank_time':
                sql = self.sql_transfer(question_type, [entity_dict.get('bank')])

            elif question_type == 'production_time':
                sql = self.sql_transfer(question_type, [entity_dict.get('product'), entity_dict.get('attribution')])

            elif question_type == 'attribution_different':
                sql = self.sql_transfer(question_type, [entity_dict.get('attribution')])

            elif question_type == 'category_different':
                sql = self.sql_transfer(question_type, [entity_dict.get('proper_noun')])

            elif question_type == 'other_category':
                sql = self.sql_transfer(question_type, [entity_dict.get('proper_noun')])

            elif question_type == 'category_nature':
                sql = self.sql_transfer(question_type, [entity_dict.get('proper_noun')])

            elif question_type == 'recommend_category':
                sql = self.sql_transfer(question_type, [entity_dict.get('user')])

            elif question_type == 'if_recommend_category':
                sql = self.sql_transfer(question_type, [entity_dict.get('user')])

            elif question_type == 'if_buy':
                sql = self.sql_transfer(question_type, [entity_dict.get('product')])

            if sql:
                sql_['sql'] = sql
                sqls.append(sql_)
        res_sql['sqls'] = sqls

        return res_sql

    # 针对不同的问题，分开进行处理
    def sql_transfer(self, question_type, entities):
        if not entities[0]:
            return []

        if len(entities[0]) > 1 and len(entities[1]) > 1:  # 说明问了不止一类问题
            return []  # 问的太多了

        # 查询语句
        sql = []
        # 检查产品合法问题
        if question_type == 'check':
            sql = ["MATCH (m:理财产品) where m.登记编码 = '{0}' or m.产品名称 = '{0}' return m.产品名称, m.登记编码".format(i) for i in
                   entities[0]]

        # 名词解释问题
        elif question_type == 'explanation_attribution':
            sql += ["MATCH (m:机构类别) where m.名词 = '{0}' return m.名词, m.定义".format(i) for i in entities[0]]
            sql += ["MATCH (m:投资资产类型) where m.名词 = '{0}' return m.名词, m.定义".format(i) for i in entities[0]]
            sql += ["MATCH (m:募集方式) where m.名词 = '{0}' return m.名词, m.定义, m.特性, m.适用人群".format(i) for i in entities[0]]
            sql += ["MATCH (m:开放形态) where m.名词 = '{0}' return m.名词, m.定义, m.特性, m.适用人群".format(i) for i in entities[0]]
            sql += ["MATCH (m:产品类型) where m.名词 = '{0}' return m.名词, m.定义, m.特性, m.适用人群".format(i) for i in entities[0]]
            sql += ["MATCH (m:投资性质) where m.名词 = '{0}' return m.名词, m.定义, m.特性, m.适用人群".format(i) for i in entities[0]]
            sql += ["MATCH (m:收益类型) where m.名词 = '{0}' return m.名词, m.特性, m.适用人群".format(i) for i in entities[0]]
            sql += ["MATCH (m:运作模式) where m.名词 = '{0}' return m.名词, m.定义".format(i) for i in entities[0]]
            sql += ["MATCH (m:管理主体) where m.名词 = '{0}' return m.名词, m.定义, m.特性".format(i) for i in entities[0]]
            sql += ["MATCH (m:风险等级) where m.名词 = '{0}' return m.名词, m.特性".format(i) for i in entities[0]]

        # 名词解释问题
        elif question_type == 'explanation_noun':
            sql += ["MATCH (m:费用) where m.名词 = '{0}' return m.名词, m.定义".format(i) for i in entities[0]]
            sql += ["MATCH (m:产品要素) where m.名词 = '{0}' return m.名词, m.定义".format(i) for i in entities[0]]
            sql += ["MATCH (m:资产运作) where m.名词 = '{0}' return m.名词, m.定义".format(i) for i in entities[0]]
            sql += ["MATCH (m:信息披露) where m.名词 = '{0}' return m.名词, m.定义".format(i) for i in entities[0]]
            sql += ["MATCH (m:流动性安排) where m.名词 = '{0}' return m.名词, m.定义".format(i) for i in entities[0]]
            sql += ["MATCH (m:投资资产) where m.名词 = '{0}' return m.名词, m.定义".format(i) for i in entities[0]]
            sql += ["MATCH (m:风险) where m.名词 = '{0}' return m.名词, m.定义".format(i) for i in entities[0]]

        # 询问产品注意事项问题   针对与购买产品的注意事项  针对与某一属性产品的注意事项
        elif question_type == 'notice_attribution':
            sql = ["MATCH (m:属性类别) where m.名词 = '{0}' or '{0}' in m.别名 return m.名词, m.注意事项".format(i) for i in
                   entities[0] for j in entities[0]]

        elif question_type == 'notice_product':
            sql = [
                "MATCH (m:理财产品)-[r:]->(n:属性类别) where m.产品名称 = '{0}' or m.登记编码 = '{0}' return m.产品名称, n.名词, n.注意事项".format(
                    i) for i in entities[0]]

        # 询问银行电话
        elif question_type == 'call_number':
            sql += ["MATCH (m:银行) where m.名称 = '{0}' return m.名称, m.客服电话".format(i) for i in entities[0]]
            sql += ["MATCH (m:支行) where m.名称 = '{0}' return m.名称, m.咨询电话".format(i) for i in entities[0]]

        # 介绍产品概要信息
        elif question_type == 'product_desc':
            sql = [
                "MATCH (m:理财产品) where m.产品名称 = '{0}' or m.登记编码 = '{0}' return m.产品名称, m.登记编码, m.期限类型, m.业绩比较标准, m.发行机构, m.募集方式, m.运作模式, m.投资性质".format(
                    i) for i in entities[0]]

        # 介绍银行概要信息
        elif question_type == 'bank_desc':
            sql = ["MATCH (m:银行) where m.名称 = '{0}' or '{0}' in m.别名 return m.名称, m.营业时间, m.客服电话, m.官网链接".format(i) for
                   i in entities[0]]

        # 询问银行官网链接
        elif question_type == 'url':
            sql = ["MATCH (m:银行) where m.名称 = '{0}' or '{0}' in m.别名 return m.名称, m.官网链接".format(i) for i in
                   entities[0]]

        # 询问某区域某银行的支行  “广东哪里有汇丰银行”
        elif question_type == 'area_subbank_addr':
            sql = [
                "MATCH (m:支行)-[r:所属总行]->(n:银行) where n.名称 = '{1}' or '{1}' in n.别名 and m.区域 = '{0}' return n.银行, m.区域, m.名称, m.具体地址 ".format(
                    i, j) for i in entities[0] for j in entities[1]]

        # 询问银行在某地区的支行信息  “汇丰在广东有哪些支行/网点”
        elif question_type == 'area_subbank':
            sql = [
                "MATCH (m:支行)-[r:所属总行]->(n:银行) where n.名称 = '{1}' or '{1}' in n.别名 and m.区域 = '{0}' return n.名称, m.区域, m.名称".format(
                    i, j) for i in entities[0] for j in entities[1]]

        # 询问理财产品某属性有哪些类
        elif question_type == 'attribution_infos':
            sql = ["MATCH (m:产品属性)-[r:含有类别]->(n:属性类别) where m.名称 = '{0}' return m.名称, n.名词".format(i) for i in
                   entities[0]]

        # 询问某银行理财产品的数量 返回在售、预售、续存的数量以及总数
        elif question_type == 'product_number':
            # sql语句会返回不同产品状态的结果
            sql = ["MATCH (m:银行) where (m.名称 = '{0}' or '{0}' in m.别名) return m.名称, count(m), m.产品状态".format(i) for i in
                   entities[0]]

        # 询问某银行在某地区的总数
        elif question_type == 'subbank_number':
            sql = [
                "MATCH (m:支行)-[r:所属总行]->(n:银行) where (n.名称 = '{1}' or '{1}' in n.别名) and m.区域 = '{0}' return n.名称,m.区域,count(r)".format(
                    i, j) for i in entities[0] for j in entities[1]]

        # 询问某理财产品销售区域
        elif question_type == 'product_area':
            sql = [
                "MATCH (m:理财产品)-[r:销售地区]->(n:区域) where (m.产品名称 = '{1}' or m.登记编码 = '{1}') return m.产品名称, n.名称".format(
                    i, j) for i in entities[0] for j in entities[1]]

        # 询问产品的某属性所属类别
        elif question_type == 'product_attribution':
            sql += [
                "MATCH (m:理财产品)-[]->(n:属性类别)-[]->(p:产品属性) where (m.产品名称 = '{0}' or m.登记编码 = '{0}') and (p.名称 = '{1}' or '{1}' in p.别名) return m.产品名称, p.名称, n.名词".format(
                    i, j) for i in entities[0] for j in entities[1]]
            sql += ["MATCH (m:理财产品) where m.产品名称 = '{0}' or m.登记编码 = '{0}' return m.产品名称, m.{1}".format(i, j) for i in
                    entities[0] for j in entities[1]]

        # 询问某产品的面向的用户
        elif question_type == 'product_user':
            sql = ["MATCH (m:理财产品)-[r:]->(n:) where (m.产品名称 = '{0}' or m.登记编码 = '{0}')  return m.产品名称, n.适用群体".format(i)
                   for i in entities[0]]

        # 询问某投资资产所属资产类别
        elif question_type == 'investment_category':
            sql = ["MATCH (m:投资资产)-[]->(n:投资资产类型) where (m.名称 = '{0}' or '{0}' in m.别名) return m.名称, n.名词  ".format(i)
                   for i in entities[0]]

        # 确认某投资资产是否属于某资产类别
        elif question_type == 'if_investment_category':
            sql = [
                "MATCH (m:投资资产)-[]->(n:投资资产类型) where (m.名称 = '{0}' or '{0}' in m.别名) and n.名词='{1}' return m.名称, n.名词".format(
                    i, j) for i in entities[0] for j in entities[1]]

        # 询问某发行机构所属的机构类别
        elif question_type == 'institution_category':
            sql = ["MATCH (m:发行机构)-[]->(n:机构类别) where m.名称 = '{0}' return m.名称, n.名词".format(i) for i in entities[0]]

        # 询问某发行机构所属的总行
        elif question_type == 'institution_bank':
            sql = ["MATCH (m:发行机构)-[]->(n:银行) where m.名称 = '{0}' return m.名称, n.名称".format(i) for i in entities[0]]

        # 判断某产品的某属性是否为某类别
        elif question_type == 'if_category':
            sql = [
                "MATCH (m:理财产品)-[]->(p:属性类别)-[]->(n:产品属性) where (m.产品名称 = '{0}' or m.登记编码 = '{0}') and (p.名称 = '{1}' or '{1}' in p.别名) return m.产品名称, p.名词, n.名称".format(
                    i, j) for i in entities[0] for j in entities[1]]

        # 询问某银行营业时间
        elif question_type == 'bank_time':
            sql = ["MATCH (m:银行) where m.名称 = '{0}' or '{0}' in m.别名  return m.名称, m.营业时间".format(i) for i in
                   entities[0]]

        # 询问某产品的时间属性
        elif question_type == 'production_time':
            sql = ["MATCH (m:理财产品) where m.产品名称 = '{0}' or m.登记编码 ='{0}' return m.产品名称, m.'{1}'".format(i,j) for i in
                   entities[0] for j in entities[1]]

        # 询问某属性的不同类之间的差别  问：“某个属性的不同类别之间的差异，” “某个类别和其他类别的差异”
        elif question_type == 'attribution_different':
            sql = ["MATCH (m:产品属性) where (m.名称 = '{0}' or '{0}' in m.别名) return m.名称, m.类别差异".format(i) for i in
                   entities[0]]

        # 询问某属性的不同类之间的差别  问：“某个属性的不同类别之间的差异，” “某个类别和其他类别的差异”
        elif question_type == 'category_different':
            sql = [
                "MATCH (m:属性类别)-[r:相关类别]->(n:属性类别) where m.名词 = '{0}' or '{0}' in m.别名  return m.名词, r.差异, n.名词".format(
                    i) for i in entities[0]]

        # 询问某属性的下的其他类别
        elif question_type == 'other_category':
            sql = [
                "MATCH (m:属性类别)-[r:相关类别]->(n:属性类别) where m.名词='{0}' or '{0}' in m.别名 return m.名词, r.name, n.名词".format(
                    i) for i in entities[0]]

        # 询问某类别的特性
        elif question_type == 'category_nature':
            sql = ["MATCH (m:属性类别) where m.名词 = '{0}' or '{0}' in m.别名  return m.名词, m.特性".format(i) for i in
                   entities[0]]

        # 寻求产品类型推荐    具体产品不做推荐哦！
        # elif question_type == 'recommend_category':
        #    sql = ["MATCH (m:Drug) where m.name = '{0}' or '{0}' in m.another_name  return m.name, m.advantage".format(i) for i in entities[0]]

        # 判断某类产品是否适合某类人群
        # elif question_type == 'if_recommend_category':
        #    sql = ["MATCH (m:Disease) where m.name = '{0}' or '{0}' in m.another_name  return m.name, m.pregnant".format(i) for i in entities[0]]

        # 询问某产品现在可以购买否
        elif question_type == 'if_buy':
            sql = ["MATCH (m:理财产品) where (m.产品名称 = '{0}' or m.登记编码 = '{0}') return m.理财产品, m.产品状态".format(i) for i in
                   entities[0]]

        return sql



if __name__ == '__main__':
    handler = QuestionPaser()