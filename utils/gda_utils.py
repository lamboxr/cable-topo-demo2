import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from typing import Optional, Dict, Callable, List


class LayerDGA:
    """按图层标识创建单例的GeoPackage图层操作类"""
    _instances: Dict[str, "LayerDGA"] = {}  # 存储{图层标识: 实例}的映射

    def __new__(cls, gpkg_path: str, layer_name: str):
        """
        按图层标识（gpkg_path + layer_name）创建单例
        :param gpkg_path: GeoPackage文件路径
        :param layer_name: 图层名称
        """
        # 生成唯一标识（区分不同图层）
        instance_key = f"{gpkg_path}::{layer_name}"
        if instance_key not in cls._instances:
            # 新标识：创建实例并缓存
            cls._instances[instance_key] = super().__new__(cls)
            # 初始化实例属性
            cls._instances[instance_key].gpkg_path = gpkg_path
            cls._instances[instance_key].layer_name = layer_name
            cls._instances[instance_key]._gdf: Optional[gpd.GeoDataFrame] = None  # 缓存当前图层的GeoDataFrame
            # 加载图层数据
            cls._instances[instance_key]._load_layer()
        return cls._instances[instance_key]

    def _load_layer(self):
        """加载当前图层数据到缓存"""
        try:
            self._gdf = gpd.read_file(self.gpkg_path, layer=self.layer_name)
            print(f"图层加载成功：{self.layer_name}@{self.gpkg_path}，要素数：{len(self._gdf)}")
        except Exception as e:
            print(f"图层加载失败：{self.layer_name}@{self.gpkg_path}，错误：{str(e)}")
            self._gdf = None

    @property
    def gdf(self) -> Optional[gpd.GeoDataFrame]:
        """获取当前图层的GeoDataFrame（自动重新加载如果未加载）"""
        if self._gdf is None:
            self._load_layer()
        return self._gdf

    def query_by_attribute(self, condition) -> Optional[gpd.GeoDataFrame]:
        """属性查询（返回符合条件的子集）"""
        if self.gdf is None:
            return None
        return self.gdf[condition].copy()

    def query_by_spatial(self, spatial_func) -> Optional[gpd.GeoDataFrame]:
        """空间查询（返回符合空间条件的子集）"""
        if self.gdf is None:
            return None
        return self.gdf[spatial_func(self.gdf)].copy()

    def save(self, overwrite: bool = True):
        """保存当前图层（覆盖原图层）"""
        if self.gdf is None:
            print("无数据可保存")
            return
        # 保存图层（覆盖模式）
        self.gdf.to_file(
            self.gpkg_path,
            layer=self.layer_name,
            driver="GPKG",
            mode="a",
            append=not overwrite  # overwrite=True时append=False（覆盖）
        )
        print(f"图层已保存：{self.layer_name}@{self.gpkg_path}")

    def refresh(self):
        """重新加载图层数据（刷新缓存）"""
        self._load_layer()

    # --------------------------
    # 新增：数据更新方法
    # --------------------------
    def update_attributes(self, condition: Callable, field: str, new_value) -> bool:
        """
        按条件更新指定字段的值
        :param condition: 筛选条件（如：lambda gdf: gdf["level"] == 1）
        :param field: 要更新的字段名
        :param new_value: 新值（可是固定值或与字段长度匹配的列表/数组）
        :return: 更新成功返回True，失败返回False
        """
        if self.gdf is None or field not in self.gdf.columns:
            print(f"图层为空或字段不存在：{field}")
            return False

        # 筛选符合条件的行并更新字段值
        mask = condition(self.gdf)
        if not mask.any():
            print("无符合条件的要素可更新")
            return True

        self._gdf.loc[mask, field] = new_value
        print(f"已更新 {mask.sum()} 个要素的 {field} 字段")
        return True

    def add_features(self, new_features: gpd.GeoDataFrame) -> bool:
        """
        向图层添加新要素
        :param new_features: 包含新要素的GeoDataFrame（需与原图层字段和CRS一致）
        :return: 添加成功返回True
        """
        if self.gdf is None:
            print("图层未加载，无法添加要素")
            return False

        # 检查字段一致性（新要素必须包含原图层的所有必填字段）
        missing_fields = set(self.gdf.columns) - set(new_features.columns)
        if missing_fields:
            print(f"新要素缺少必要字段：{missing_fields}")
            return False

        # 检查坐标系一致性
        if self.gdf.crs != new_features.crs:
            print(f"坐标系不一致，自动转换为图层坐标系：{self.gdf.crs}")
            new_features = new_features.to_crs(self.gdf.crs)

        # 拼接新要素到原图层
        self._gdf = pd.concat([self._gdf, new_features], ignore_index=True)
        print(f"已添加 {len(new_features)} 个新要素，当前总要素数：{len(self._gdf)}")
        return True

    def delete_features(self, condition: Callable) -> bool:
        """
        按条件删除要素
        :param condition: 筛选条件（如：lambda gdf: gdf["status"] == "废弃"）
        :return: 删除成功返回True
        """
        if self.gdf is None:
            print("图层未加载，无法删除要素")
            return False

        # 筛选符合条件的行
        mask = condition(self.gdf)
        if not mask.any():
            print("无符合条件的要素可删除")
            return True

        # 删除要素（保留不满足条件的要素）
        self._gdf = self._gdf[~mask].copy()
        print(f"已删除 {mask.sum()} 个要素，当前总要素数：{len(self._gdf)}")
        return True

    def save_changes(self, overwrite: bool = True) -> bool:
        """
        将内存中的修改同步到GeoPackage文件
        :param overwrite: 是否覆盖原图层
        :return: 保存成功返回True
        """
        if self.gdf is None:
            print("无数据可保存")
            return False

        try:
            # 保存图层（覆盖模式）
            self._gdf.to_file(
                self.gpkg_path,
                layer=self.layer_name,
                driver="GPKG",
                mode="a",
                append=not overwrite
            )
            print(f"修改已同步到文件：{self.gpkg_path}（图层：{self.layer_name}）")
            return True
        except Exception as e:
            print(f"保存失败：{e}")
            return False
# 使用示例
if __name__ == "__main__":
    # 1. 创建cable图层的单例实例
    gpkg_cable_path = "./gpkg/cable.gpkg"
    cable_dga1 = LayerDGA(gpkg_cable_path, "cable")
    cable_dga2 = LayerDGA(gpkg_cable_path, "cable")  # 同一图层，应返回同一实例
    print(f"cable实例是否相同：{cable_dga1 is cable_dga2}")  # 输出：True

    gpkg_nap_path = "./gpkg/nap.gpkg"
    # 2. 创建nap图层的单例实例
    nap_dga1 = LayerDGA(gpkg_nap_path, "nap")
    nap_dga2 = LayerDGA(gpkg_nap_path, "nap")  # 同一图层，应返回同一实例
    print(f"nap实例是否相同：{nap_dga1 is nap_dga2}")  # 输出：True

    # 3. 验证cable和nap是不同实例
    print(f"cable和nap实例是否不同：{cable_dga1 is nap_dga1}")  # 输出：False

    # 4. 使用cable实例查询
    if cable_dga1.gdf is not None:
        # 查询电压>10kV的电缆
        level1 = cable_dga1.query_by_attribute(
            condition=cable_dga1.gdf["level"] == 1
        )
        print(f"cable图层中level==1的要素数：{len(level1)}")

    # 5. 使用nap实例查询
    if nap_dga1.gdf is not None:
        # 查询code包含"NAP"的点
        nap_filtered = nap_dga1.query_by_attribute(
            condition=nap_dga1.gdf["in_start"] == 1
        )
        print(f"nap图层中in_start==1的要素数：{len(nap_filtered)}")