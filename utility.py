from plotter import Plotter


def read_csv(file):
    """Reads a .csv file to gather point data

    file -- the .csv file to be read

    Returns: a list of point lists
    """
    result = []

    try:
        with open(file, 'r') as f:
            for line in f.readlines()[1:]:
                items = line.split(',')
                items = [float(x) for x in items]
                result.append(items)

        return result
    except:
        print("An error occured")


def user_input():
    """Reads user input to gather point data

    Returns: a list of point lists
    """
    answer = ""
    points = []
    id = 1
    try:
        iterations = int(
            input("How many coordinates would you like to enter? "))

        for i in range(iterations):
            x = float(input('x coordinate: '))
            y = float(input('y coordinate: '))
            point = [id, x, y]
            points.append(point)
            id = id + 1

        return points
    except:
        print("An exception occured")


def format_data(points):
    """Creates two lists of all x's and all y's.

    Returns: two lists of x's and y's
    """
    xs = []
    ys = []

    for point in points:
        xs.append(point[1])
        ys.append(point[2])

    return xs, ys


def categorise_points(points, polygon):
    """An abstraction away from the two algorithms

    Returns: the results of points' categories
    """
    return mbv(points, polygon)


def mbv(points, polygon):
    """Calculates whether a point is inside the MBV.

    If point is inside the polygon, it is passed into the RCA function.

    points -- a list of points
    polygon -- a list of points to make a polygon

    Returns: a list of points with their calculated category
    ...
    """
    polygon_xs, polygon_ys = format_data(polygon)
    x_min = min(polygon_xs)
    x_max = max(polygon_xs)
    y_min = min(polygon_ys)
    y_max = max(polygon_ys)

    for point in points:
        x = point[1]
        y = point[2]
        
        if x_min > x > x_max or y_min > y > y_max:
            point.append("outside")
        else:
            category = rca(point, polygon)
            point.append(category)

    return points


def rca(point, polygon):
    """Calculates whether a point is inside a polygon.

    point -- a singular point
    polygon -- a list of points to make a polygon

    Returns:
    ...

    Credit to Joel Lawhead, http://geospatialpython.com/2011/08/point-in-polygon-2-on-line.html
    """

    x = point[1]
    y = point[2]
    n = len(polygon)

    if boundary(point, polygon) == "boundary":
        return "boundary"

    inside = False

    p1x, p1y = polygon[0][1:]

    for i in range(n+1):
        p2x, p2y = polygon[i % n][1:]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y

    if inside:
        return "inside"
    return "outside"


def boundary(point, polygon):
    """Calculates whether a point is on the boundary of a polygon.

    point -- a singular point
    polygon -- a list of points to make a polygon

    Returns: a string correlating to a point's boundary status.

    Credit to Alex, https://stackoverflow.com/a/17750176/12488201
    """
    n = len(polygon)
    for i in range(n):
        p1x, p1y = polygon[i][1:]
        p2x, p2y = polygon[(i+1) % n][1:]
        v1x = p2x - p1x
        v1y = p2y - p1y
        v2x = point[1] - p1x
        v2y = point[2] - p1y

        if (v1x * v2y - v1y * v2x == 0):
            if (v1x > 0):
                if (v2x / v1x > 0):
                    if (v1x * v1x + v1y * v1y >= v2x * v2x + v2y * v2y):
                        return "boundary"

    return ""


def results_to_csv(results):
    """Writes a list of points to a .csv file."""
    with open("output.csv", "w") as f:
        f.write("id,category" + "\n")

        for result in results:
            data = [str(int(result[0])), result[3]]
            f.write(','.join(data) + "\n")


def plot(points, polygon):
    """Plots points and a polygon onto a graph

    points -- a list of points
    polygon -- a list of points to make a polygon
    """
    pl = Plotter()

    polygon_xs, polygon_ys = format_data(polygon)

    for point in polygon:
        pl.add_polygon(polygon_xs, polygon_ys)

    for point in points:
        x = point[1]
        y = point[2]
        kind = point[3]
        pl.add_point(x, y, kind=kind)

    pl.show()
