from utils import gpkg_utils
from utils.gda_utils import LayerDGA

gpkg_cable_path = r"E:\Users\lambo\Desktop\mlg\cable.gpkg"

def _gda():
    # gpkg_cable_path = gpkg_utils.get_gpkg_path("cable.gpkg")

    layer_name = "cable"
    cable_dga = LayerDGA(gpkg_cable_path, layer_name)
    return cable_dga


def get_all_distribution_1():
    cable_dga = _gda()
    return cable_dga.query_by_attribute(cable_dga.gdf["level"]==1)

def update(condition,filed,new_value):
    cable_dga = _gda()
    update_success = cable_dga.update_attributes(
        condition=lambda gdf: gdf["code"] == "SRO01-1",
        field="in_start",
        new_value=1
    )
    print(update_success)
    cable_dga.save_changes()


if __name__ == '__main__':
    print(get_all_distribution_1())
    update(1,1,1)
