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
    return __gda.query_by_attribute(__gda.gdf["level"]==1)

def get_all_distribution_start_with_SRO(sro_code):
    def custom_condition(gdf):
        return (gdf["point_in_code"] == sro_code) & (gdf["level"] == 1)

    return __gda.get_features_by_condition(custom_condition)

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

