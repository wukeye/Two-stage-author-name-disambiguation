
import pandas as pd
import time



def over(coll):
    '''该函数功能是将同一姓名下每一个学者的学术圈子进行聚合，形成大的学术圈'''
# 例如：
# AB姓名下有10篇论文，
# 经过第一阶段消歧，
# 我们将10维列表中的每一维代表当前论文作者可能与哪些论文作者是同一个人。
# Input is:  比如第一个元素[1,2,3]代表：该姓名下第一篇论文的著者与第2，3篇论文的著者为同一人
#  [[1, 2, 3], [2, 3], [3], [4], [5, 6], [6, 7], [7], [8], [9, 10], [10]]
# Output is:    经过子学术圈的聚合之后，形成大学术圈，方便后续合并id
#  [[1, 2, 3], [4], [5, 6, 7], [8], [9, 10]]
    # print('Input is:\n', coll)
    for i in range(len(coll)):
        j = i+1
        while j < len(coll):
            k = list(set(coll[i])&set(coll[j]))
            if k != []:
                coll[i] = list(set(coll[i]+coll[j]))
                coll[j] = []
                j = j + 1
                continue
            j = j + 1
    index = [i for i, x in enumerate(coll) if x == []]
    x = 0
    for k in index:
        coll.pop(k-x)
        x = x+1
    # print('Output is:\n', coll)
    return coll



start = time.clock()
train = pd.read_excel("my_information_sort.xlsx", encoding='utf-8-sig', keep_default_na=False)
print(train.head(3))
author_name = set()

# 找出所有的同名异id的姓名
for i in range(len(train['AuthorName'])):
    if i <= 276122:
        if train['AuthorName'][i+1] == train['AuthorName'][i] and train['AuthorId'][i+1] != train['AuthorId'][i]:
            author_name.add(train['AuthorName'][i])

train_copy = train.copy()
print(len(author_name))


for item in author_name:
    # 构建该姓名下的index和Coauthor键值对
    Co = []
    for i in list(train_copy[train_copy['AuthorName'] == item]['Names_Coo']):
        Co.append(eval(i))
    index = list(train_copy[train_copy['AuthorName'] == item].index)
    print(train_copy.loc[index[0], ['AuthorName']].item())
    # 寻找可能是同一作者的行
    ll = [[]]*len(index)
    for i in range(len(index)):
        ll[i] = [i]
        j = i+1
        af = train_copy.loc[index[i], ['AffiliatesNor']].item()
        year = int(train_copy.loc[index[i], ['Year']].item())
        while j < len(index):

            # step1判断合作圈是否有overlap
            x = [x for x in Co[i] if x in Co[j]]
            if x:                                       # 如果有重合就加入需要合并的类
                ll[i].append(j)
                j = j + 1
                continue

            # step2判断affiliatesnor是否相同且年份是否相近
            if af and af == train_copy.loc[index[j], ['AffiliatesNor']].item():
                if year-2 <= int(train_copy.loc[index[j], ['Year']].item()) <= year+2:
                    ll[i].append(j)
                    j = j + 1
                    continue
            j = j + 1
    ll = over(ll)
    # 统一每一个学术圈的id
    for x in ll:
        id = train_copy.loc[index[x[0]], ['AuthorId']]
        for l in x:
            train_copy.loc[index[l], ['AuthorId']] = id




train_copy.to_csv('first_disambiguation_Result.csv', encoding='utf-8-sig', index=0)
end = time.clock()

print("final is in ", end - start)