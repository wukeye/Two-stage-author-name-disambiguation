import pandas as pd
import numpy as np

def compute_pre_rec_f1(cluster_result, ground_truth_result):
    predict_label_dict = {}
    for i, item in enumerate(cluster_result):
        if item not in predict_label_dict.keys():
            predict_label_dict[item] = [i]
        else:
            predict_label_dict[item].append(i)

    true_label_dict = {}
    for i, item in enumerate(ground_truth_result):
        if item not in true_label_dict.keys():
            true_label_dict[item] = [i]
        else:
            true_label_dict[item].append(i)

    # compute cluster-level F1
    # let's denote C(r) as clustering result and T(k) as partition (ground-truth)
    # construct r * k contingency table for clustering purpose
    r_k_table = []
    # compare the result to construct the table
    for v1 in predict_label_dict.values():
        k_list = []
        for v2 in true_label_dict.values():
            N_ij = len(set(v1).intersection(v2))
            k_list.append(N_ij)  # see the overlapping part between truth and predict
        r_k_table.append(k_list)
    r_k_matrix = np.array(r_k_table)
    r_num = int(r_k_matrix.shape[0])
    print(r_k_matrix.shape)

    # compute F1 for each row C_i
    sum_f1 = 0.0
    sum_pre = 0.0
    sum_rec = 0.0
    for row in range(0, r_num):
        row_sum = np.sum(r_k_matrix[row, :])
        if row_sum != 0:
            max_col_index = np.argmax(r_k_matrix[row, :])
            row_max_value = r_k_matrix[row, max_col_index]
            prec = float(row_max_value) / row_sum
            col_sum = np.sum(r_k_matrix[:, max_col_index])
            rec = float(row_max_value) / col_sum
            row_f1 = float(2 * prec * rec) / (prec + rec)
            sum_f1 += row_f1
            sum_pre += prec
            sum_rec += rec
    average_f1 = float(sum_f1) / r_num
    average_pre = float(sum_pre) / r_num
    average_rec = float(sum_rec) / r_num

    return str(average_pre), str(average_rec), str(average_f1)


data = pd.read_excel("my_information_sort_labeled.xlsx", encoding='utf-8-sig', keep_default_na=False)
first_data = pd.read_csv("first-step\\first_disambiguation_Result.csv", encoding='utf-8-sig', keep_default_na=False)
second_data = pd.read_csv('second-step\\new_info_for_eval.csv', encoding='utf-8-sig', keep_default_na=False)
name = ['Zhiwei Li', 'Bing Su', 'Michael Cohen', 'A. Kundu', 'Elisa Ricci', 'En Zhu', 'Tim Oates', 'Javier Romero', 'Adam J. Grove', 'Malik Ghallab', 'A. Del Bimbo', 'N. Nandhakumar', 'A. Huertas', 'Wei Wang', 'Yang Zhao', 'E. Morales', 'Wei Pan', 'Qi Li', 'Xin Li', 'Zhe Li', 'Li Wang', 'Jie Zhang', 'Ning Xu', 'Li Zhang', 'Ke Xu', 'Hongtao Lu', 'He Wang']
for n in name:
    ground_truth = data[data['AuthorName'] == n][['AuthorId', 'labels', 'AffiliatesNor']].sort_values(by=['AffiliatesNor'])
    ground_truth_result = list(ground_truth['labels'])
    original_id = list(ground_truth['AuthorId'])
    p = first_data[first_data['AuthorName'] == n][['AuthorId', 'AffiliatesNor']].sort_values(by=['AffiliatesNor'])
    cluster_result = list(p['AuthorId'])
    s = second_data[second_data['AuthorName'] == n][['AuthorId', 'AffiliatesNor']].sort_values(by=['AffiliatesNor'])
    second_result = list(s['AuthorId'])
    print(len(second_result))
    p, r, f = compute_pre_rec_f1(original_id, ground_truth_result)
    print(n+"原始数据中的效果:precision "+p+" recall " + r + " f1 " + f)
    p, r, f = compute_pre_rec_f1(cluster_result, ground_truth_result)
    print(n+"一阶段消歧效果:precision "+p+" recall " + r + " f1 " + f)
    p, r, f = compute_pre_rec_f1(second_result, ground_truth_result)
    print(n+"二阶段消歧效果:precision "+p+" recall " + r + " f1 " + f)
