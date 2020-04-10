import pandas as pd

da = pd.read_csv('..\\AIpapersTop.tsv', encoding='utf-8-sig', keep_default_na=False, sep='\t')
information_dict = {'AuthorId': [], 'AuthorName': [], 'AffiliatesNor': [], 'Year': [], 'Title': [], 'Names_Coo': [], 'Doi': [], 'CitationNums': [], 'EstimateCitation': []}
for i in range(len(da)):

    # 处理每一行论文数据
    Author = list(da.loc[i, ['AuthorNames']])
    Author = Author[0].split('; ')
    Coauthor_list = []
    for item in Author:     # 为每个作者创建一个合作者列表
        Coauthor = str([ii for ii in Author if ii is not item])
        Coauthor_list.append(Coauthor)
    AuthorId = list(da.loc[i, ['AuthorIds']])
    AuthorId = AuthorId[0].split('; ')
    AffNor = list(da.loc[i, ['AffiliatesNormalized']])
    AffNor = AffNor[0].split('; ')
    year = da['Year'][i]
    title = da['OriginalTitle'][i]
    citation = da['CitationCount'][i]
    esticitation = da['EstimatedCitation'][i]
    doi = da['Doi'][i]

    # 加入dict中
    for j in range(len(Author)):
        information_dict['AuthorName'].append(Author[j])
        information_dict['AuthorId'].append(AuthorId[j])
        information_dict['AffiliatesNor'].append(AffNor[j])
        information_dict['Names_Coo'].append(Coauthor_list[j])
        information_dict['Year'].append(year)
        information_dict['Title'].append(title)
        information_dict['Doi'].append(doi)
        information_dict['CitationNums'].append(citation)
        information_dict['EstimateCitation'].append(esticitation)
    print(i)

test_df = pd.DataFrame(data=information_dict)
test_df = test_df.sort_values(by='AuthorName')
# 将通过地理位置爬取到的相关信息加入到原始数据中
compensate_data = pd.read_csv('information_from_location.csv', encoding='utf-8-sig')
test_df.insert(2, 'OriAffiliates', compensate_data['OriAffiliates'])
test_df.insert(4, 'Countries', compensate_data['country'])
test_df.insert(5, 'States', compensate_data['state'])
test_df.insert(6, 'Cities', compensate_data['city'])
test_df.insert(7, 'Universities', compensate_data['university'])
test_df.insert(8, 'Departments', compensate_data['Department'])
test_df.insert(15, 'labels', value=0)

test_df.to_excel('my_information_sort.xlsx', encoding='utf-8-sig', engine='openpyxl', index=0)

