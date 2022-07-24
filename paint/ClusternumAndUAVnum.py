from algorithm.GmmImprove import gmm_final
from algorithm.LeachImprove import leach_final
from algorithm.SCImprove import sc_final
import matplotlib.pyplot as plt
import numpy as np

from algorithm.WCAImprove import wca_final


def paint_clusternum_and_uavnum():
    colors = ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3', '#999999', '#e41a1c', '#6b5152', '#a29988', '#7a7281', '#c7b8a1']
    # 画图
    fontsize = 8
    uav_num = 100
    n_max = 15
    speed = 20

    y_sc = []
    sc_cluster_result, sc_all_uav_number_packet = sc_final(uav_num, n_max)
    for cluster in sc_cluster_result:
        y_sc.append(len(cluster))

    y_gmm = []
    gmm_cluster_result, gmm_all_uav_number_packet = gmm_final(uav_num, n_max)
    for cluster in gmm_cluster_result:
        y_gmm.append(len(cluster))

    y_wca = []
    wca_cluster_result, wca_all_uav_number_packet = wca_final(uav_num, n_max)
    for cluster in wca_cluster_result:
        y_wca.append(len(cluster))

    y_leach = []
    leach_cluster_result, leach_all_uav_number_packet = leach_final(uav_num, n_max)
    for cluster in leach_cluster_result:
        y_leach.append(len(cluster))

    y = [y_sc, y_gmm, y_wca, y_leach]
    y = np.array(y).T

    x = ["FSC", "GMM", "WCA", "LEACH"]
    plt.boxplot(y,
                labels=x,  # 为箱线图添加标签，类似于图例的作用
                # sym="r",  # 异常点形状，默认为蓝色的“+”
                showmeans=True  # 是否显示均值，默认不显示
                )
    # _xtick_labels = ["{}year".format(i) for i in x]
    # plt.xticks(x, x)
    plt.xlabel("Cluster algorithm")
    plt.ylabel("The number of clusters")
    plt.grid(True)
    # plt.legend()
    plt.savefig('./picture/ClusternumAndUAVnum.eps', dpi=600)
    plt.show()


paint_clusternum_and_uavnum()
