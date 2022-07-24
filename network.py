import uav
import math
import numpy as np
import argparse


def set_network_param():
    parser = argparse.ArgumentParser()
    parser.add_argument('--alpha', type=float, default=4, help='path_loss_exponent')
    parser.add_argument('--power', type=float, default=20, help='transmission_power(dbm)')
    parser.add_argument('--sigma', type=float, default=-100, help='noise_power(dbm)')
    parser.add_argument('--gain', type=float, default=0.5, help='power_gain')
    parser.add_argument('--bandwidth', type=float, default=10, help='bandwidth(MHz)')
    parser.add_argument('--slot', type=float, default=30, help='slot')
    parser.add_argument('--gamma', type=float, default=0, help='SINR threshold(db)')
    parser.add_argument('--l', type=float, default=500, help='the size of a packet(bit)')
    arg = parser.parse_args()
    return arg


def normalize(data):
    m = max([max(i) for i in data])
    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] /= m
    return data


def generate_uav(uav_num):
    """
    生成指定数量的随机且固定的无人机集合
    :param uav_num: 无人机数量
    :return: 无人机集合
    """
    uav_list = []
    for uav_id in range(uav_num):
        uav_args = uav.set_uav_param(uav_id)
        new_uav = uav.UAV(uav_id, uav_args)
        uav_list.append(new_uav)
    # print("无人机构建完成，数目为", uav_num)
    return uav_list


def cal_dis(uav_i, uav_j):
    """
    计算任意两架无人机之间的距离
    :param uav_i: 无人机i
    :param uav_j: 无人机j
    :return: 距离
    """
    distance = (sum([i ** 2 for i in (uav_i.current_position - uav_j.current_position)])) ** 0.5
    return distance


def dbm_to_w(power):
    """
    分贝和瓦的转换
    :param power: 功率（分贝）
    :return: 功率（瓦）
    """
    # 1w=1000mw=10lg1000dbm=30dbm
    return 0.001*math.pow(10, power/10)


def db_to_ratio(power):
    """
    分贝和比例的转换
    :param power: 功率（分贝）
    :return: 功率（瓦）
    """
    # 1db=10lg(p1/p2)
    return math.pow(10, power/10)


def cal_SINR(uav_i, uav_j, net_args):
    """
    计算SINR
    :param net_args: 网络参数
    :param uav_i: 无人机i
    :param uav_j: 无人机j
    :return: SINR值
    """
    alpha = net_args.alpha  # path_loss_exponent
    p = dbm_to_w(net_args.power)  # transmission_power 20dbm
    sigma = dbm_to_w(net_args.sigma)  # noise_power -100dbm
    h = net_args.gain  # power_gain
    d = cal_dis(uav_i, uav_j)  # distance
    sinr = (p*h)/(sigma*(d**alpha))
    return sinr


def cal_channel_capacity(uav_i, uav_j, net_args):
    """
    香农公式，计算信道容量
    :param net_args: 网络参数
    :param uav_i: 无人机i
    :param uav_j: 无人机j
    :return: 信道容量
    """
    b = net_args.bandwidth  # bandwidth
    return b*math.log(1+cal_SINR(uav_i, uav_j, net_args), 10)


def cal_communication_range(net_args):
    """
    假定无人机的硬件设施和通信环境都相同，那么通信距离应该是一样的
    :param net_args: 网络参数
    :return: 通信距离
    """
    alpha = net_args.alpha  # path_loss_exponent
    p = dbm_to_w(net_args.power)  # transmission_power 20dbm
    sigma = dbm_to_w(net_args.sigma)  # noise_power -100dbm
    h = net_args.gain  # power_gain
    gamma = db_to_ratio(net_args.gamma)  # SINR threshold
    communication_range = math.pow(p * h / (gamma * sigma), 1 / alpha)
    return communication_range


def cal_link_time(uav_i, uav_j, net_args):
    """
    计算时隙内连接时间
    :param uav_i: 无人机i
    :param uav_j: 无人机j
    :param net_args: 网络参数
    :return: 连接时间
    """
    communication_range = cal_communication_range(net_args)
    # 时隙长度
    slot = net_args.slot
    # 本时刻位置差
    delta_current_position_vector = uav_i.current_position - uav_j.current_position
    delta_current_position = (sum([i ** 2 for i in delta_current_position_vector])) ** 0.5
    # 上时刻位置差
    delta_latter_position_vector = uav_i.latter_position - uav_j.latter_position
    delta_latter_position = (sum([i ** 2 for i in delta_latter_position_vector])) ** 0.5
    # 前后做差，判断趋势
    delta_position = delta_current_position - delta_latter_position
    # 相对速度
    relative_speed_vector = uav_i.current_speed - uav_j.current_speed
    relative_speed = abs(np.dot(delta_current_position_vector, relative_speed_vector) / delta_current_position)
    link_time = 0
    if delta_position > 0:
        link_time = (communication_range - delta_current_position) / relative_speed
        link_time = link_time if link_time < slot else slot
    elif delta_position < 0:
        link_time = (communication_range + delta_current_position) / relative_speed
        link_time = link_time if link_time < slot else slot
    return link_time


def cal_energy(uav_i, uav_j, net_args):
    E_elec = 50 * math.pow(10, -9)
    E_fs = 10 * math.pow(10, -12)
    l = 1
    energy = l*E_elec + l*E_fs*cal_dis(uav_i, uav_j)
    return energy


def cal_preference(uav_i, uav_j, net_args):
    communication_range = cal_communication_range(net_args)
    E_elec = 50 * math.pow(10, -9)
    E_fs = 10 * math.pow(10, -12)
    l = 1
    energy_measure = l*E_elec + l*E_fs*communication_range

    # 可调节因子
    beta = 0.5
    # 时隙长度
    slot = net_args.slot

    link_time = cal_link_time(uav_i, uav_j, net_args)
    stability_preference_factor = link_time/slot

    energy = cal_energy(uav_i, uav_j, net_args)
    cost_preference_factor = energy/energy_measure
    # 加权
    preference_factor = beta*stability_preference_factor+(1-beta)*cost_preference_factor
    return preference_factor


def cal_number_packet(uav_i, uav_j, net_args):
    n = cal_channel_capacity(uav_i, uav_j, net_args)
    n *= cal_link_time(uav_i, uav_j, net_args)
    # n *= cal_PER(uav_i, uav_j, net_args)
    n *= cal_preference(uav_i, uav_j, net_args)
    # n /= math.pow(10, 6)
    # n = math.floor(n)
    return n


def get_weight_matrix(uavs, net_args):
    """
    邻接矩阵、权重系数矩阵
    :param uavs: 无人机集合
    :param net_args: 网络参数
    :return: 邻接矩阵和权重矩阵
    """
    gamma = db_to_ratio(net_args.gamma)  # threshold 0dbm
    weight_matrix = np.zeros([len(uavs), len(uavs)])
    for i in range(len(uavs)):
        for j in range(len(uavs)):
            if i != j:
                sinr = cal_SINR(uavs[i], uavs[j], net_args)
                # 只有信噪比满足条件，才建立连接
                if sinr > gamma:
                    # 连边的权重值
                    weight_matrix[i][j] = cal_number_packet(uavs[i], uavs[j], net_args)
    # print("生成权重系数矩阵")
    normalize(weight_matrix)
    return weight_matrix


def get_real_weight_matrix(uavs, net_args):
    """
    邻接矩阵、权重系数矩阵
    :param uavs: 无人机集合
    :param net_args: 网络参数
    :return: 邻接矩阵和权重矩阵
    """
    gamma = db_to_ratio(net_args.gamma)  # threshold 0dbm
    weight_matrix = np.zeros([len(uavs), len(uavs)])
    for i in range(len(uavs)):
        for j in range(len(uavs)):
            if i != j:
                sinr = cal_SINR(uavs[i], uavs[j], net_args)
                # 只有信噪比满足条件，才建立连接
                if sinr > gamma:
                    # 连边的权重值（误报率？正确的包数目？信噪比？信道容量？总比特数？）
                    # weight_matrix[i][j] = cal_PER(uavs[i], uavs[j], net_args)
                    # weight_matrix[i][j] = cal_channel_capacity(uavs[i], uavs[j], net_args)*cal_link_time(uavs[i], uavs[j], net_args)
                    weight_matrix[i][j] = cal_number_packet(uavs[i], uavs[j], net_args)
                    # weight_matrix[i][j] = cal_link_time(uavs[i], uavs[j], net_args)
    # print("生成权重系数矩阵")
    return weight_matrix


def get_adj_matrix(uavs, net_args):
    """
    邻接矩阵、权重系数矩阵
    :param uavs: 无人机集合
    :param net_args: 网络参数
    :return: 邻接矩阵和权重矩阵
    """
    gamma = db_to_ratio(net_args.gamma)  # threshold 0dbm
    adj_matrix = np.zeros([len(uavs), len(uavs)])
    for i in range(len(uavs)):
        for j in range(len(uavs)):
            if i != j:
                sinr = cal_SINR(uavs[i], uavs[j], net_args)
                # 只有信噪比满足条件，才建立连接
                if sinr > gamma:
                    adj_matrix[i][j] = 1
    # print("生成邻接矩阵")
    return adj_matrix


if __name__ == '__main__':
    uav_num = 100
    n_max = 20
    net_args = set_network_param()
    uav_list = generate_uav(uav_num)
    print("生成权重系数矩阵")
    weight = get_weight_matrix(uav_list, net_args)
    print(weight)
    print(np.sum(np.array(weight), axis=1))
    print("生成邻接矩阵")
    adj = get_adj_matrix(uav_list, net_args)
    print(adj)
    a = np.sum(np.array(adj), axis=1)
    print()
    gamma = db_to_ratio(net_args.gamma)  # threshold 0dbm
    link_matrix = np.zeros([len(uav_list), len(uav_list)])
    for i in range(len(uav_list)):
        for j in range(len(uav_list)):
            if i != j:
                sinr = cal_SINR(uav_list[i], uav_list[j], net_args)
                # 只有信噪比满足条件，才建立连接
                if sinr > gamma:
                    link_matrix[i][j] = cal_link_time(uav_list[i], uav_list[j], net_args)
    print(link_matrix)
    print()