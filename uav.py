import numpy as np
import argparse
import random


def set_uav_param(uav_id):
    # 为了保证无人机随机且固定
    random.seed(uav_id)
    parser = argparse.ArgumentParser()
    # 通信距离（常数）
    # parser.add_argument('--communication_range', type=float, default=400, help='communication_range of uav')
    # 当前速度
    speed = 15
    parser.add_argument('--current_speed', type=list, default=[random.uniform(-1, 1)*speed, random.uniform(-1, 1)*speed, random.uniform(-1, 1)*speed], help='speed of uav at current time')
    # 当前位置
    parser.add_argument('--current_position', type=list, default=[random.random()*2000, random.random()*2000, random.random()*50+100], help='position of uav')
    # 上一时刻速度，用于计算上一时刻位置
    parser.add_argument('--latter_speed', type=list, default=[random.uniform(-1, 1)*20, random.uniform(-1, 1)*20, random.uniform(-1, 1)*20], help='speed of uav at latter time')
    # 簇头还是成员
    parser.add_argument('--state', type=str, default="CM", help='state of uav, CH or CM')
    # 簇头节点id
    parser.add_argument('--cluster_id', type=int, default=-1, help='cluster id')
    parser.add_argument('--cluster_head_id', type=int, default=-1, help='cluster head uav id')
    # 邻居节点有哪些
    parser.add_argument('--neighbor', type=list, default=[], help='neighbor of uav')
    arg = parser.parse_args()
    return arg


class UAV:
    def __init__(self, uav_id, uav_args):
        # 每个无人机id不一样，单独给
        self.uav_id = uav_id  # 无人机ID
        # 大部分一样的参数
        # self.communication_range = uav_args.communication_range  # 通信距离
        self.current_speed = np.array(uav_args.current_speed)  # 无人机速度（三维坐标）
        self.latter_speed = np.array(uav_args.latter_speed)  # 无人机上一时刻速度（三维坐标）
        self.state = uav_args.state  # 状态（簇头还是普通成员）
        self.cluster_id = uav_args.cluster_id  # 簇的ID
        self.cluster_head_id = uav_args.cluster_head_id  # 簇头的ID
        self.current_position = np.array(uav_args.current_position)  # 位置（三维坐标）
        self.latter_position = self.current_position - self.latter_speed  # 上一时刻位置（三维坐标）
        self.neighbor = uav_args.neighbor

    def is_cluster_head(self):
        """
        判断该无人机是不是簇头
        :return:
        """
        if self.uav_id == self.cluster_head_id:
            self.state = "CH"
        else:
            self.state = "CM"
