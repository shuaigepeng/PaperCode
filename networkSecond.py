import copy

from algorithm.GmmImprove import gmm_final_new, gmm_final
from algorithm.LeachImprove import leach_final_new, leach_final
from algorithm.SCImprove import sc_final, sc_final_new
from algorithm.WCAImprove import wca_final_new, wca_final
from network import set_network_param, generate_uav, get_adj_matrix, cal_number_packet


def get_next_position(cluster_result, net_args):
    for result in cluster_result:
        for uav in result:
            uav.current_speed += uav.current_speed * net_args.slot
    return cluster_result


def check_outlier(cluster_result, net_args):
    outlier_list = []
    for result in cluster_result:
        cluster_head_id = result[0].cluster_head_id
        adj = get_adj_matrix(result, net_args)
        cluster_line = -1
        # 找簇头
        for i in range(len(result)):
            if result[i].uav_id == cluster_head_id:
                cluster_line = i
                break
        for i in range(len(adj[cluster_line])):
            if i != cluster_line and adj[cluster_line][i] == 0:
                result[i].cluster_id = -1
                result[i].cluster_head_id = -1
                outlier_list.append(result[i])
                result.remove(result[i])
        return cluster_result, outlier_list


def change_cluster(cluster_result, outlier_list, net_args):
    outlier_list_copy = copy.deepcopy(outlier_list)
    cluster_result_copy = copy.deepcopy(cluster_result)
    cluster_result_line = [uav for result in cluster_result_copy for uav in result]
    for outlier in outlier_list:
        maxPacket = 0
        # 投敌过程
        for uav in cluster_result_line:
            packet = cal_number_packet(outlier, uav, net_args)
            if packet > maxPacket:
                outlier.cluster_id = uav.cluster_id
                outlier.cluster_head_id = uav.cluster_head_id
        # 添加孤立点，簇号就是行号
        cluster_result[outlier.cluster_id].append(outlier)
        outlier_list_copy.remove(outlier)
    return cluster_result, outlier_list_copy


uav_num = 100
n_max = 20
net_args = set_network_param()
uav_list = generate_uav(uav_num)
# 分簇
cluster_result, all_uav_number_packet = gmm_final(100, 20)
# 下一时刻
cluster_result = get_next_position(cluster_result, net_args)
# 孤立点
cluster_result, outlier_list = check_outlier(cluster_result, net_args)
# 投敌
while len(outlier_list) != 0:
    cluster_result, outlier_list = change_cluster(cluster_result, outlier_list, net_args)
# 小范围SC
cluster_result_new = []
for result in cluster_result:
    cluster_results, all_uav_number_packet = gmm_final_new(result, n_max, net_args)
    for cluster_result in cluster_results:
        cluster_result_new.append(cluster_result)
print(cluster_result_new)
