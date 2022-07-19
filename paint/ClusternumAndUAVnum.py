from algorithm.GmmImprove import gmm_final
from algorithm.LeachImprove import leach_final
from algorithm.SCImprove import sc_final
import matplotlib.pyplot as plt

from algorithm.WCAImprove import wca_final


def paint_clusternum_and_uavnum():
    colors = ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3', '#999999', '#e41a1c', '#6b5152', '#a29988', '#7a7281', '#c7b8a1']
    # 画图
    fontsize = 8
    y_sc = []
    y_gmm = []
    y_wca = []
    y_leach = []
    n_max = 10

    x = [50, 100, 150, 200, 250, 300, 350]
    for uav_num in range(50, 400, 50):
        sc_cluster_result, sc_all_uav_number_packet = sc_final(uav_num, n_max)
        gmm_cluster_result, gmm_all_uav_number_packet = gmm_final(uav_num, n_max)
        wca_cluster_result, wca_all_uav_number_packet = wca_final(uav_num, n_max)
        leach_cluster_result, leach_all_uav_number_packet = leach_final(uav_num, n_max)
        y_sc.append(len(sc_cluster_result))
        y_gmm.append(len(gmm_cluster_result))
        y_wca.append(len(wca_cluster_result))
        y_leach.append(len(leach_cluster_result))
    plt.plot(x, y_sc, markersize=fontsize, label="SpectralClustering", marker='o')
    plt.plot(x, y_gmm, markersize=fontsize, label="GMM", marker='s')
    plt.plot(x, y_wca, markersize=fontsize, label="WCA", marker='*')
    plt.plot(x, y_leach, markersize=fontsize, label="LEACH", marker='^')

    # _xtick_labels = ["{}year".format(i) for i in x]
    # plt.xticks(x, x)
    plt.xlabel("The number of UAVs")
    plt.ylabel("The number of cluster")
    plt.grid()
    plt.legend()
    plt.savefig('./picture/ClusternumAndUAVnum.eps', dpi=600)
    plt.show()


paint_clusternum_and_uavnum()
