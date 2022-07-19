from algorithm.GmmImprove import gmm_final
from algorithm.LeachImprove import leach_final
from algorithm.SCImprove import sc_final
import matplotlib.pyplot as plt

from algorithm.WCAImprove import wca_final


def paint_packet_and_uavspeed():
    colors = ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3', '#999999', '#e41a1c', '#6b5152', '#a29988', '#7a7281', '#c7b8a1']
    # 画图
    fontsize = 8
    y_sc = [123047.24805919283, 117879.24189050304, 111743.09844404004, 107167.74982021088, 102739.44111117622, 97312.1149744299, 91945.1191267059]
    y_gmm = [118825.59827851377, 112615.65907818447, 105649.56985073691, 100532.28395236397, 95192.05067408657, 89759.26661184031, 85264.73363917014]
    y_wca = [93241.68729794382, 86997.0795437032, 82392.4567498085, 72826.73097814446, 66727.51032360375, 61199.39594265959, 59910.46146736318]
    y_leach = [107067.79744042184, 98318.14136926254, 90228.63307971132, 80954.94754789025, 73334.04673416096, 67318.95967717958, 62584.73665988883]

    x = [10, 15, 20, 25, 30, 35, 40]
    plt.plot(x, y_sc, markersize=fontsize, label="SpectralClustering", marker='o')
    plt.plot(x, y_gmm, markersize=fontsize, label="GMM", marker='s')
    plt.plot(x, y_wca, markersize=fontsize, label="WCA", marker='*')
    plt.plot(x, y_leach, markersize=fontsize, label="LEACH", marker='^')

    # _xtick_labels = ["{}year".format(i) for i in x]
    # plt.xticks(x, x)
    plt.xlabel("The speed of UAVs (m/s)")
    plt.ylabel("The number of bit (M)")
    plt.grid()
    plt.legend()
    plt.savefig('./picture/PacketAndUAVspeed.eps', dpi=600)
    plt.show()


paint_packet_and_uavspeed()
