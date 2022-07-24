from algorithm.GmmImprove import gmm_final
from algorithm.LeachImprove import leach_final
from algorithm.SCImprove import sc_final
import matplotlib.pyplot as plt

from algorithm.WCAImprove import wca_final


def paint_clusternum_and_uavnum_single():
    colors = ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3', '#999999', '#e41a1c', '#6b5152', '#a29988', '#7a7281', '#c7b8a1']
    # 画图
    uav_num = 100
    speed = 20
    fontsize = 8
    y_a = []
    y_b = []
    y_c = []
    y_d = []

    x = [50, 100, 150, 200, 250, 300, 350]
    for uav_num in range(50, 400, 50):
        sc_cluster_result_a, sc_all_uav_number_packet_a = sc_final(uav_num, 10)
        sc_cluster_result_b, sc_all_uav_number_packet_b = sc_final(uav_num, 15)
        sc_cluster_result_c, sc_all_uav_number_packet_c = sc_final(uav_num, 20)
        sc_cluster_result_d, sc_all_uav_number_packet_d = sc_final(uav_num, 25)
        y_a.append(len(sc_cluster_result_a))
        y_b.append(len(sc_cluster_result_b))
        y_c.append(len(sc_cluster_result_c))
        y_d.append(len(sc_cluster_result_d))
    plt.plot(x, y_a, markersize=fontsize, label="n_max=10", marker='o')
    plt.plot(x, y_b, markersize=fontsize, label="n_max=15", marker='s')
    plt.plot(x, y_c, markersize=fontsize, label="n_max=20", marker='*')
    plt.plot(x, y_d, markersize=fontsize, label="n_max=25", marker='^')

    # _xtick_labels = ["{}year".format(i) for i in x]
    # plt.xticks(x, x)
    plt.xlabel("The number of UAVs")
    plt.ylabel("The number of clusters")
    plt.grid()
    plt.legend()
    plt.savefig('./picture/ClusternumAndUAVnumsingle.eps', dpi=600)
    plt.show()


paint_clusternum_and_uavnum_single()
