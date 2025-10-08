from utils import gpkg_utils
from utils.gda_utils import LayerDGA


def _gda():
    gpkg_cable_path = gpkg_utils.get_gpkg_path("nap.gpkg")
    layer_name = "nap"
    nap_gda = LayerDGA(gpkg_cable_path, layer_name)
    return nap_gda

def get_all_points_on_cable(cable_code):
    nap_dga = _gda()
    return nap_dga.query_by_attribute(nap_dga.gdf["cable_code"] == cable_code)

if __name__ == '__main__':
    print(get_all_points_on_cable("SRO01-1"))