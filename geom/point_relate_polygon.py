# -*- coding: UTF-8 -*- 

"""
Author  : Xinyi Gu
Date    : 2023/2/15 12:08 
Project :
Description:
__all__ 注册了外部可调用的方法名

Change History: 
    @change
"""
from shapely.geometry import Polygon, Point, MultiPoint

__all__ = ["points_outside_polygon"]


def points_outside_polygon(points, polygon_points) -> list:
    """
    判断点集是否在多边形外
    @param points: 点集 [[x1,y1],...]
    @param polygon_points: 多边形顶点 [(x,y),...]
    @return: out_ids: 在多边形外部的点的index list
    @return: in_ids: 不超出多边形的点的index list
    """
    out_ids = []
    in_ids = []
    region = Polygon(polygon_points)

    if region.covers(MultiPoint(points)):
        in_ids = list(range(len(points)))
        return out_ids, in_ids

    for i, point in enumerate(points):
        if not region.covers(Point(point)):
            out_ids.append(i)
        else:
            in_ids.append(i)

    return out_ids, in_ids
