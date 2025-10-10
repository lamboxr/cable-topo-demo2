import pandas as pd

from data_service import data_service_cable
from utils import gpkg_utils
from utils.gda_utils import LayerDGA


def _gda():
    gpkg_cable_path = gpkg_utils.get_gpkg_path("nap.gpkg")
    layer_name = "nap"
    nap_gda = LayerDGA(gpkg_cable_path, layer_name)
    return nap_gda


__gda = _gda()


def get_all_extremities():
    """
    获取所有终点类型的节点
    :return: 终点类型的节点列表
    """
    return __gda.get_features_by_attribute('pass_seq', '==', 0)


def get_all_sro_points():
    """
    获取所有SRO节点
    :return: 所有SRO节点列表
    """
    return __gda.get_features_by_attribute('class', '==', 'SRO')


def get_all_points_on_cable(cable_code: str):
    """
    获取指定线缆上所有掏芯节点（closure,终点）
    :param cable_code: 根据线缆code查询
    :return: 所有掏芯节点列表
    """
    return __gda.get_features_by_attribute('cable_in', '==', cable_code)


def init_data_of_all_sro_points():
    """
    初始化所有sro节点的skip_count值为0
    """

    def custom_condition(gdf):
        return gdf["class"] == 'SRO'

    update_success = __gda.update_attributes(condition=custom_condition, field='skip_count', new_value=0)
    if update_success:
        __gda.save_changes(overwrite=True)


def update_skip_count_of_points_on_cable(cable_code: str, cable_skip_count: int):
    """
    更新指定线缆上所有掏芯节点的skip_count
    :param cable_code: 根据线缆code查询
    :param cable_skip_count: 线缆skip_count
    """
    print(f"cable_code: {cable_code}, skip count: {cable_skip_count}")

    def custom_condition(gdf):
        return gdf["cable_in"] == cable_code

    __gda.update_attributes(condition=custom_condition, field="skip_count",
                            new_value=__gda.gdf['in_start'] + cable_skip_count - 1)
    __gda.save_changes(overwrite=True)
