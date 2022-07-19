from algorithm.GmmImprove import gmm_final
from algorithm.LeachImprove import leach_final
from algorithm.SCImprove import sc_final
from algorithm.WCAImprove import wca_final

uavnum = 100
n_max = 15
cluster_result, all_uav_number_packet = sc_final(uavnum, n_max)
print(len(cluster_result))
# cluster_result, all_uav_number_packet = agglomerativeclustering_final(uavnum, n_max)
# print(len(cluster_result))
cluster_result, all_uav_number_packet = gmm_final(uavnum, n_max)
print(len(cluster_result))
cluster_result, all_uav_number_packet = wca_final(uavnum, n_max)
print(len(cluster_result))
cluster_result, all_uav_number_packet = leach_final(uavnum, n_max)
print(len(cluster_result))
