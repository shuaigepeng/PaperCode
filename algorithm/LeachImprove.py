from sklearn.cluster import KMeans
import math
from network import set_network_param, generate_uav, get_adj_matrix, cal_SINR, db_to_ratio, get_real_weight_matrix
import numpy as np


def combine_list(cluster_result, cluster_part):
    """
    拆完簇和原簇合并
    :param cluster_result: 总结果
    :param cluster_part: 新结果
    :return: 总结果
    """
    for result in cluster_part:
        cluster_result.append(result)
    return cluster_result


def get_count(cluster_result):
    """
    计数，符合条件的簇有几个
    :param cluster_result: 分簇结果
    :return: 计数
    """
    return len(cluster_result)


def delete_empty_line(lists):
    """
    模糊聚类后出现空行（无奈），只能删了
    :param lists: 分簇结果
    :return: 去除空行
    """
    lists = [line for line in lists if len(line) != 0]
    return lists


def get_cluster_id(cluster_result):
    for cluster_id in range(len(cluster_result)):
        for uav in cluster_result[cluster_id]:
            uav.cluster_id = cluster_id
    return cluster_result


def update_neighbor_in_cluster(cluster_result, net_args):
    """
    同一个簇内有多少节点
    :param cluster: 簇
    :param net_args: 参数
    :return: 更新后的簇
    """
    gamma = db_to_ratio(net_args.gamma)  # threshold 0dbm
    for cluster in cluster_result:
        for i in range(len(cluster)):
            # 清空原有簇成员
            cluster[i].neighbor.clear()
            for j in range(len(cluster)):
                if i != j:
                    sinr = cal_SINR(cluster[i], cluster[j], net_args)
                    if sinr > gamma:
                        cluster[i].neighbor.append(cluster[j])
    return cluster_result


def is_has_candidate_head(cluster, net_args):
    a = get_adj_matrix(cluster, net_args)
    b = np.sum(np.array(a), axis=0)
    for i in range(len(cluster)):
        # 至少保证一个点是可以当做簇头的
        if len(cluster[i].neighbor) == len(cluster)-1:
            return True
    return False


def kmeans_plus(uav_list, k):
    """

    :param uav_list: 无人机集合
    :return: 分簇结果
    """
    np.random.seed(1)
    H = []
    for uav in uav_list:
        H.append(uav.current_position)
    sc = KMeans(n_clusters=k).fit(H).labels_
    result = [[] * k for _ in range(k)]
    for index in range(len(uav_list)):
        cluster_id = sc[index]
        result[cluster_id].append(uav_list[index])
    return result


def split_cluster(cluster_result, n_max, net_args):
    """
    拆簇
    :param cluster_result: 分簇总结果
    :param n_max: 簇内最大
    :return: 分簇合并后的新结果
    """
    for uavs_part in cluster_result:
        # 是否超过最大值
        if len(uavs_part) > n_max:
            uavs_part_tmp = uavs_part
            cluster_result.remove(uavs_part)
            result = kmeans_plus(uavs_part_tmp, int(math.ceil(len(uavs_part)/n_max)))
            # 删除空簇
            result = delete_empty_line(result)
            cluster_result = combine_list(cluster_result, result)
            return cluster_result
        # 判断有没有能成为簇头的存在
        if not is_has_candidate_head(uavs_part, net_args):
            uavs_part_tmp = uavs_part
            cluster_result.remove(uavs_part)
            result = kmeans_plus(uavs_part_tmp, 2)
            # 删除空簇
            result = delete_empty_line(result)
            cluster_result = combine_list(cluster_result, result)
            return cluster_result
    return cluster_result


def select_cluster_head(cluster_result, net_args):
    """
    选簇头，求整个网络的数据包数
    :param cluster_result: 分簇结果
    :param net_args: 网络参数
    :return:
    """
    all_uav_number_packet = 0
    for cluster in cluster_result:
        # 每一行就是一个簇
        real_weight_matrix = get_real_weight_matrix(cluster, net_args)
        max_cluster_number_packet = 0
        cluster_head_id = -1
        for i in range(len(cluster)):
            if len(cluster[i].neighbor) == len(cluster)-1:
                cluster_number_packet = sum(real_weight_matrix[i])
                max_cluster_number_packet = cluster_number_packet
                cluster_head_id = cluster[i].uav_id
        for uav in cluster:
            if uav.uav_id == cluster_head_id:
                uav.state = "CH"
            uav.cluster_head_id = cluster_head_id
        all_uav_number_packet += max_cluster_number_packet
    return cluster_result, all_uav_number_packet


def leach_final(uav_num, n_max):
    print("leach:")
    # # 无人机总数
    # uav_num = 100
    # # 每个簇最大的数
    # n_max = 20
    net_args = set_network_param()
    # 无人机集合
    uav_list = generate_uav(uav_num)
    # 初始化分簇结果
    cluster_result = [uav_list]
    # 更新簇内邻居
    cluster_result = update_neighbor_in_cluster(cluster_result, net_args)
    cluster_result = split_cluster(cluster_result, n_max, net_args)
    # 更新簇内邻居
    cluster_result = update_neighbor_in_cluster(cluster_result, net_args)
    # count当作标记，判断是否符合要求，最后的count就是分簇数了
    count = 1  # 第一次分簇后为2，所以一定进循环
    while count != len(cluster_result):
        # 更新count。如果后面不继续分簇，跳出循环
        count = get_count(cluster_result)
        # 大簇分小簇，每次只分一个
        cluster_result = split_cluster(cluster_result, n_max, net_args)
        # 更新簇内邻居
        cluster_result = update_neighbor_in_cluster(cluster_result, net_args)
    # 簇号
    cluster_result = get_cluster_id(cluster_result)
    # print(cluster_result)

    # 选个簇头
    cluster_result, all_uav_number_packet = select_cluster_head(cluster_result, net_args)
    print("leach：", all_uav_number_packet)
    return cluster_result, all_uav_number_packet


if __name__ == '__main__':
    # # 无人机总数
    # uav_num = 100
    # # 每个簇最大的数
    # n_max = 20
    leach_final(100, 30)
