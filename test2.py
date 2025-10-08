# 获取所有distribution1
from data_service import data_service_cable
from data_service import data_service_nap

list_d1 = data_service_cable.get_all_distribution_1()
if list_d1 is not None and not list_d1.empty:
    # 遍历每行数据
    for i, d1 in list_d1.iterrows():
        code = d1["code"]
        list_pass = data_service_nap.get_all_points_on_cable(code)
        if list_pass is not None and not list_pass.empty:
            for j, _pass in list_pass.iterrows():

                print("%s %s %s %s %s" % (_pass["cable_code"], _pass["class"], str(_pass["in_start"]), str(_pass["in_end"]), _pass["skip_count"]))