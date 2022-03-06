# !/usr/bin/env python3
# coding=utf-8
#
# Personal code. All Rights Reserved
#
"""
日常销量处理
Authors: He
"""
import pandas as pd
from utils import get_data_file


# 这是原始的需要处理的表格
src_file = get_data_file("daily_0902.xlsx")

data = pd.read_excel(src_file, sheet_name="原始数据")
kucun = pd.read_excel(src_file, sheet_name="库存表头", index_col=0)

data_group_by_SKU3 = data.groupby("SKU3")
sku_num = data_group_by_SKU3["SKU数量"].sum()

# 五日平均
wrpj_data = data[["SKU1", "五日平均"]]
wrpj_data.set_index("SKU1", inplace=True)

# 五日最大平台
zdpt_data = data[["SKU2", "五日最大平台", "平台"]]


for sku in kucun.index:  # 遍历库存表的每一行
    # 昨日销量
    if sku in sku_num.index:
        # print(sku, sku_num[sku])
        kucun.loc[sku, "昨日销量"] = sku_num[sku]
    else:
        kucun.loc[sku, "昨日销量"] = 0

    if sku in wrpj_data.index:
        kucun.loc[sku, "五日平均"] = wrpj_data.loc[sku]["五日平均"]
    else:
        kucun.loc[sku, "五日平均"] = 0

    zdpt_sku = zdpt_data[zdpt_data["SKU2"] == sku]
    if not zdpt_sku.empty:
        idx_max = zdpt_sku["五日最大平台"].idxmax()  # 取得五日最大平台数量最大的那一行，的索引
        pt_max = zdpt_sku.loc[idx_max]["平台"]  # 数量最大的对应的平台
        kucun.loc[sku, "五日最大平台"] = pt_max  # 记录这个平台到库存表的 "五日最大平台这一栏"
    print(kucun.loc[sku])

# 这是处理完后的表格需要存放的路径，只包含一张"达达直邮库存"
to_file = get_data_file("daily_0902_result.xlsx")

with pd.ExcelWriter(to_file, if_sheet_exists="new") as writer:
    kucun.to_excel(writer, index=True, sheet_name="库存统计")
