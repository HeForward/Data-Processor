# !/usr/bin/env python3
# coding=utf-8
#
# Personal code. All Rights Reserved
#
"""
工具类函数
Authors: He
"""
import os


def get_data_file(filename: str):
    """
    获取data目录下文件文件路径
    Args:
        filename: 文件名
    Returns:
    """
    data_dir = os.path.join(os.path.dirname(__file__), "data")  # data 目录
    data_file = os.path.join(data_dir, filename)
    return data_file
