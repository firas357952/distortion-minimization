import random
from collections.abc import Iterable

import numpy as np
from shapely.geometry import LineString
from shapely.geometry import Point as ShapelyPoint
from shapely.geometry import Polygon as ShapelyPolygon
from skspatial.objects import Line as ln

"""
The shapely.geometry.Point from the Shapely library doesn't directly support adding custom methods
through subclassing due to its design as a C-based geometric library.
(source https://github.com/shapely/shapely/issues/1233)
So we create a wrapper around the ShapelyPoint class.
Same for other classes.
"""


# Converts inputs to ShapelyPoint and potentially converts ShapelyPoint outputs to Point
class PointWrapper:
    @staticmethod
    def convert(arg):
        if isinstance(arg, Iterable):
            return type(arg)(
                (
                    (
                        PointWrapper.convert(ar)
                        if isinstance(ar, Iterable)
                        else (ar._point if isinstance(ar, Point) else ar)
                    )
                    for ar in arg
                )
            )
        return arg._point if isinstance(arg, Point) else arg

    @staticmethod
    def input_wrapper(func):
        def wrapper(*args, **kwargs):
            return func(*PointWrapper.convert(args), **kwargs)

        return wrapper

    @staticmethod
    def result_wrapper(result):
        return Point(result) if isinstance(result, ShapelyPoint) else result

    @staticmethod
    def output_wrapper(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return PointWrapper.result_wrapper(result)

        return wrapper


class PolygonWrapper:
    @staticmethod
    def input_wrapper(func):
        def wrapper(*args, **kwargs):
            return func(
                *(arg._polygon if isinstance(arg, Polygon) else arg for arg in args),
                **kwargs,
            )

        return wrapper

    @staticmethod
    def result_wrapper(result):
        return Polygon(result) if isinstance(result, ShapelyPolygon) else result

    @staticmethod
    def output_wrapper(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return PolygonWrapper.result_wrapper(result)

        return wrapper


pw = PointWrapper
plw = PolygonWrapper


class Point:
    def __init__(self, *args):
        if len(args) == 2:
            self._point = ShapelyPoint(*args)
        elif len(args) == 1 and isinstance(args[0], ShapelyPoint):
            self._point = args[0]
        else:
            raise ValueError("Could not initialize Point object")
        self._attribute_cache = {}  # Cache to store accessed attributes

    def __getattr__(self, attr):
        if attr not in self._attribute_cache:
            if hasattr(self._point, attr):
                attr_value = getattr(self._point, attr)
                if callable(attr_value):
                    self._attribute_cache[attr] = pw.output_wrapper(
                        pw.input_wrapper(attr_value)
                    )
                else:
                    self._attribute_cache[attr] = pw.result_wrapper(attr_value)
            else:
                raise AttributeError(f"'Point' object has no attribute '{attr}'")
        return self._attribute_cache[attr]

    def __str__(self):
        return str(self._point)

    @pw.input_wrapper
    def __eq__(self, other):
        return self.equals(other)

    @pw.input_wrapper
    def __ne__(self, other):
        return not self.__eq__(other)

    @pw.output_wrapper
    def closest_point(self, point_list: list) -> "Point":
        return min(point_list, key=lambda p: self.distance(p))

    @staticmethod
    def coords_to_points(list_coords: list[tuple]) -> list["Point"]:
        points = []
        for x, y in list_coords:
            points.append(Point(x, y))
        return points

    @staticmethod
    def points_to_coords(list_coords: list["Point"]) -> list[tuple]:
        coords = []
        for point in list_coords:
            coords.append((point.x, point.y))
        return coords


class Line:
    def __init__(self, start, end):
        if start == end:
            raise ValueError("To define a Line, points must be different")
        self._line: LineString = pw.input_wrapper(LineString)([start, end])
        self._attribute_cache = {}  # Cache to store accessed attributes

    def __getattr__(self, attr):
        if attr not in self._attribute_cache:
            if hasattr(self._line, attr):
                attr_value = getattr(self._line, attr)
                if callable(attr_value):
                    self._attribute_cache[attr] = pw.output_wrapper(
                        pw.input_wrapper(attr_value)
                    )
                else:
                    self._attribute_cache[attr] = pw.result_wrapper(attr_value)
            else:
                raise AttributeError(f"'Line' object has no attribute '{attr}'")
        return self._attribute_cache[attr]

    def __str__(self):
        return str(self._line)

    @pw.input_wrapper
    def get_projection_coordinate(self, point) -> "Point":
        p1, p2 = self._line.coords
        x, y = ln(
            point=[p1[0], p1[1]], direction=[p2[0] - p1[0], p2[1] - p1[1]]
        ).project_point([point.x, point.y])
        return Point(x, y)

    @pw.input_wrapper
    def perpendicular_line(self, point) -> "Line":
        p1, p2 = self._line.coords
        normal_vector = Vector(Point(*p1), Point(*p2)).normal_vector()
        return Line(point, Point(point.x + normal_vector.x, point.y + normal_vector.y))


class Vector(np.ndarray):
    def __new__(cls, *args):
        if len(args) == 2 and all(isinstance(arg, Point) for arg in args):
            start, end = args
            x_comp, y_comp = end.x - start.x, end.y - start.y
        elif len(args) == 2 and all(isinstance(arg, (int, float)) for arg in args):
            x_comp, y_comp = args
        else:
            raise ValueError("Invalid arguments provided to create Vector object")

        # Create a numpy array with the components and cast it to the Vector class
        obj = np.array([x_comp, y_comp]).view(cls)
        obj.x, obj.y = x_comp, y_comp
        return obj

    @property
    def norm(self) -> float:
        return np.linalg.norm(self)

    @staticmethod
    def dot_product(vector_1: "Vector", vector_2: "Vector") -> float:
        return np.dot(vector_1, vector_2)

    def normal_vector(self) -> "Vector":
        return Vector(self.y, -self.x)


class Shape:
    def __init__(self, arg):
        self._create_shape(arg)
        self._attribute_cache = {}  # Cache to store accessed attributes

    def _create_shape(self, arg):
        if isinstance(arg, ShapelyPolygon):
            self._polygon = arg
        else:
            self._polygon = self._generate_shape(arg)
        self.vertices = self._extract_vertices(self._polygon)

    def _generate_shape(self, arg):
        if all(isinstance(point, Point) for point in arg):
            return ShapelyPolygon((v._point for v in arg))
        return ShapelyPolygon(arg)

    def _extract_vertices(self, polygon):
        exterior_coords = polygon.exterior.coords[:-1]
        return self._process_vertices(exterior_coords)

    def _process_vertices(self, exterior_coords):
        raise NotImplementedError("Subclasses must implement _process_vertices method")

    def __getattr__(self, attr):
        if attr not in self._attribute_cache:
            if hasattr(self._polygon, attr):
                attr_value = getattr(self._polygon, attr)
                if callable(attr_value):
                    self._attribute_cache[attr] = plw.output_wrapper(
                        plw.input_wrapper(attr_value)
                    )
                else:
                    self._attribute_cache[attr] = plw.result_wrapper(
                        pw.result_wrapper(attr_value)
                    )
            else:
                raise AttributeError(
                    f"'{self.__class__.__name__}' object has no attribute '{attr}'"
                )
        return self._attribute_cache[attr]

    def __str__(self):
        return str(self._polygon)


class Polygon(Shape):
    expected_vertex_count = 3  # A polygon should have at least 3 vertices

    def _process_vertices(self, exterior_coords):
        distinct_vertices = set(exterior_coords)
        if len(distinct_vertices) < self.expected_vertex_count:
            raise ValueError(
                f"A {self.__class__.__name__.lower()} must have at least {self.expected_vertex_count} distinct points."
            )
        if len(distinct_vertices) < len(exterior_coords):
            raise ValueError(
                f"A {self.__class__.__name__.lower()} must have distinct points."
            )
        return Point.coords_to_points(exterior_coords)

    def divide_convex_polygon_to_triangles(self) -> list["Triangle"]:
        triangles = []
        for i in range(1, len(self.vertices) - 1):
            triangles.append(
                Triangle([self.vertices[0], self.vertices[i], self.vertices[i + 1]])
            )
        return triangles

    def random_point_in_shape(self) -> "Point":
        triangles = self.divide_convex_polygon_to_triangles()
        areas = [triangle.area for triangle in triangles]
        total_area = sum(areas)
        probabilities = [area / total_area for area in areas]
        idx = random.choices(range(len(triangles)), weights=probabilities, k=1)[0]
        return Triangle.random_point_in_shape(triangles[idx])

    def average_square_distance(self, point: "Point"):
        return sum(
            triangle.average_square_distance(point)
            for triangle in self.divide_convex_polygon_to_triangles()
        )


class Triangle(Shape):
    expected_vertex_count = 3  # A triangle should have exactly 3 vertices

    def _process_vertices(self, exterior_coords):
        if len(set(exterior_coords)) != self.expected_vertex_count:
            raise ValueError(
                f"A {self.__class__.__name__.lower()} must have {self.expected_vertex_count} distinct points."
            )
        return Point.coords_to_points(exterior_coords)

    def random_point_in_shape(self) -> "Point":
        a, b, c = self.vertices

        r1 = random.uniform(0, 1)
        r2 = random.uniform(0, 1)
        if r1 + r2 > 1:
            r1 = 1 - r1
            r2 = 1 - r2
        r3 = 1 - (r1 + r2)
        random_point = (r1 * a.x + r2 * b.x + r3 * c.x, r1 * a.y + r2 * b.y + r3 * c.y)

        return Point(*random_point)

    def average_square_distance(self, point: "Point") -> float:
        a, b, c = self.vertices

        h = Line(a, b).get_projection_coordinate(c)
        g = self.centroid
        gc = Line(h, c).get_projection_coordinate(g)
        gy = Line(a, b).perpendicular_line(a).get_projection_coordinate(g)
        surface = self.area

        sign_ah_ab = 1 if Vector.dot_product(Vector(a, b), Vector(a, h)) > 0 else -1
        sign_hb_ab = 1 if Vector.dot_product(Vector(a, b), Vector(h, b)) > 0 else -1

        return (
            Vector(h, c).norm
            / 12
            * (
                sign_ah_ab * Vector(a, h).norm ** 3
                + sign_hb_ab * Vector(h, b).norm ** 3
                + Vector(a, b).norm * Vector(h, c).norm ** 2
            )
            + surface * Vector(a, point).norm ** 2
            + 2 * surface * Vector.dot_product(Vector(point, a), Vector(a, g))
            + surface * (Vector(g, gy).norm ** 2 - Vector(g, gc).norm ** 2)
        )
