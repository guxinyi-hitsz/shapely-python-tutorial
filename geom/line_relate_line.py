# -*- coding: UTF-8 -*- 

"""
Author  : Xinyi Gu
Date    : 2023/2/15 12:11 
Project :
Description:
__all__ 注册了外部可调用的方法名

Change History: 
    @change
"""
from shapely.geometry import LineString

__all__ = ["line_intersection"]


def line_intersection(points_A, points_B):
    """
    判断两个线段是否相交
    @param points_A 画的线段 [(x,y),(x,y)]
    @param points_B 多边形的线段 [(x,y),(x,y)]

    @return flag 线段有交点（不包括端点）或者线段有共线重合返回True，否则返回False
    @return is_line_string 有交点False，共线True
    """
    line1 = LineString([points_A[0], points_A[1]])
    line2 = LineString([points_B[0], points_B[1]])

    if line1.crosses(line2):
        # 线段有交点（不包括端点）
        flag = True
        is_line_string = False
    elif line1.overlaps(line2):
        # 线段有共线重合
        flag = True
        is_line_string = True
    else:
        flag = False
        is_line_string = False

    return flag, is_line_string
