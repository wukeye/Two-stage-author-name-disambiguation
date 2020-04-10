# 合并同id的作者
import pandas as pd
data = pd.read_csv('first_disambiguation_Result.csv', encoding='utf-8-sig',keep_default_na=False)
l = 0
id_set = set()
gloab ={'nan': ""}
test_dic = {'AuthorId': [], 'AuthorName': [], 'Affiliates': [], 'Countries': [], 'States': [], 'Cities': [], 'Universities': [], 'Departments': [], 'Years': [], 'CitationNums': [], 'EstimateCitation': [], 'paperNums': []}
for i in range(len(data)):
    id_set.add(data['AuthorId'][i])
for id in id_set:
    id_aff = []
    id_country = []
    id_state = []
    id_city = []
    id_university = []
    id_department = []
    id_year = []
    id_citationum = 0
    id_estimacitation =0
    for j in data[data['AuthorId'] == id].index:
        id_aff.append(data['AffiliatesNor'][j])
        id_country.append(data['Countries'][j])
        id_state.append(data['States'][j])
        id_city.append(data['Cities'][j])
        id_university.append(data['Universities'][j])
        id_department.append(data['Departments'][j])
        id_year.append(data['Year'][j])
        id_citationum = id_citationum + int(data['CitationNums'][j])
        id_estimacitation = id_estimacitation+int(data['EstimateCitation'][j])
    test_dic['AuthorId'].append(id)
    test_dic['AuthorName'].append(data['AuthorName'][j])
    test_dic['Affiliates'].append(id_aff)
    test_dic['Countries'].append(id_country)
    test_dic['States'].append(id_state)
    test_dic['Cities'].append(id_city)
    test_dic['Universities'].append(id_university)
    test_dic['Departments'].append(id_department)
    test_dic['Years'].append(id_year)
    test_dic['CitationNums'].append(id_citationum)
    test_dic['EstimateCitation'].append(id_estimacitation)
    test_dic['paperNums'].append(len(data[data['AuthorId'] == id]))
    l = l + 1
    print(l)
dpf = pd.DataFrame(data=test_dic)
dpf = dpf.sort_values(by='AuthorId')
dpf.to_csv('first-finally.csv', encoding='utf-8-sig', index=0)


