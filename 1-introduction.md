# shapely（继承自GEOS/JTS的python计算几何库）

GIS背景，但不局限于GIS应用
https://shapely.readthedocs.io/en/stable/manual.html

## 空间数据对象

shapley实现的基本几何对象类型是点、曲线和曲面。一个对象的内部(Interior)、边界(Boundary)、外部(Exterior)点集是互斥的，三者的并集是整个2D平面。

+ 点

  - 内集：一个点
  - 边集：空集
  - 外集：不含该点的所有点集
  - 拓扑维数：0
  - class/collection class:
    - Point
      ![20230118141632](https://appen-pe.oss-cn-shanghai.aliyuncs.com/imgupload/20230118141632.png)
    - MultiPoint
      ![20230118141615](https://appen-pe.oss-cn-shanghai.aliyuncs.com/imgupload/20230118141615.png)
+ 曲线

  - 内集：曲线长度构成的点集，不包含端点
  - 边集：两个端点
  - 外集：不含该曲线的所有点集
  - 拓扑维数：1
  - class/collection class:
    - LineString
      ![20230118141701](https://appen-pe.oss-cn-shanghai.aliyuncs.com/imgupload/20230118141701.png)
    - LinearRing
      ![20230118141722](https://appen-pe.oss-cn-shanghai.aliyuncs.com/imgupload/20230118141722.png)
    - MultiLineString
      ![20230118141739](https://appen-pe.oss-cn-shanghai.aliyuncs.com/imgupload/20230118141739.png)
+ 曲面 Surface

  - 内集：曲面面积构成的点集，不包含边界
  - 边集：由一个及多个曲线的边界
  - 外集：不含该曲面的所有点集
  - 拓扑维数：2
  - class/collection class:
    - Polygon
      ![20230118141819](https://appen-pe.oss-cn-shanghai.aliyuncs.com/imgupload/20230118141819.png)
    - MultiPolygon
      ![20230118141833](https://appen-pe.oss-cn-shanghai.aliyuncs.com/imgupload/20230118141833.png)

## 拓扑关系

shapely能够描述几何对象之间的关系：DE-9IM列出的9种拓扑关系

[Dimensionally Extended Nine-Intersection Model (DE-9IM)](https://giswiki.hsr.ch/images/3/3d/9dem_springer.pdf)


|  拓扑谓词  |                                                描述                                                |
| :----------: | :--------------------------------------------------------------------------------------------------: |
|   Equals   |                                          几何对象完全相等                                          |
|  Disjoint  |                                       几何对象的点集没有共点                                       |
| Intersects |                            几何对象的点集至少有一个共点 (NOT Disjoint)                            |
|  Touches  |                             几何对象的边集至少有一个共点，内集没有共点                             |
|  Crosses  | 几何对象的内点至少有一个共点，但非全部内点都是共点，并且相交部分的拓扑维数*小于*其中一个几何对象。 |
|  Overlaps  | 几何对象的内点至少有一个共点，但非全部内点都是共点，并且相交部分的拓扑维数*等于*其中一个几何对象。 |
|   Within   |                          本几何对象的全部内点和边界点都是共点，被包含关系                          |
|  Contains  |                         另一个几何对象的全部内点和边界点都是共点，包含关系                         |

+ Equal
  A: Polygon
  B: Polygon
  A.Equals(B)
  ![20230118145717](https://appen-pe.oss-cn-shanghai.aliyuncs.com/imgupload/20230118145717.png)
+ Disjoint
  A: Line
  B: MultiPoint
  A.Disjoints(B)
  ![20230118154947](https://appen-pe.oss-cn-shanghai.aliyuncs.com/imgupload/20230118154947.png)
+ Intersect
  A: Line
  B: Line
  A.Intersects(B)
  ![20230118155028](https://appen-pe.oss-cn-shanghai.aliyuncs.com/imgupload/20230118155028.png)
+ Touch
  A: Polygon
  B: Polygon
  C: Polygon
  A.Touches(B) AND A.Touches(C)
  ![20230118155121](https://appen-pe.oss-cn-shanghai.aliyuncs.com/imgupload/20230118155121.png)
+ Cross
  A: Line
  B: Polygon
  A.Crosses(B)
  ![20230118155410](https://appen-pe.oss-cn-shanghai.aliyuncs.com/imgupload/20230118155410.png)
+ Overlap
  A: Line
  B: Line
  A.Overlaps(B)
  ![20230118155506](https://appen-pe.oss-cn-shanghai.aliyuncs.com/imgupload/20230118155506.png)
+ Within
  A: Line
  B: Polygon
  A.Within(B)
  ![20230118155544](https://appen-pe.oss-cn-shanghai.aliyuncs.com/imgupload/20230118155544.png)
+ Contain
  A: MultiPoint(方格点)
  B: MultiPoint(黑圆点)
  A.Contains(B)
  ![20230118155741](https://appen-pe.oss-cn-shanghai.aliyuncs.com/imgupload/20230118155741.png)

## API

几何对象的处理操作分为：
+ attributes 属性
  - geoms: 几何对象类型
  - is_simple: 线类型的简单性（LineString, LinearRing）
  - is_valid: 多边形的有效性（Polygon, MultiPolygon）
  - exterior: 多边形的外边LinearRing
  - interiors: 多边形的内边LinearRing, 可能有多个
+ measurement 测量
  - bounds: 计算Bounding Box（Point, MultiPoints, LineString, LinearRing, MultiLineString, Polygon, MultiPolygon）
  - length
  - area
+ coordinate operations 坐标转换
  - object.coords: 获取坐标
  - 
+ constructive operations 图形构建类操作
  - box: 矩形
  - polygon.orient: clone多边形
  - buffer
  - convex_hull
+ set-theoretic operations 集合类操作
  - intersection
  - union

几何对象的数值类型为float

在构造实例时可以使用第三个z坐标值但对计算没有影响，因为shapely忽略z坐标值，所有操作均在x-y平面内进行。所有操作都假定这些几何对象存在于同一个笛卡尔平面上。

构建几何对象时不会自动检查拓扑的简单性和有效性，需要用户自行调用：

```python
>>> LineString([(0, 0), (1, 1), (1, -1), (0, 1)]).is_simple
False

>>> MultiPolygon([Point(0, 0).buffer(2.0), Point(1, 1).buffer(2.0)]).is_valid
False
```

## To be continued
后续的笔记为可视化交互的Jupyter Notebook格式，用jupyter-lab浏览
$ pip install jupyterlab
$ cd .../shapely_tutorials
$ jupyter lab
