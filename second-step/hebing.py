import pandas as pd
data = pd.read_csv('new_information-second_disambiguation.csv', encoding='utf-8-sig')
ll = []
gloab ={'nan': ""}
for i in range(len(data)):
    for j in data.loc[(data['AuthorId'] == data['AuthorId'][i])].index:
        if j > i:
            data['Affiliates'][i] = str(eval(data['Affiliates'][i], gloab)+eval(data["Affiliates"][j], gloab))
            data['Countries'][i] = str(eval(data['Countries'][i], gloab)+eval(data['Countries'][j], gloab))
            data['States'][i] = str(eval(data['States'][i], gloab)+eval(data['States'][j], gloab))
            data['Cities'][i] = str(eval(data['Cities'][i], gloab)+eval(data['Cities'][j], gloab))
            data['Universities'][i] = str(eval(data['Universities'][i], gloab) + eval(data['Universities'][j], gloab))
            data['Departments'][i] = str(eval(data['Departments'][i], gloab) + eval(data['Departments'][j], gloab))
            data['Years'][i] = str(eval(data['Years'][i], gloab) + eval(data['Years'][j], gloab))
            data['CitationNums'][i] = int(data['CitationNums'][i]) + int(data['CitationNums'][j])
            data['EstimateCitation'][i] = int(data['EstimateCitation'][i]) + int(data['CitationNums'][j])
            data['paperNums'][i] = int(data['paperNums'][i])+int(data['paperNums'][j])
            #data = data.drop([j], axis=0)
            ll.append(j)
            print(data.iloc[i])
            print(data.iloc[j])
        else:
             continue
ll = set(ll)
ll = list(ll)
print(len(ll))
data = data.drop(index=ll)
data = data.reset_index(drop=True)
print(len(data))

data.to_csv('new_information-final.csv', encoding='utf-8-sig', index=0)
