from utils import gpkg_utils
from utils.gda_utils import LayerDGA


def _gda():
    gpkg_cable_path = gpkg_utils.get_gpkg_path("cable.gpkg")
    layer_name = "cable"
    cable_dga = LayerDGA(gpkg_cable_path, layer_name)
    return cable_dga


__gda = _gda()


def get_all_SRO():
    cable_dga = _gda()


def get_all_distribution_1():
    return __gda.query_by_attribute(__gda.gdf["level"] == 1)


def get_all_distribution_1_start_with_SRO(sro_code):
    def custom_condition(gdf):
        return (gdf["point_in_code"] == sro_code) & (gdf["level"] == 1)

    return __gda.get_features_by_condition(custom_condition)


def get_all_cable_start_with_one_point(nap_code):
    def custom_condition(gdf):
        return gdf["point_in_code"] == nap_code

    return __gda.get_features_by_condition(custom_condition)


def init_data_of_distribution_1():
    def custom_condition(gdf):
        return gdf["level"] == 1

    update_success_1 = __gda.update_attributes(condition=custom_condition, field='skip_count', new_value=0)
    update_success_2 = __gda.update_attributes(condition=custom_condition, field='in_start', new_value=1)
    if update_success_1 and update_success_2:
        __gda.save_changes(overwrite=True)


def update_skip_count_of_cable_start_with_point(start_point_code, start_point_skip_count):
    def custom_condition(gdf):
        return gdf["point_in_code"] == start_point_code

    update_success = __gda.update_attributes(condition=custom_condition, field='skip_count',
                                             new_value=__gda.gdf['in_start'] + start_point_skip_count - 1)
    if update_success:
        __gda.save_changes(overwrite=True)


# def update(condition,filed,new_value):
#     update_success = __gda.update_attributes(
#         condition=lambda gdf: gdf["code"] == "SRO01-1",
#         field="in_start",
#         new_value=None
#     )
#     print(update_success)
#     __gda.save_changes(overwrite=True)


if __name__ == '__main__':
    print(get_all_distribution_1())
