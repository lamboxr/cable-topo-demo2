import geopandas as gpd

# 1. 读取两个GeoPackage中的图层
gpkg_cable = "cable.gpkg"
gpkg_nap = "nap.gpkg"

# 读取线图层（cable）和点图层（nap）
gdf_cable = gpd.read_file(gpkg_cable, layer="cable")
gdf_nap = gpd.read_file(gpkg_nap, layer="nap")

# 2. 查看图层字段（确认关联字段存在）
print("cable图层字段：", gdf_cable.columns.tolist())  # 需包含 "code" 字段
print("nap图层字段：", gdf_nap.columns.tolist())      # 需包含 "cable_code" 字段

# 3. 基于 "cable.code = nap.cable_code" 进行连接
# left_on：左图层（cable）的关联字段
# right_on：右图层（nap）的关联字段
gdf_joined = gdf_cable.merge(
    gdf_nap,
    left_on="code",       # cable图层的关联字段
    right_on="cable_code",  # nap图层的关联字段
    how="inner"           # 连接方式（内连接，仅保留匹配的记录）
)

# 4. 查看连接结果
print(f"连接后要素数量：{len(gdf_joined)}")
# 显示关键关联字段，确认连接是否正确
print(gdf_joined[["code", "cable_code"]].head())