# 获取所有distribution1
from data_service import data_service_cable
from data_service import data_service_nap


# list_d1 = data_service_cable.get_all_distribution_1()
# if list_d1 is not None and not list_d1.empty:
#     # 遍历每行数据
#     for i, d1 in list_d1.iterrows():
#         code = d1["code"]
#         list_pass = data_service_nap.get_all_points_on_cable(code)
#         if list_pass is not None and not list_pass.empty:
#             for j, _pass in list_pass.iterrows():
#
#                 print("%s %s %s %s %s" % (_pass["cable_code"], _pass["class"], str(_pass["in_start"]), str(_pass["in_end"]), _pass["skip_count"]))

# sro_list = data_service_nap.get_all_SRO_points()
# if sro_list is not None and not sro_list.empty:
#     for i, sro in sro_list.iterrows():
#         print(f'nap code: {sro["nap_code"]}')
#         d1_list = data_service_cable.get_all_distribution_start_with_SRO(sro["nap_code"])
#         if d1_list is not None and not d1_list.empty:
#             for j, d1 in d1_list.iterrows():
#                 print(d1['code'])
#                 passes_on_d1 = data_service_nap.get_all_passes_on_d1(d1['code'])
#                 if passes_on_d1 is not None and not passes_on_d1.empty:
#                     for k, d1_pass in passes_on_d1.iterrows():
#
#                         print(f"nap code: {d1_pass['nap_code']},in_start: {d1_pass['in_start']},in_end: {d1_pass['in_end']}")

# 所有SRO的点skip_count都设置为0
data_service_nap.init_skip_count_as_zero_of_all_SRO_points()

# 所有distribution1类型的skip_count都设置为0