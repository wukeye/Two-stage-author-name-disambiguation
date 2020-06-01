''' 该模块作用是将拥有相同orcid的作者合并id '''
import pandas as pd
from collections import Counter
data = pd.read_csv('new_information.csv', encoding='utf-8-sig')
i = 0


dic_orcid = dict()

while i < len(data):
    # print(i)
    orcid = data['orcid'][i]
    if type(orcid) is float:
        i = i + 1
        continue
    # print(orcid)
    if orcid not in dic_orcid.keys():
        dic_orcid[orcid] = data['AuthorId'][i]
    else:
        data['AuthorId'][i] = dic_orcid[orcid]
        print(data['AuthorName'][i])
        print(dic_orcid[orcid])
    i = i + 1
print(len(dic_orcid.keys()))
print(len(data))
data.to_csv('new_information-second_disambiguation.csv', encoding='utf-8-sig', index=0)
