# -*- coding: UTF-8 -*- 

"""
Author  : Xinyi Gu
Date    : 2023/2/15 12:10 
Project :
Description:
__all__ 注册了外部可调用的方法名

Change History: 
    @change
"""
from shapely.geometry import Polygon, LineString, MultiPoint
from shapely.geometry.polygon import orient
from wooey_utils.projects.geom.cone import ConvexCone
from wooey_utils.projects.geom.point_relate_polygon import points_outside_polygon

__all__ = ["line_in_polygon", "line_in_polygon_v1", "line_in_polygon_v2"]


def line_in_polygon(line_points, polygon_points) -> bool:
    """
    判断折线段是否完全在多边形内、边界上
    调用shapely方法
    @param line_points: [(x,y),...]
    @param polygon_points: [(x,y),...]

    @return bool
    """
    l = LineString(line_points)
    p = Polygon(polygon_points)

    if p.covers(l):
        return True
    else:
        return False


def line_in_polygon_v1(line_points, polygon_points):
    """
    判断折线段是否完全在多边形内、边界上，并提示是具体的哪一条线段超出多边形
    version 1: 调用shapely方法
    @param line_points: [(x,y),...]
    @param polygon_points: [(x,y),...]

    @return bool
    @return out_segments: list 超出多边形区域的线段，在原line_points中的index list
    """
    out_segments = []

    poly = Polygon(polygon_points)
    for k, p1 in enumerate(line_points[0:-1]):
        p2 = line_points[k + 1]
        segment = LineString([p1, p2])
        if not poly.covers(segment):
            out_segments.append([k, k + 1])

    return len(out_segments) == 0, out_segments


def line_in_polygon_v2(line_points, polygon_points):
    """
    判断折线段是否完全在多边形内、边界上，并提示是具体的哪一条线段超出多边形
    version 2: 将多边形以外的区域视为不可见区域, 计算线段的每两个端点相互之间的可见性
    @param line_points: [(x,y),...]
    @param polygon_points: [(x,y),...]

    @return bool 外False
    @return out_points: list 超出多边形区域的点，在原line_points中的index list
    @return out_segments: list 超出多边形区域的线段，在原line_points中的index list
    """
    """逆时针点序构造多边形"""
    flag = True
    out_points = []
    out_segments = []

    p = orient(Polygon(polygon_points), sign=1.0)
    """判断折线段的顶点是否全部在多边形内"""
    out_ids, in_ids = points_outside_polygon(points=line_points, polygon_points=polygon_points)
    if len(out_ids) > 0:
        flag = False
        out_points = out_ids
        line_points = line_points[in_ids]
    """判断多边形的凹凸性"""
    hull = orient(p.convex_hull, sign=1.0)
    hull_pts = list(hull.exterior.coords)
    polygon_pts = list(p.exterior.coords)
    compare_pts = [False] * len(polygon_pts)
    j = 0
    for i, pp in enumerate(polygon_pts):
        if pp == hull_pts[j]:
            compare_pts[i] = True
            j += 1
    if not any(compare_pts):
        """如果凸多边形且顶点都在内部，折线一定在内部"""
        return flag, out_points, out_segments
    """凹多边形与凸包求差计算不可见区域"""
    diff = hull.difference(p)
    invisible_regions = []
    if diff.geom_type == 'Polygon':
        invisible_regions = [diff]
    elif diff.geom_type == 'MultiPolygon':
        invisible_regions = list(diff.geoms)
    """计算线段的每两个端点相互之间的可见性， 任意一段不可见就返回False"""
    for region in invisible_regions:
        region_points = list(region.exterior.coords)
        for k, p1 in enumerate(line_points[0:-1]):
            p2 = line_points[k + 1]
            """以p1为原点,不可见区域的顶点构成的凸锥"""
            cone = ConvexCone(p1, region_points[:-1])
            """p2点在凸锥内，不可见。p2点在凸锥外，可见。"""
            if cone.contains(p2):
                """线段(p1,p2)不在多边形内"""
                out_segments.append([k, k + 1])
                flag = False
    return flag, out_points, out_segments
