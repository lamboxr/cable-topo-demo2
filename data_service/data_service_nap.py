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


def get_all_SRO_points():
    return __gda.get_features_by_attribute('class', '==', 'SRO')


def get_all_points_on_cable(cable_code):
    return __gda.get_features_by_attribute('cable_code', '==', cable_code)


def get_all_passes_on_d1(d1_code):
    return __gda.get_features_by_attribute('cable_code', '==', d1_code)


def init_skip_count_as_zero_of_all_SRO_points():
    def custom_condition(gdf):
        return gdf["class"] == 'SRO'

    update_success = __gda.update_attributes(condition=custom_condition, field='skip_count', new_value=0)
    if update_success:
        __gda.save_changes(overwrite=True)


def update_skip_count_of_points_on_cable(cable_code, cable_skip_count):
    print(f"d1 code {cable_code} skip count {cable_skip_count}")

    def custom_condition(gdf):
        return gdf["cable_code"] == cable_code

    __gda.update_attributes(condition=custom_condition, field="skip_count",
                            new_value=__gda.gdf['in_start'] + cable_skip_count - 1)
    __gda.save_changes(overwrite=True)


if __name__ == '__main__':
    print(get_all_points_on_cable("SRO01-1"))
