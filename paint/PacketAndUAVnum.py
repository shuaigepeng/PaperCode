from algorithm.KmeansImprove import kmeans_final
from algorithm.SCImprove import sc_final
import matplotlib.pyplot as plt


def paint_packet_and_uavnum():
    colors = ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3', '#999999', '#e41a1c', '#6b5152', '#a29988', '#7a7281', '#c7b8a1']
    # 画图
    fontsize = 13
    y_sc = []
    y_kmeans = []
    y_fcm = []
    n_max = 20
    x = [50, 100, 150, 200, 250, 300, 350]
    for uav_num in range(50, 400, 50):
        sc_cluster_result, sc_all_uav_number_packet = sc_final(uav_num, n_max)
        kmeans_cluster_result, kmeans_all_uav_number_packet = kmeans_final(uav_num, n_max)
        y_sc.append(sc_all_uav_number_packet)
        y_kmeans.append(kmeans_all_uav_number_packet)

    plt.plot(x, y_sc, markersize=fontsize, label="SpectralClustering", marker='o')
    plt.plot(x, y_kmeans, markersize=fontsize, label="KMeans", marker='s')
    plt.plot(x, y_sc, markersize=fontsize, label="FCM", marker='*')

    # _xtick_labels = ["{}year".format(i) for i in x]
    # plt.xticks(x, x)
    plt.xlabel("The number of UAVs")
    plt.ylabel("The number of packet")
    plt.grid()
    plt.legend()
    # plt.savefig('./picture/PacketAndUAVnum.eps', dpi=600)
    plt.show()


paint_packet_and_uavnum()
