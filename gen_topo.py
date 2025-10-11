import openpyxl
from openpyxl.styles import Border, Side, Font, Alignment
from data_service import data_service_nap, data_service_cable

# 全局配置
COLUMN_WIDTHS = {
    'A': 12,
    'B': 48,
    'C': 32,
    'D': 48,
    'E': 32,
    'F': 48,
    'G': 32
}
LEVEL_TO_COLUMN = {
    1: 'B',
    2: 'D',
    3: 'F'
}
GROUP_ROWS = 8  # 每组占用8行


def init_workbook():
    """初始化Excel工作簿，设置列宽和样式基础"""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "逻辑拓扑图"

    # 设置列宽
    for col, width in COLUMN_WIDTHS.items():
        ws.column_dimensions[col].width = width

    return wb, ws


def generate_topo_excel(output_path):
    """生成拓扑Excel的主函数"""
    wb, ws = init_workbook()
    current_row = 1  # 起始行

    # 1. 获取所有SRO节点（根节点），按code升序
    sro_points = data_service_nap.get_all_sro_points_by_order_code_asc()
    if sro_points is None or sro_points.empty:
        print("无SRO节点数据，无法生成拓扑图")
        return

    # 2. 遍历SRO节点，递归绘制拓扑
    for _, sro in sro_points.iterrows():
        # 绘制SRO节点（A列）
        current_row = draw_sro_node(ws, current_row, sro)
        # 查询SRO节点关联的线缆（Level1），按code升序
        cables = data_service_cable.get_all_cables_start_with_one_point_order_by_code_asc(sro['code'])
        if cables is not None and not cables.empty:
            for _, cable in cables.iterrows():
                # 绘制线缆（B列，Level1）并递归处理下一级节点
                current_row = draw_cable_and_recurse(ws, current_row, cable, level=1)

    # 保存文件
    wb.save(output_path)
    print(f"拓扑图已生成：{output_path}")


def draw_sro_node(ws, start_row, sro_data):
    """绘制A列的SRO节点（8行一组）"""
    # 1-4行合并，粗外侧线框
    merge_cells(
        ws,
        start_row=start_row,
        end_row=start_row + 3,  # 第1-4行（索引0-3）
        col='A',
        value=None,
        border=THICK_BORDER
    )
    # 第1行：nap.class（加粗居中）
    set_cell(
        ws,
        row=start_row,
        col='A',
        value=sro_data['class'],
        font=BOLD_FONT,
        align=CENTER_ALIGN
    )
    # 第2行：nap.code（居中）
    set_cell(
        ws,
        row=start_row + 1,
        col='A',
        value=sro_data['code'],
        align=CENTER_ALIGN
    )
    # 5-8行留空（不合并，保持默认样式）
    return start_row + GROUP_ROWS


def draw_closure_pbo_node(ws, start_row, nap_data, col):
    """绘制C/E/G列的Closure/PBO节点（8行一组）"""
    # 1-4行合并，粗外侧线框
    merge_cells(
        ws,
        start_row=start_row,
        end_row=start_row + 3,
        col=col,
        value=None,
        border=THICK_BORDER
    )
    # 第1行：nap.class（加粗居中）
    set_cell(
        ws,
        row=start_row,
        col=col,
        value=nap_data['class'],
        font=BOLD_FONT,
        align=CENTER_ALIGN
    )
    # 第2行：nap.code + "    " + nap.type（居中）
    set_cell(
        ws,
        row=start_row + 1,
        col=col,
        value=f"{nap_data['code']}    {nap_data['type']}",
        align=CENTER_ALIGN
    )
    # 第4行：nap.in_start + "-" + nap.in_end（居中）
    set_cell(
        ws,
        row=start_row + 3,
        col=col,
        value=f"{nap_data['in_start']}-{nap_data['in_end']}",
        align=CENTER_ALIGN
    )
    return start_row + GROUP_ROWS


def draw_cable_and_recurse(ws, start_row, cable_data, level):
    """绘制线缆并递归处理下一级节点"""
    # 占位：后续实现
    return start_row + GROUP_ROWS


# 样式定义
THICK_BORDER = Border(
    left=Side(style='thick'),
    right=Side(style='thick'),
    top=Side(style='thick'),
    bottom=Side(style='thick')
)
BOTTOM_THICK_BORDER = Border(
    bottom=Side(style='thick')
)
BOLD_FONT = Font(bold=True)
CENTER_ALIGN = Alignment(horizontal='center', vertical='center', wrap_text=True)


def merge_cells(ws, start_row, end_row, col, value, border=None, font=None, align=None):
    """
    合并单元格并设置内容和样式
    :param ws: 工作表
    :param start_row: 起始行
    :param end_row: 结束行
    :param col: 列标识（如'A'）
    :param value: 单元格内容
    :param border: 边框样式
    :param font: 字体样式
    :param align: 对齐方式
    """
    cell_range = f"{col}{start_row}:{col}{end_row}"
    ws.merge_cells(cell_range)
    cell = ws[f"{col}{start_row}"]
    cell.value = value
    cell.border = border or Border()
    cell.font = font or Font()
    cell.alignment = align or Alignment()


def set_cell(ws, row, col, value, border=None, font=None, align=None):
    """设置单个单元格内容和样式"""
    cell = ws[f"{col}{row}"]
    cell.value = value
    cell.border = border or Border()
    cell.font = font or Font()
    cell.alignment = align or Alignment()



if __name__ == '__main__':
    generate_topo_excel("拓扑图输出.xlsx")