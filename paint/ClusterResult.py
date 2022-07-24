import matplotlib.pyplot as plt

from algorithm.SCImprove import sc_final
from network import generate_uav


def paint_init_cluster(uavs, filepath):
    # 画图
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = []
    y = []
    z = []
    # 无人机散点
    for uav in uavs:
        uav_pos = uav.current_position.tolist()
        x.append(uav_pos[0])
        y.append(uav_pos[1])
        z.append(uav_pos[2])
        # label = "cluster"+str(uav.cluster_id)
    ax.scatter(x, y, z, c="#965454", s=50)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    # plt.legend()
    plt.savefig(filepath, dpi=600)
    plt.show()


def paint_final_cluster(cluster_result, filepath):
    colors = ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3', '#999999', '#e41a1c', '#6b5152', '#a29988', '#7a7281', '#c7b8a1']
    # 画图
    speed = 10
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for uav_cluster in cluster_result:
        x = []
        y = []
        z = []
        for uav in uav_cluster:
            uav_pos = uav.current_position.tolist()
            # 簇头单独表示
            if uav.uav_id == uav.cluster_head_id:
                ax.scatter(uav_pos[0], uav_pos[1], uav_pos[2], c=colors[uav.cluster_id], marker="*", s=60)
                continue
            x.append(uav_pos[0])
            y.append(uav_pos[1])
            z.append(uav_pos[2])
            # uav_speed = uav.current_speed.tolist()
            # uav_speed_max = 4
            # ax.quiver(uav_pos[0], uav_pos[1], uav_pos[2], uav_speed[0]/uav_speed_max, uav_speed[1]/uav_speed_max, uav_speed[2]/uav_speed_max, color='black', lw=1, arrow_length_ratio=0.5)
        label = "cluster"+str(uav_cluster[0].cluster_id)
        ax.scatter(x, y, z, c=colors[uav_cluster[0].cluster_id], label=label, s=50)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.legend(loc=6, fontsize='xx-small')
    plt.savefig(filepath, dpi=600)
    plt.show()


if __name__ == '__main__':
    # 无人机总数
    uav_num = 100
    paint_init_cluster(generate_uav(uav_num), "./picture/clusterresult(num="+str(uav_num)+",max=0).eps")

    # 每个簇最大的数
    n_max = 15
    cluster_result, all_uav_number_packet = sc_final(uav_num, n_max)
    paint_final_cluster(cluster_result, "./picture/clusterresult(num="+str(uav_num)+",max="+str(n_max)+").eps")

    # 每个簇最大的数
    n_max = 20
    cluster_result, all_uav_number_packet = sc_final(uav_num, n_max)
    paint_final_cluster(cluster_result, "./picture/clusterresult(num="+str(uav_num)+",max="+str(n_max)+").eps")

    # 每个簇最大的数
    n_max = 25
    cluster_result, all_uav_number_packet = sc_final(uav_num, n_max)
    paint_final_cluster(cluster_result, "./picture/clusterresult(num="+str(uav_num)+",max="+str(n_max)+").eps")
