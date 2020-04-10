from orcidspider.orcid import OrcidSpider
from orcidspider.orcid import parse_arg
import pandas as pd

def deal_info(arg):

    arg = arg.replace('nan,', '\'\',')
    arg = arg.replace('nan]', '\'\']')
    arg = eval(arg)
    arg = set(arg)
    if '' in arg:
        arg.remove('')
    arg = list(arg)
    return arg

i = 34544

data = pd.read_csv('first-finally.csv', encoding='utf-8-sig')
data_copy = data.copy()
data_copy.insert(12, 'orcid', '')
o = []
while i < len(data['AuthorId']):
    print(i)
    # 处理姓名
    name = data['AuthorName'][i]
    l = name.split(' ')
    if len(l) == 1:
        givenname = l[0]
        familyname = ''
    elif len(l) >= 2:
        familyname = l[-1]
        givenname = l[0]

    # 处理affiliates
    af = data['Affiliates'][i]
    af = deal_info(af)
    if not af:
        # 如果affiliate没有匹配到，则寻找其他keywords
        affiliates = ''
        key = data['Universities'][i]
        key = deal_info(key)
        if not key:
            key = data['Departments'][i]
            key = deal_info(key)
            if not key:
                key = data['Cities'][i]
                key = deal_info(key)
                if not key:
                    keywords = ''
            else:
                keywords = key[0]
        else:
            keywords = key[0]
    else:
        affiliates = af[0]
        keywords = ''

    query = parse_arg(familyname, givenname, affiliates, keywords)
    params = dict(
        q=query,  # 检索式
        start=0,  # 从检索到的第一个开始
        rows=1,  # 显示检索到的5个人的orcid
    )
    parser = OrcidSpider(params=params)
    orcid = parser.run()
    print(orcid)
    data_copy['orcid'][i] = orcid
    i = i + 1
    o.append(orcid)
    print(o)

data_copy.to_csv('new_information.csv', encoding='utf-8-sig', index=0)

# import pandas as pd
# f = open('..\\listt.txt', 'r')
# listall = []
# for line in f:
#     list1 = eval(line)
#     listall = listall + list1
# for i in range(len(listall)):
#     if listall[i] is None:
#         listall[i] = ''
#     listall[i] = str(listall[i])
# print(listall)
# data = pd.read_csv('first-finally.csv', encoding='utf-8-sig')
# data_copy = data.copy()
# data_copy.insert(12, 'orcid', listall)
# print(data_copy.head())
# data_copy.to_csv('new_information.csv', encoding='utf-8-sig', index=0)
