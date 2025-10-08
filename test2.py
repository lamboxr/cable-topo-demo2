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



def update_skip_count_of_all_features():
    d1_list = data_service_cable.get_all_distribution_1()
    if d1_list is not None and not d1_list.empty:
        # 遍历每行数据
        for d1_idx, d1 in d1_list.iterrows():
            d1_code = d1["code"]
            d1_skip_count = d1["skip_count"]
            # 更新所有d1上的掏芯点的skip_count
            data_service_nap.update_skip_count_of_points_on_cable(d1_code, d1_skip_count)
            # 获取所有d1上的掏芯点
            cl_points = data_service_nap.get_all_points_on_cable(d1_code)
            if cl_points is not None and not cl_points.empty:
                for cl_idx, cl_point in cl_points.iterrows():
                    cl_code = cl_point["nap_code"]
                    cl_skip_count = cl_point["skip_count"]
                    # 更新d1上的掏芯点，分离出去的d2,d3线缆上的skip count
                    data_service_cable.update_skip_count_of_cable_start_with_point(cl_code, cl_skip_count)
                    # 获取所有d1上的掏芯点分出去的cable
                    d2_d3_list = data_service_cable.get_all_cable_start_with_one_point(cl_code)
                    if d2_d3_list is not None and not d2_d3_list.empty:
                        for d2_d3_idx, d2_d3 in d2_d3_list.iterrows():
                            d2_d3_code = d2_d3["code"]
                            d2_d3_skip_count = d2_d3["skip_count"]
                            # 更新d1上的掏芯点，分离出去的d2,d3线缆上所有掏芯点的skip count
                            data_service_nap.update_skip_count_of_points_on_cable(d2_d3_code, d2_d3_skip_count)
                            # 得到d1上的掏芯点，分离出去的d2,d3线缆上所有掏芯点
                            cl_points_on_d2_d3 = data_service_nap.get_all_points_on_cable(d2_d3_code)
                            if cl_points_on_d2_d3 is not None and not cl_points_on_d2_d3.empty:
                                for cl_on_d2_d3_idx, cl_on_d2_d3 in cl_points_on_d2_d3.iterrows():
                                    cl_code_on_d2_d3 = cl_on_d2_d3["nap_code"]
                                    cl_skip_count_on_d2_d3 = cl_on_d2_d3["skip_count"]
                                    data_service_cable.update_skip_count_of_cable_start_with_point(cl_code_on_d2_d3,
                                                                                                   cl_skip_count_on_d2_d3)


def init_skip_count():
    # 所有SRO的点skip_count都设置为0
    data_service_nap.init_skip_count_as_zero_of_all_SRO_points()

    # 所有distribution1类型的skip_count都设置为0
    data_service_cable.init_data_of_distribution_1()


def update_skip_count_start_with_one_point(nap_code, nap_skip_count):
    # 更新从单个点（起点、掏芯点、终点）上分离出去的所有子线缆上的skip count
    data_service_cable.update_skip_count_of_cable_start_with_point(nap_code, nap_skip_count)
    # 获取单个点（起点、掏芯点、终点）上分离出去的所有子线缆
    cable_list = data_service_cable.get_all_cable_start_with_one_point(nap_code)
    if cable_list is not None and not cable_list.empty:
        for _cable_idx, _cable in cable_list.iterrows():
            _cable_code = _cable["code"]
            _cable_skip_count = _cable["skip_count"]
            # 更在单个线缆（d1,d2,d3）上掏芯的所有点（closure,终点）的skip count
            data_service_nap.update_skip_count_of_points_on_cable(_cable_code, _cable_skip_count)
            # 获取在单个线缆（d1,d2,d3）上掏芯的所有点（closure,终点）
            nap_list = data_service_nap.get_all_points_on_cable(_cable_code)
            if nap_list is not None and not nap_list.empty:
                for _nap_idx, _nap in nap_list.iterrows():
                    _nap_code = _nap["nap_code"]
                    _nap_skip_count = _nap["skip_count"]
                    update_skip_count_start_with_one_point(_nap_code, _nap_skip_count)


def update_skip_count():
    all_sro_point = data_service_nap.get_all_SRO_points()
    if all_sro_point is not None and not all_sro_point.empty:
        for _sro_idx, _sro in all_sro_point.iterrows():
            _nap_code = _sro["nap_code"]
            _nap_skip_count = _sro["skip_count"]
            update_skip_count_start_with_one_point(_nap_code, _nap_skip_count)
"""==================主流程=================="""

# 更新所有distribution1线缆上的掏芯点上的skip_count值
if __name__ == '__main__':
    init_skip_count()
    update_skip_count()
