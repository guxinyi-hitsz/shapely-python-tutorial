# -*- coding: UTF-8 -*- 

"""
Author  : Xinyi Gu
Date    : 2023/2/16 10:03 
Project :
Description: 凸锥

Change History: 
    @change
"""
from numpy import angle

__all__ = ["ConvexCone"]


class ConvexCone(object):
    def __init__(self, p0, pts):
        """
        以p0为原点,包含pts所有点的凸锥convex cone
        @param: p0 原点 [x,y]
        @param: pts 点列表 [(x,y),...]
        """
        self.vec_min = None
        self.vec_max = None
        self.origin = p0
        self.sort(pts)

    def sort(self, pts) -> list:
        """
        以p0为原点,更新pts所有点的凸锥convex cone
        @param: pts 点列表 [(x,y),...]
        """
        # 向量和辐角
        vectors = []
        for p in pts:
            vectors.append(complex(p[0] - self.origin[0], p[1] - self.origin[1]))

        # 计算锥边
        self.vec_min = vectors[0]
        self.vec_max = vectors[0]
        index_sort = []
        for i, vec in enumerate(vectors):
            a = angle(self.vec_min.conjugate() * vec, deg=True)
            if a < 0:
                self.vec_min = vec
                index_sort.insert(0, i)
                continue

            a = angle(self.vec_max.conjugate() * vec, deg=True)
            if a > 0:
                self.vec_max = vec
                index_sort.append(i)
                continue

            index_sort.insert(-1, i)

        # 返回排序后的points index list
        return index_sort

    def contains(self, point) -> bool:
        """
        判断点是否在凸锥内
        @params: point 任意点 [x,y]
        @return: flag True/False
        """
        vec = complex(point[0] - self.origin[0], point[1] - self.origin[1])

        flag = True
        a = angle(self.vec_min.conjugate() * vec, deg=True)
        if a < 0:
            flag = False

        a = angle(self.vec_max.conjugate() * vec, deg=True)
        if a > 0:
            flag = False
        return flag
