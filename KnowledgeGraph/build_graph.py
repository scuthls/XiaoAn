import pandas as pd
import os
import json
from py2neo import Graph, Node
import numpy as np
class FinanceGraph:
    def __init__(self):
        self.g = Graph(
            host="127.0.0.1",
            http_port=7687,
            user="neo4j",
            password="admin")
        #self.g.run('MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r')

    def read_nodes(self):
        # 节点
        products = []  # 理财产品
        registration_codes = []  # 登记编码
        banks = []  # 银行
        areas = []  # 区域
        subbanks = []  # 支行
        investments = []  # 投资资产
        investment_types = []  # 投资资产类型
        operations = []  # 运作模式
        raise_ways = []  # 募集方式
        risk_levels = []  # 风险等级
        investment_natures = []  # 投资性质
        income_types = []  # 收益类型
        institution_categories = []  # 发行机构类别
        institutions = []  # 发行机构
        proper_nouns = []  # 说明书专有名词
        open_forms = []  # 开放形态
        types = []  # 类型  ——净值型 、 非净值型

        # 7.4完善
        banks_another_name = []  # 银行别名
        attributions = []  # 产品属性
        attributions_another_name = []  # 产品属性别名
        categories = []  # 属性类别
        categories_another_name = []  # 属性类别别名
        #

        product_infos = []  # 理财产品信息
        bank_infos = []  # 银行信息
        subbank_infos = []  # 支行信息
        investment_infos = []  # 投资资产信息   未收集
        investment_nature_infos = []  # 投资性质信息
        investment_type_infos = []  # 投资资产类型信息
        operation_infos = []  # 运作模式信息
        income_type_infos = []  # 收益类型信息
        raise_way_infos = []  # 募集方式信息
        risk_level_infos = []  # 风险等级信息
        institution_category_infos = []  # 发行机构类别信息

        # 专有名词解释 包括上面的部分列表
        cost_infos = []  # 理财费用信息
        disclosure_method_infos = []  # 披露方式信息
        liquidity_arrangement_infos = []  # 流动性安排信息
        product_element_infos = []  # 产品要素信息
        capital_operation_infos = []  # 资产运作信息
        risk_infos = []  # 风险信息
        management_subject_infos = []  # 管理主体信息
        open_form_infos = []  # 开放形态信息
        type_infos = []  # 类型信息    ——净值型 、 非净值型

        # 7.4完善
        attribution_infos = []  # 产品属性信息
        #

        # 关系
        rels_area = []  # 产品销售地区
        rels_subbank_area = []  # 支行所在区域
        rels_subbank_bank = []  # 支行所属总行
        rels_investment_nature = []  # 产品投资性质
        rels_investment_type = []  # 投资资产的类型
        rels_operation = []  # 产品的运作模式
        rels_income_type = []  # 产品收益类型
        rels_raise_way = []  # 产品募集方式
        rels_risk_level = []  # 产品的风险等级
        rels_product_institution = []  # 产品的发行机构
        rels_institution_category = []  # 发行机构的类别
        rels_institution_bank = []  # 发行机构所属总行
        rels_open_form = []  # 产品开放形态
        rels_type = []  # 产品类型 ——净值型 、 非净值型

        # 7.4完善
        rels_attribution_category = []  # 属性拥有的类别
        rels_other_category = []  # 相关的其他类别

        count = 0
        jsonFile = open('.\json\product.json', encoding='utf-8')
        jsonData = json.load(jsonFile)
        for data in jsonData:
            product_dict = {}
            count += 1
            print("product_node:", count)
            product = data['产品名称']
            product_dict['产品名称'] = product
            products.append(product)
            product_dict['登记编码'] = ''
            product_dict['服务对象'] = ''
            product_dict['业绩比较基准'] = ''
            product_dict['期限类型'] = ''
            product_dict['募集币种'] = ''
            product_dict['募集起始日期'] = ''
            product_dict['募集结束日期'] = ''
            product_dict['产品起始日期'] = ''
            product_dict['产品终止日期'] = ''
            product_dict['产品状态'] = ''
            product_dict['业务起始日'] = ''
            product_dict['业务结束日'] = ''
            product_dict['实际天数'] = ''
            product_dict['初始净值'] = ''
            product_dict['产品净值'] = ''
            product_dict['累计净值'] = ''
            product_dict['最近一次兑付收益率'] = ''
            product_dict['预期最高收益率'] = ''
            product_dict['预期最低收益率'] = ''
            product_dict['认购价格'] = ''

            # 7.4添加 未实现
            product_dict['投资资产种类及比例'] = ''
            product_dict['托管机构'] = ''
            product_dict['资金投向地区'] = ''
            product_dict['投资资产实时信息'] = ''
            product_dict['业绩表现'] = ''
            product_dict['产品评价'] = ''
            product_dict['包含费用'] = ''
            product_dict['业绩表现'] = ''
            # ...

            # 属性添加
            if '登记编码' in data:
                product_dict['登记编码'] = data['登记编码']
                registration_codes.append(data['登记编码'])

            if '业绩比较基准' in data:
                product_dict['业绩比较基准'] = data['业绩比较基准']

            if '服务对象' in data:
                product_dict['服务对象'] = data['产品类别']

            if '期限类型' in data:
                product_dict['期限类型'] = data['期限类型']

            if '募集币种' in data:
                product_dict['募集币种'] = data['募集币种']

            if '募集起始日期' in data:
                product_dict['募集起始日期'] = data['募集起始日期']

            if '募集结束日期' in data:
                product_dict['募集结束日期'] = data['募集结束日期']

            if '产品起始日期' in data:
                product_dict['产品起始日期'] = data['产品起始日期']

            if '产品终止日期' in data:
                product_dict['产品终止日期'] = data['产品终止日期']

            if '产品状态' in data:
                product_dict['产品状态'] = data['产品状态']

            if '业务起始日' in data:
                product_dict['业务起始日'] = data['业务起始日']

            if '业务结束日' in data:
                product_dict['业务结束日'] = data['业务结束日']

            if '实际天数' in data:
                product_dict['实际天数'] = data['实际天数']

            if '初始净值' in data:
                product_dict['初始净值'] = data['初始净值']

            if '产品净值' in data:
                product_dict['产品净值'] = data['产品净值']

            if '累计净值' in data:
                product_dict['累计净值'] = data['累计净值']

            if '最近一次兑付收益率' in data:
                product_dict['最近一次兑付收益率'] = data['最近一次兑付收益率']

            if '预期最高收益率' in data:
                product_dict['预期最高收益率'] = data['预期最高收益率']

            if '预期最低收益率' in data:
                product_dict['预期最低收益率'] = data['预期最低收益率']

            if '认购价格' in data:
                product_dict['认购价格'] = data['认购价格']

            # 关系添加
            if '投资资产类型' in data:
                investment_types.append(data['投资资产类型'])
                rels_investment_type.append([product, data['投资资产类型']])

            if '运作模式' in data:
                operations.append(data['运作模式'])
                rels_operation.append([product, data['运作模式']])
                open_forms.append(data['运作模式'][0:3])
                rels_open_form.append([product, data['运作模式'][0:3]])
                types.append(data['运作模式'][3:])
                rels_type.append([product, data['运作模式'][3:]])

            if '收益类型' in data:
                income_types.append(data['收益类型'])
                rels_income_type.append([product, data['收益类型']])

            if '募集方式' in data:
                raise_ways.append(data['募集方式'])
                rels_raise_way.append([product, data['募集方式']])

            if '风险等级' in data:
                risk_levels.append(data['风险等级'])
                rels_risk_level.append([product, data['风险等级']])

            if '投资性质' in data:
                investment_natures.append(data['投资性质'])
                rels_investment_nature.append([product, data['投资性质']])

            if '机构类别' in data:
                institution_categories.append(data['机构类别'])
                rels_institution_category.append([data['发行机构'], data['机构类别']])

            if '发行机构' in data:
                institutions.append(data['发行机构'])
                if '农业银行' in data['发行机构']:
                    banks.append('农业银行')
                    rels_institution_bank.append([data['发行机构'], '农业银行'])
                elif '汇丰银行' in data['发行机构']:
                    banks.append('汇丰银行')
                    rels_institution_bank.append([product, '汇丰银行'])
                elif '招商银行' in data['发行机构']:
                    banks.append('招商银行')
                    rels_institution_bank.append([product, '招商银行'])
                rels_product_institution.append([product, data['发行机构']])

            if '产品销售区域' in data:
                for area in data['产品销售区域'].split(','):
                    areas.append(area)
                    rels_area.append([product, area])

            product_infos.append(product_dict)

        count = 0
        jsonFile = open('.\json\\attribution.json', encoding='utf-8')
        jsonData = json.load(jsonFile)
        for data in jsonData:
            attribution_dict = {}
            count += 1
            print("attribution_node:", count)
            attribution = data['名称']
            attribution_dict['名称'] = attribution
            attributions.append(attribution)
            attribution = data['别名']
            attribution_dict['类别差异'] = ''

            # 属性添加
            if '别名' in data:
                attribution_dict['别名'] = data['别名']
                for 别名 in data['别名'].split(','):
                    attributions_another_name.append(别名)

            if '类别差异' in data:
                attribution_dict['类别差异'] = data['类别差异']

            # 关系添加
            if '类别' in data:
                for 类别 in data['类别'].split(','):
                    categories.append(类别)
                    rels_attribution_category.append([attribution, 类别])
                    for 类别_ in data['类别'].split(','):
                        rels_other_category.append([类别, 类别_])

            attribution_infos.append(attribution_dict)

        count = 0
        jsonFile = open('.\json\subbank.json', encoding='utf-8')
        jsonData = json.load(jsonFile)
        for data in jsonData:
            subbank_dict = {}
            count += 1
            print("subbank_node:", count)
            subbank = data['名称']
            subbank_dict['名称'] = subbank
            subbanks.append(subbank)
            subbank_dict['区域'] = ''
            subbank_dict['具体地址'] = ''
            subbank_dict['咨询电话'] = ''

            # 属性添加
            if '具体地址' in data:
                subbank_dict['具体地址'] = data['具体地址']

            if '咨询电话' in data:
                subbank_dict['咨询电话'] = data['电话']

            if '区域' in data:
                subbank_dict['区域'] = data['区域']
                rels_subbank_area.append([subbank, data['区域'].split('省')[0]])

            # 关系添加
            if '总行' in data:
                banks.append(data['总行'])
                rels_subbank_bank.append([subbank, data['总行']])

            subbank_infos.append(subbank_dict)

        count = 0
        jsonFile = open('.\\json\\bank.json', encoding='utf-8')
        jsonData = json.load(jsonFile)
        for data in jsonData:
            bank_dict = {}
            count += 1
            print("bank_node:", count)
            bank = data['名称']
            bank_dict['名称'] = bank
            banks.append(bank)
            bank_dict['别名'] = ''
            bank_dict['营业时间'] = ''
            bank_dict['客服电话'] = ''
            bank_dict['官网链接'] = ''

            # 属性添加
            if '别名' in data:
                bank_dict['别名'] = data['别名']
                for 别名 in data['别名'].split(','):
                    banks_another_name.append(别名)

            if '营业时间' in data:
                bank_dict['营业时间'] = data['营业时间']

            if '客服电话' in data:
                bank_dict['客服电话'] = data['客服电话']

            if '官网链接' in data:
                bank_dict['官网链接'] = data['官网链接']

            bank_infos.append(bank_dict)

        count = 0
        jsonFile = open('.\\json\\capital_operation.json', encoding='utf-8')
        jsonData = json.load(jsonFile)
        for data in jsonData:
            capital_operation_dict = {}
            count += 1
            print("capital_operation_node:", count)
            capital_operation = data['名词']
            proper_nouns.append(capital_operation)
            capital_operation_dict['名词'] = capital_operation
            capital_operation_dict['定义'] = ''

            # 属性添加

            if '定义' in data:
                capital_operation_dict['定义'] = data['定义']

            capital_operation_infos.append(capital_operation_dict)

        count = 0
        jsonFile = open('.\\json\\cost.json', encoding='utf-8')
        jsonData = json.load(jsonFile)
        for data in jsonData:
            cost_dict = {}
            count += 1
            print("cost_node:", count)
            cost = data['名词']
            proper_nouns.append(cost)
            cost_dict['名词'] = cost
            cost_dict['定义'] = ''

            # 属性添加

            if '定义' in data:
                cost_dict['定义'] = data['定义']

            cost_infos.append(cost_dict)

        count = 0
        jsonFile = open('.\\json\\disclosure_method.json', encoding='utf-8')
        jsonData = json.load(jsonFile)
        for data in jsonData:
            disclosure_method_dict = {}
            count += 1
            print("disclosure_method_node:", count)
            disclosure_method = data['名词']
            proper_nouns.append(disclosure_method)
            disclosure_method_dict['名词'] = disclosure_method
            disclosure_method_dict['定义'] = ''

            # 属性添加

            if '定义' in data:
                disclosure_method_dict['定义'] = data['定义']

            disclosure_method_infos.append(disclosure_method_dict)

        count = 0
        jsonFile = open('.\\json\\income_type.json', encoding='utf-8')
        jsonData = json.load(jsonFile)
        for data in jsonData:
            income_type_dict = {}
            count += 1
            print("income_type_node:", count)
            income_type = data['名词']
            proper_nouns.append(income_type)
            income_type_dict['名词'] = income_type
            income_types.append(income_type)
            categories.append(income_type)
            income_type_dict['别名'] = ''
            income_type_dict['特性'] = ''
            income_type_dict['适用人群'] = ''

            # 属性添加
            if '别名' in data:
                income_type_dict['别名'] = data['别名']
                for 别名 in data['别名'].split(','):
                    categories_another_name.append(别名)
            if '特性' in data:
                income_type_dict['特性'] = data['特性']

            if '适用人群' in data:
                income_type_dict['适用人群'] = data['适用人群']

            income_type_infos.append(income_type_dict)

        count = 0
        jsonFile = open('.\\json\\institution_category.json', encoding='utf-8')
        jsonData = json.load(jsonFile)
        for data in jsonData:
            institution_category_dict = {}
            count += 1
            print("institution_category_node:", count)
            institution_category = data['名词']
            proper_nouns.append(institution_category)
            categories.append(institution_category)
            institution_category_dict['名词'] = institution_category
            institution_categories.append(institution_category)
            institution_category_dict['定义'] = ''
            institution_category_dict['别名'] = ''

            # 属性添加
            if '别名' in data:
                institution_category_dict['别名'] = data['别名']
                for 别名 in data['别名'].split(','):
                    categories_another_name.append(别名)
            if '定义' in data:
                institution_category_dict['定义'] = data['定义']

            institution_category_infos.append(institution_category_dict)

        count = 0
        jsonFile = open('.\\json\\investment_nature.json', encoding='utf-8')
        jsonData = json.load(jsonFile)
        for data in jsonData:
            investment_nature_dict = {}
            count += 1
            print("investment_nature_node:", count)
            investment_nature = data['名词']
            proper_nouns.append(investment_nature)
            investment_nature_dict['名词'] = investment_nature
            investment_natures.append(investment_nature)
            categories.append(investment_nature)
            investment_nature_dict['别名'] = ''
            investment_nature_dict['定义'] = ''
            investment_nature_dict['特性'] = ''
            investment_nature_dict['适用人群'] = ''

            # 属性添加
            if '别名' in data:
                investment_nature_dict['别名'] = data['别名']
                for 别名 in data['别名'].split(','):
                    categories_another_name.append(别名)
            if '定义' in data:
                investment_nature_dict['定义'] = data['定义']

            if '特性' in data:
                investment_nature_dict['特性'] = data['特性']

            if '适用人群' in data:
                investment_nature_dict['适用人群'] = data['适用人群']

            investment_nature_infos.append(investment_nature_dict)

        count = 0
        jsonFile = open('.\\json\\liquidity_arrangement.json', encoding='utf-8')
        jsonData = json.load(jsonFile)
        for data in jsonData:
            liquidity_arrangement_dict = {}
            count += 1
            print("liquidity_arrangement_node:", count)
            liquidity_arrangement = data['名词']
            proper_nouns.append(liquidity_arrangement)
            liquidity_arrangement_dict['名词'] = liquidity_arrangement
            liquidity_arrangement_dict['定义'] = ''

            # 属性添加

            if '定义' in data:
                liquidity_arrangement_dict['定义'] = data['定义']

            liquidity_arrangement_infos.append(liquidity_arrangement_dict)

        count = 0
        jsonFile = open('.\\json\\management_subject.json', encoding='utf-8')
        jsonData = json.load(jsonFile)
        for data in jsonData:
            management_subject_dict = {}
            count += 1
            print("management_subject_node:", count)
            management_subject = data['名词']
            proper_nouns.append(management_subject)
            management_subject_dict['名词'] = management_subject
            management_subject_dict['定义'] = ''
            management_subject_dict['特性'] = ''

            # 属性添加
            if '定义' in data:
                management_subject_dict['定义'] = data['定义']
            if '特性' in data:
                management_subject_dict['特性'] = data['特性']

            management_subject_infos.append(management_subject_dict)

        count = 0
        jsonFile = open('.\\json\\open_form.json', encoding='utf-8')
        jsonData = json.load(jsonFile)
        for data in jsonData:
            open_form_dict = {}
            count += 1
            print("open_form_node:", count)
            open_form = data['名词']
            proper_nouns.append(open_form)
            open_form_dict['名词'] = open_form
            open_forms.append(open_form)
            categories.append(open_form)
            open_form_dict['别名'] = ''
            open_form_dict['定义'] = ''
            open_form_dict['特性'] = ''
            open_form_dict['适用人群'] = ''

            # 属性添加
            if '别名' in data:
                open_form_dict['别名'] = data['别名']
                for 别名 in data['别名'].split(','):
                    categories_another_name.append(别名)
            if '定义' in data:
                open_form_dict['定义'] = data['定义']

            if '特性' in data:
                open_form_dict['特性'] = data['特性']

            if '适用人群' in data:
                open_form_dict['适用人群'] = data['适用人群']

            open_form_infos.append(open_form_dict)

        count = 0
        jsonFile = open('.\\json\\operation.json', encoding='utf-8')
        jsonData = json.load(jsonFile)
        for data in jsonData:
            operation_dict = {}
            count += 1
            print("operation_dict_node:", count)
            operation = data['名词']
            proper_nouns.append(operation)
            operation_dict['名词'] = operation
            operations.append(operation)
            categories.append(operation)
            operation_dict['别名'] = ''
            operation_dict['开放形态'] = ''
            operation_dict['产品类型'] = ''

            # 属性添加
            if '别名' in data:
                operation_dict['别名'] = data['别名']
                for 别名 in data['别名'].split(','):
                    categories_another_name.append(别名)

            if '开放形态' in data:
                operation_dict['开放形态'] = data['开放形态']

            if '产品类型' in data:
                operation_dict['产品类型'] = data['产品类型']

            operation_infos.append(operation_dict)

        count = 0
        jsonFile = open('.\\json\\product_element.json', encoding='utf-8')
        jsonData = json.load(jsonFile)
        for data in jsonData:
            product_element_dict = {}
            count += 1
            print("product_element_node:", count)
            product_element = data['名词']
            proper_nouns.append(product_element)
            product_element_dict['名词'] = product_element
            product_element_dict['定义'] = ''

            # 属性添加

            if '定义' in data:
                product_element_dict['定义'] = data['定义']

            product_element_infos.append(product_element_dict)

        count = 0
        jsonFile = open('.\\json\\raise_way.json', encoding='utf-8')
        jsonData = json.load(jsonFile)
        for data in jsonData:
            raise_way_dict = {}
            count += 1
            print("raise_way_dict_node:", count)
            raise_way = data['名词']
            proper_nouns.append(raise_way)
            raise_way_dict['名词'] = raise_way
            raise_ways.append(raise_way)
            categories.append(raise_way)
            raise_way_dict['别名'] = ''
            raise_way_dict['定义'] = ''
            raise_way_dict['特性'] = ''
            raise_way_dict['适用人群'] = ''

            # 属性添加
            if '别名' in data:
                raise_way_dict['别名'] = data['别名']
                for 别名 in data['别名'].split(','):
                    categories_another_name.append(别名)

            if '定义' in data:
                raise_way_dict['定义'] = data['定义']

            if '特性' in data:
                raise_way_dict['特性'] = data['特性']

            if '适用人群' in data:
                raise_way_dict['适用人群'] = data['适用人群']

            raise_way_infos.append(raise_way_dict)

        count = 0
        jsonFile = open('.\\json\\investment_type.json', encoding='utf-8')
        jsonData = json.load(jsonFile)
        for data in jsonData:
            investment_type_dict = {}
            count += 1
            print("investment_type_node:", count)
            investment_type = data['名词']
            proper_nouns.append(investment_type)
            investment_type_dict['名词'] = investment_type
            investment_types.append(investment_type)
            categories.append(investment_type)
            investment_type_dict['别名'] = ''
            investment_type_dict['定义'] = ''

            # 属性添加
            if '别名' in data:
                investment_type_dict['别名'] = data['别名']
                for 别名 in data['别名'].split(','):
                    categories_another_name.append(别名)

            if '定义' in data:
                investment_type_dict['定义'] = data['定义']

            investment_type_infos.append(investment_type_dict)

        count = 0
        jsonFile = open('.\\json\\risk.json', encoding='utf-8')
        jsonData = json.load(jsonFile)
        for data in jsonData:
            risk_dict = {}
            count += 1
            print("risk_node:", count)
            risk = data['名词']
            proper_nouns.append(risk)
            risk_dict['名词'] = risk
            risk_dict['定义'] = ''

            # 属性添加

            if '定义' in data:
                risk_dict['定义'] = data['定义']

            risk_infos.append(risk_dict)

        count = 0
        jsonFile = open('.\\json\\risk_level.json', encoding='utf-8')
        jsonData = json.load(jsonFile)
        for data in jsonData:
            risk_level_dict = {}
            count += 1
            print("risk_level_node:", count)
            risk_level = data['名词']
            proper_nouns.append(risk_level)
            risk_level_dict['名词'] = risk_level
            risk_levels.append(risk_level)
            categories.append(risk_level)
            risk_level_dict['别名'] = ''
            risk_level_dict['特性'] = ''

            # 属性添加
            if '别名' in data:
                risk_level_dict['别名'] = data['别名']
                for 别名 in data['别名'].split(','):
                    categories_another_name.append(别名)

            if '特性' in data:
                risk_level_dict['特性'] = data['特性']

            risk_level_infos.append(risk_level_dict)

        count = 0
        jsonFile = open('.\\json\\type.json', encoding='utf-8')
        jsonData = json.load(jsonFile)
        for data in jsonData:
            type_dict = {}
            count += 1
            print("type_node:", count)
            type = data['名词']
            proper_nouns.append(type)
            type_dict['名词'] = type
            types.append(type)
            categories.append(type)
            type_dict['别名'] = ''
            type_dict['定义'] = ''
            type_dict['特性'] = ''
            type_dict['适用人群'] = ''

            # 属性添加
            if '别名' in data:
                type_dict['别名'] = data['别名']
                for 别名 in data['别名'].split(','):
                    categories_another_name.append(别名)

            if '定义' in data:
                type_dict['定义'] = data['定义']

            if '特性' in data:
                type_dict['特性'] = data['特性']

            if '适用人群' in data:
                type_dict['适用人群'] = data['适用人群']

            type_infos.append(type_dict)

        return set(products), set(registration_codes), set(banks), set(areas), set(subbanks), set(investments), set(investment_types), set(operations), set(raise_ways), set(risk_levels), set(investment_natures), set(income_types), set(institution_categories), set(institutions), set(proper_nouns), set(open_forms), set(types), set(banks_another_name), set(attributions), set(attributions_another_name), set(categories), set(categories_another_name), \
               product_infos, bank_infos, subbank_infos, investment_infos, investment_nature_infos, investment_type_infos, operation_infos, income_type_infos, raise_way_infos, risk_level_infos, institution_category_infos, cost_infos, disclosure_method_infos, liquidity_arrangement_infos, product_element_infos, capital_operation_infos, risk_infos, management_subject_infos, open_form_infos, type_infos, attribution_infos ,\
               rels_area, rels_subbank_area, rels_subbank_bank, rels_investment_nature, rels_investment_type, rels_operation, rels_income_type, rels_raise_way, rels_risk_level, rels_product_institution, rels_institution_category, rels_institution_bank, rels_open_form, rels_type, rels_attribution_category, rels_other_category

    # 建立产品节点
    def create_product_nodes(self, product_infos):
        count = 0
        for product_dict in product_infos:
            node = Node("理财产品",
                        产品名称=product_dict['产品名称'],
                        登记编码=product_dict['登记编码'],
                        服务对象=product_dict['服务对象'],
                        业绩比较基准=product_dict['业绩比较基准'],
                        期限类型=product_dict['期限类型'],
                        募集币种=product_dict['募集币种'],
                        募集起始日期=product_dict['募集起始日期'],
                        募集结束日期=product_dict['募集结束日期'],
                        产品起始日期=product_dict['产品起始日期'],
                        产品终止日期=product_dict['产品终止日期'],
                        产品状态=product_dict['产品状态'],
                        业务起始日=product_dict['业务起始日'],
                        业务结束日=product_dict['业务结束日'],
                        实际天数=product_dict['实际天数'],
                        初始净值=product_dict['初始净值'],
                        产品净值=product_dict['产品净值'],
                        累计净值=product_dict['累计净值'],
                        最近一次兑付收益率=product_dict['最近一次兑付收益率'],
                        预期最高收益率=product_dict['预期最高收益率'],
                        预期最低收益率=product_dict['预期最低收益率'],
                        认购价格=product_dict['认购价格'])
            self.g.create(node)
            count += 1
            print("产品节点：", count)
        return

    # 建立银行节点
    def create_bank_nodes(self, bank_infos):
        count = 0
        for bank_dict in bank_infos:
            node = Node("银行",
                        名称=bank_dict['名称'],
                        营业时间=bank_dict['营业时间'],
                        客服电话=bank_dict['客服电话'],
                        官网链接=bank_dict['官网链接'])
            self.g.create(node)
            count += 1
            print("银行节点：", count)
        return

    # 建立支行节点
    def create_subbank_nodes(self, subbank_infos):
        count = 0
        for subbank_dict in subbank_infos:
            node = Node("支行",
                        名称=subbank_dict['名称'],
                        区域=subbank_dict['区域'],
                        具体地址=subbank_dict['具体地址'],
                        咨询电话=subbank_dict['咨询电话'])
            self.g.create(node)
            count += 1
            print("支行节点：", count)
        return

    # 建立产品属性节点
    def create_attribution_nodes(self, attribution_infos):
        count = 0
        for attribution_dict in attribution_infos:
            node = Node('产品属性',
                        名称=attribution_dict['名称'],
                        别名=attribution_dict['别名'],
            类别差异 = attribution_dict['类别差异'])
            self.g.create(node)
            count += 1
            # print(count, len(nodes))
        return

    # 建立节点
    def create_node(self, label, nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, 名称=node_name)
            self.g.create(node)
            count += 1
            # print(count, len(nodes))
        return

    # 建立节点1
    def create_node1(self, label, nodes):
        count = 0
        for node_dict in nodes:
            node = Node(label, 名词=node_dict['名词'], 定义=node_dict['定义'])
            self.g.create(node)
            count += 1
            # print(count, len(nodes))
        return

    def create_node11(self, label1, label2, nodes):
        count = 0
        for node_dict in nodes:
            node = Node(label1, label2, 名词=node_dict['名词'], 别名=node_dict['别名'], 定义=node_dict['定义'])
            self.g.create(node)
            count += 1
            # print(count, len(nodes))
        return

    # 建立节点2
    def create_node2(self, label1, label2, nodes):
        count = 0
        for node_dict in nodes:
            node = Node(label1, label2, 名词=node_dict['名词'], 别名=node_dict['别名'], 定义=node_dict['定义'],
                        特性=node_dict['特性'], 适用人群=node_dict['适用人群'])
            self.g.create(node)
            count += 1
            # print(count, len(nodes))
        return

    # 建立节点3
    def create_node3(self, label1, label2, nodes):
        count = 0
        for node_dict in nodes:
            node = Node(label1, label2, 名词=node_dict['名词'], 别名=node_dict['别名'],
                        特性=node_dict['特性'], 适用人群=node_dict['适用人群'])
            self.g.create(node)
            count += 1
            # print(count, len(nodes))
        return

    # 建立节点4
    def create_node4(self, label1, label2, nodes):
        count = 0
        for node_dict in nodes:
            node = Node(label1, label2, 名词=node_dict['名词'], 别名=node_dict['别名'],
                        开放形态=node_dict['开放形态'], 产品类型=node_dict['产品类型'])
            self.g.create(node)
            count += 1
            # print(count, len(nodes))
        return

    # 建立节点5
    def create_node5(self, label, nodes):
        count = 0
        for node_dict in nodes:
            node = Node(label, 名词=node_dict['名词'],
                        定义=node_dict['定义'], 特性=node_dict['特性'])
            self.g.create(node)
            count += 1
            # print(count, len(nodes))
        return

    # 建立节点6
    def create_node6(self, label1, label2, nodes):
        count = 0
        for node_dict in nodes:
            node = Node(label1, label2, 名词=node_dict['名词'],
                        别名=node_dict['别名'], 特性=node_dict['特性'])
            self.g.create(node)
            count += 1
            # print(count, len(nodes))
        return

    # 创建知识图谱实体节点类型schema
    def create_graphnodes(self):
        products, registration_codes, banks, areas, subbanks, investments, investment_types, operations, raise_ways, risk_levels, investment_natures, income_types, institution_categories, institutions, proper_nouns, open_forms, types, banks_another_name, attributions, attributions_another_name, categories, categories_another_name, \
        product_infos, bank_infos, subbank_infos, investment_infos, investment_nature_infos, investment_type_infos, operation_infos, income_type_infos, raise_way_infos, risk_level_infos, institution_category_infos, cost_infos, disclosure_method_infos, liquidity_arrangement_infos, product_element_infos, capital_operation_infos, risk_infos, management_subject_infos,open_form_infos, type_infos,  attribution_infos, \
        rels_area, rels_subbank_area, rels_subbank_bank, rels_investment_nature, rels_investment_type, rels_operation, rels_income_type, rels_raise_way, rels_risk_level, rels_product_institution, rels_institution_category, rels_institution_bank, rels_open_form, rels_type, rels_attribution_category, rels_other_category = self.read_nodes()
        self.create_product_nodes(product_infos)
        self.create_bank_nodes(bank_infos)
        self.create_subbank_nodes(subbank_infos)
        self.create_attribution_nodes(attribution_infos)

        self.create_node('区域', areas)
        self.create_node('投资资产', investments)
        self.create_node('发行机构', institutions)

        self.create_node1('风险', risk_infos)
        self.create_node1('费用', cost_infos)
        self.create_node1('产品要素', product_element_infos)
        self.create_node1('资产运作', capital_operation_infos)
        self.create_node1('信息披露', disclosure_method_infos)
        self.create_node1('流动性安排', liquidity_arrangement_infos)
        self.create_node11('机构类别', '属性类别', institution_category_infos)
        self.create_node11('投资资产类型', '属性类别', investment_type_infos)

        self.create_node2('募集方式', '属性类别', raise_way_infos)
        self.create_node2('开放形态', '属性类别', open_form_infos)
        self.create_node2('产品类型', '属性类别', type_infos)
        self.create_node2('投资性质', '属性类别', investment_nature_infos)

        self.create_node3('收益类型', '属性类别', income_type_infos)
        self.create_node4('运作模式', '属性类别', operation_infos)
        self.create_node5('管理主体', management_subject_infos)
        self.create_node6('风险等级', '属性类别', risk_level_infos)
        # 投资资产未创建
        return

    # 创建实体关系边
    def create_graphrels(self):
        products, registration_codes, banks, areas, subbanks, investments, investment_types, operations, raise_ways, risk_levels, investment_natures, income_types, institution_categories, institutions, proper_nouns, open_forms, types, banks_another_name, attributions, attributions_another_name, categories, categories_another_name, \
        product_infos, bank_infos, subbank_infos, investment_infos, investment_nature_infos, investment_type_infos, operation_infos, income_type_infos, raise_way_infos, risk_level_infos, institution_category_infos, cost_infos, disclosure_method_infos, liquidity_arrangement_infos, product_element_infos, capital_operation_infos, risk_infos, management_subject_infos,open_form_infos, type_infos,  attribution_infos, \
        rels_area, rels_subbank_area, rels_subbank_bank, rels_investment_nature, rels_investment_type, rels_operation, rels_income_type, rels_raise_way, rels_risk_level, rels_product_institution, rels_institution_category, rels_institution_bank, rels_open_form, rels_type, rels_attribution_category, rels_other_category = self.read_nodes()
        self.create_relationship('理财产品', '区域', rels_area, '销售地区', '销售地区',3)
        self.create_relationship('支行', '区域', rels_subbank_area, '所在区域', '所在区域',2)
        self.create_relationship('支行', '银行', rels_subbank_bank, '所属总行', '所属总行',2)
        self.create_relationship('理财产品', '投资性质', rels_investment_nature, '投资性质属于', '投资性质属于',0)
        self.create_relationship('理财产品', '投资资产类型', rels_investment_type, '投资资产的类型属于', '投资资产,0的类型属于')
        self.create_relationship('理财产品', '运作模式', rels_operation, '运作模式属于', '运作模式属于',0)
        self.create_relationship('理财产品', '收益类型', rels_income_type, '收益类型属于', '收益类型属于',0)
        self.create_relationship('理财产品', '募集方式', rels_raise_way, '募集方式属于', '募集方式属于',0)
        self.create_relationship('理财产品', '风险等级', rels_risk_level, '风险等级属于', '风险等级属于',0)
        self.create_relationship('理财产品', '发行机构', rels_product_institution, '发行机构属于', '发行机构属于',3)
        self.create_relationship('理财产品', '机构类别', rels_institution_category, '发行机构类别属于', '发行机构类别属于',0)
        self.create_relationship('发行机构', '总行', rels_institution_bank, '所属总行', '所属总行',2)
        self.create_relationship('理财产品', '开放形态', rels_open_form, '开放形态属于', '开放形态属于',0)
        self.create_relationship('理财产品', '产品类型', rels_type, '所属类型', '所属类型',0)
        self.create_relationship('产品属性', '属性类别', rels_attribution_category, '含有类别', '含有类别',1)
        self.create_relationship('属性类别', '属性类别', rels_other_category, '相关类别', '相关类别',4)
        return

    # 创建实体关联边
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name,n):
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            # 关系的属性
            if n == 0:
                query = "match(p:%s),(q:%s) where p.产品名称='%s'and q.名词='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                    start_node, end_node, p, q, rel_type, rel_name)
            elif n==1:
                query = "match(p:%s),(q:%s) where p.名称='%s'and q.名词='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                    start_node, end_node, p, q, rel_type, rel_name)
            elif n == 2:
                query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                    start_node, end_node, p, q, rel_type, rel_name)
            elif n == 3:
                query = "match(p:%s),(q:%s) where p.产品名称='%s'and q.名称='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                    start_node, end_node, p, q, rel_type, rel_name)
            elif n == 4:
                query = "match(p:%s),(q:%s) where p.名词='%s'and q.名词='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                    start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return

    # 导出数据
    def export_data(self):
        products, registration_codes, banks, areas, subbanks, investments, investment_types, operations, raise_ways, risk_levels, investment_natures, income_types, institution_categories, institutions, proper_nouns, open_forms, types, banks_another_name, attributions, attributions_another_name, categories, categories_another_name, \
        product_infos, bank_infos, subbank_infos, investment_infos, investment_nature_infos, investment_type_infos, operation_infos, income_type_infos, raise_way_infos, risk_level_infos, institution_category_infos, cost_infos, disclosure_method_infos, liquidity_arrangement_infos, product_element_infos, capital_operation_infos, risk_infos, management_subject_infos,open_form_infos, type_infos,  attribution_infos, \
        rels_area, rels_subbank_area, rels_subbank_bank, rels_investment_nature, rels_investment_type, rels_operation, rels_income_type, rels_raise_way, rels_risk_level, rels_product_institution, rels_institution_category, rels_institution_bank, rels_open_form, rels_type, rels_attribution_category, rels_other_category = self.read_nodes()
        f_product = open('./dict/product.txt', 'w+', encoding="utf-8")
        f_bank = open('./dict/bank.txt', 'w+', encoding="utf-8")
        f_area = open('./dict/area.txt', 'w+', encoding="utf-8")
        f_subbank = open('./dict/subbank.txt', 'w+', encoding="utf-8")
        f_investment = open('./dict/investment.txt', 'w+', encoding="utf-8")
        f_investment_type = open('./dict/investment_type.txt', 'w+', encoding="utf-8")
        f_operation = open('./dict/operation.txt', 'w+', encoding="utf-8")
        f_raise_way = open('./dict/raise_way.txt', 'w+', encoding="utf-8")
        f_risk_level = open('./dict/risk_level.txt', 'w+', encoding="utf-8")
        f_investment_nature = open('./dict/investment_nature.txt', 'w+', encoding="utf-8")
        f_income_type = open('./dict/income_type.txt', 'w+', encoding="utf-8")
        f_institution_category = open('./dict/institution_category.txt', 'w+', encoding="utf-8")
        f_institution = open('./dict/institution.txt', 'w+', encoding="utf-8")
        f_proper_noun = open('./dict/proper_noun.txt', 'w+', encoding="utf-8")
        f_open_form = open('./dict/open_form.txt', 'w+', encoding="utf-8")
        f_type = open('./dict/type.txt', 'w+', encoding="utf-8")
        f_attribution = open('./dict/attribution.txt', 'w+', encoding="utf-8")
        f_category = open('./dict/category.txt', 'w+', encoding="utf-8")


        print('\n'.join(list(products)))
        print("--------分割线-------")
        print('\n'.join(list(registration_codes)))

        f_product.write('\n'.join(list(products)))
        f_product.write('\n')
        f_product.write('\n'.join(list(registration_codes)))

        f_bank.write('\n'.join(list(banks)))
        f_bank.write('\n')
        f_bank.write('\n'.join(list(banks_another_name)))

        f_area.write('\n'.join(list(areas)))

        f_subbank.write('\n'.join(list(subbanks)))

        f_investment.write('\n'.join(list(investments)))

        f_investment_type.write('\n'.join(list(investment_types)))

        f_operation.write('\n'.join(list(operations)))

        f_raise_way.write('\n'.join(list(raise_ways)))

        f_risk_level.write('\n'.join(list(risk_levels)))

        f_investment_nature.write('\n'.join(list(investment_natures)))

        f_income_type.write('\n'.join(list(income_types)))

        f_institution_category.write('\n'.join(list(institution_categories)))

        f_institution.write('\n'.join(list(institutions)))

        f_proper_noun.write('\n'.join(list(proper_nouns)))

        f_open_form.write('\n'.join(list(open_forms)))

        f_type.write('\n'.join(list(types)))

        f_attribution.write('\n'.join(list(attributions)))
        f_attribution.write('\n')
        f_attribution.write('\n'.join(list(attributions_another_name)))

        f_category.write('\n'.join(list(categories)))
        f_category.write('\n')
        f_category.write('\n'.join(list(categories_another_name)))

        f_product.close()
        f_bank.close()
        f_area.close()
        f_subbank.close()
        f_investment.close()
        f_investment_type.close()
        f_operation.close()
        f_raise_way.close()
        f_risk_level.close()
        f_investment_nature.close()
        f_income_type.close()
        f_institution_category.close()
        f_institution.close()
        f_proper_noun.close()
        f_open_form.close()
        f_type.close()
        f_attribution.close()
        f_category.close()


        return



if __name__ == '__main__':
    handler = FinanceGraph()
    handler.create_graphnodes()
    handler.create_graphrels()
    handler.export_data()