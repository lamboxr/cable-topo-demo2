from utils import gpkg_utils
from utils.gda_utils import LayerDGA


def _gda():
    gpkg_cable_path = gpkg_utils.get_gpkg_path("cable.gpkg")
    layer_name = "cable"
    cable_dga = LayerDGA(gpkg_cable_path, layer_name)
    return cable_dga


__gda = _gda()


def get_all_cables_start_with_one_point(nap_code):
    """
    获取指定点位为起点的所有线缆
    :param nap_code: 根据nap_code查询
    :return: 线缆列表
    """
    def custom_condition(gdf):
        return gdf["point_in_code"] == nap_code

    return __gda.get_features_by_condition(custom_condition)


def init_data_of_all_distribution01():
    """
    初始化所有sro节点的skip_count值为0，in_start为0
    """
    def custom_condition(gdf):
        return gdf["level"] == 1

    update_success_1 = __gda.update_attributes(condition=custom_condition, field='skip_count', new_value=0)
    update_success_2 = __gda.update_attributes(condition=custom_condition, field='in_start', new_value=1)
    if update_success_1 and update_success_2:
        __gda.save_changes(overwrite=True)


def update_skip_count_of_cable_start_with_point(start_point_code, start_point_skip_count):
    """
    更新起点为指定点的所有线缆的skip_count
    :param start_point_code: 根据nap_code查询
    :param start_point_skip_count: nap上的skip_count
    """
    def custom_condition(gdf):
        return gdf["point_in_code"] == start_point_code

    update_success = __gda.update_attributes(condition=custom_condition, field='skip_count',
                                             new_value=__gda.gdf['in_start'] + start_point_skip_count - 1)
    if update_success:
        __gda.save_changes(overwrite=True)

