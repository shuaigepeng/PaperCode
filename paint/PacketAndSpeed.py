from algorithm.GmmImprove import gmm_final
from algorithm.LeachImprove import leach_final
from algorithm.SCImprove import sc_final
import matplotlib.pyplot as plt

from algorithm.WCAImprove import wca_final


def paint_packet_and_uavspeed():
    colors = ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3', '#999999', '#e41a1c', '#6b5152', '#a29988', '#7a7281', '#c7b8a1']
    # 画图
    fontsize = 8
    n_max = 20
    uav_num = 100
    y_sc = [61471.96563680397, 60441.80886453963, 59098.620928856995, 55892.90153644953, 54752.94909712451]
    y_gmm = [56850.36841260877, 55734.359653618216, 54503.4186772513, 52710.690356177554, 50642.3044232653]
    y_wca = [49844.89292434668, 50208.29118205166, 50197.35527449211, 48367.351679801744, 46137.161995296985]
    y_leach = [48632.883452318165, 47159.67230894316, 45385.804647722165, 43744.094405563475, 42224.48424015098]

    x = [15, 20, 25, 30, 35]
    plt.plot(x, y_sc, markersize=fontsize, label="FSC", marker='o')
    plt.plot(x, y_gmm, markersize=fontsize, label="GMM", marker='s')
    plt.plot(x, y_wca, markersize=fontsize, label="WCA", marker='*')
    plt.plot(x, y_leach, markersize=fontsize, label="LEACH", marker='^')

    _xtick_labels = [15, 20, 25, 30, 35]
    plt.xticks(x, x)
    plt.xlabel("The speed of UAVs (m/s)")
    plt.ylabel("The number of bits (M)")
    plt.grid()
    plt.legend()
    plt.savefig('./picture/PacketAndUAVspeed.eps', dpi=600)
    plt.show()


paint_packet_and_uavspeed()
