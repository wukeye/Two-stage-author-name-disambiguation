# 为验证二次消歧的效果，我们将每个人的每篇论文分开
import pandas as pd
da = pd.read_csv('new_information-final.csv', encoding='utf-8-sig', keep_default_na=False)
information_dict = {'AuthorId': [], 'AuthorName': [], 'AffiliatesNor': [], 'Year': []}
for i in range(len(da)):
    aff = eval(da.loc[i, ['Affiliates']].item())
    year = eval(da.loc[i, ['Years']].item())
    id = da.loc[i, ['AuthorId']].item()
    name = da.loc[i, ['AuthorName']].item()
    for j in range(len(aff)):
        information_dict['AuthorId'].append(id)
        information_dict['AffiliatesNor'].append(aff[j])
        information_dict['AuthorName'].append(name)
        information_dict['Year'].append(year[j])
    print(i)
df = pd.DataFrame(data=information_dict)
df = df.sort_values(by='AuthorName')
df.to_csv('new_info_for_eval.csv', encoding='utf-8-sig', index=0)