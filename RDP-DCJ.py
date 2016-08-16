### Source: http://codereview.stackexchange.com/questions/49809/python-implementation-of-the-ramer-douglas-peucker-algorithm ###

### Import modules ###
import turtle, random, math

### Generate random seed ###
random.seed()

### Create point class ###
class Points:   
    def __init__(self, xcor, ycor):
        self.xcor = xcor
        self.ycor = ycor  

### Create turtle window ###
turtle.reset()
turtle.setworldcoordinates(0,0,128,160)
turtle.tracer(False)
turtle.hideturtle()

### Create raw points ###
raw = [0]*128
raw [0] = 20
raw [10] = 53       
raw [20] = 34
raw [30] = 69
raw [40] = 87
raw [50] = 103
raw [60] = 80
raw [70] = 137
raw [80] = 95
raw [90] = 67
raw [100] = 54
raw [110] = 40
raw [120] = 39
raw [127] = 34

firstval = 0
lastval = 0
for i in range(128):
    if raw[i] == 0:
        try:
            for j in range(i+1, 128):
                if raw[j] != 0:
                    firstval = raw[j]
                    for k in range(j+1, 128):
                        if raw[k] != 0:
                            lastval = raw[k]
                            break
                    break
            if firstval < lastval:
                raw[i] = random.randint(firstval, lastval)
            elif firstval > lastval:
                raw[i] = random.randint(lastval, firstval)
            else:
                raw[i] = random.randint(lastval-4, lastval+4)
        except IndexError:
            pass
        except ValueError:
            pass

### Draw raw points ###
rplist = []
for rawpoint in range(len(raw)):
    rp = Points(rawpoint, raw[rawpoint])
    rpturtle = turtle.Turtle()
    rpturtle.up()
    rpturtle.hideturtle()
    rpturtle.goto(rp.xcor,rp.ycor)
    rpturtle.dot()
    rplist.append(rpturtle)

rawdraw = turtle.Turtle()
rawdraw.up()
rawdraw.hideturtle()
rawdraw.goto(rplist[0].position())
rawdraw.down()
for rpturtle in rplist:
    rawdraw.goto(rpturtle.position())

### Ramer-Douglas-Peucker Algorithm ###
NegInf = float('-inf')
#Calculate the distance between two points
def distance(v1,v2):    #v1 and v2 refer to the vertices of two points
    dx = v2[0] - v1[0]
    dy = v2[1] - v1[1]
    return dx*dx + dy*dy

#Calculate the perpendicular distance from a point to a line
def perpendicular_distance(point, line_start, line_end):
    x1, y1 = line_start
    x2, y2 = line_end
    vx, vy = point

    if x1 == x2:
        return abs(x1 - vx)
    m = (y2 - y1)/(x2 - x1)
    b = y1 - m*x1
    return abs(m * vx - vy + b)/math.sqrt(m*m + 1)

def _rdp_approx(points, tolerance, depth):
    """
    Internal Function: Recursively perform the RDP algorithm.
    """
    if not points:
        # In case the furthest point index discovered is equal to the length of the
        # list of points, leading to points[furthest:] sending in an empty list.
        return []
    elif len(points) <= 2:
        # BASE CASE:: No points to remove, only the start and the end points of the line.
        # Return it.
        return points
    elif len(points) == 3:
        # BASE CASE:: Our decomposition of the polygon has reached a minimum of 3 points.
        # Now all that is left is to remove the point in the middle (assuming it's distance
        # from the line is greater than the set tolerance).
        dist = perpendicular_distance(points[1],
                                      points[0],
                                      points[2]
                                      )
        if dist < tolerance:
            return [points[0], points[-1]]
        return points

    max_dist = NegInf
    furthest = None

    start = 0
    start_point = points[start]

    if depth == 1:
        # In the initial approximation, we are given an entire polygon to approximate. This
        # means that the start and end points are the same, thus we cannot use the perpendicular
        # distance equation to calculate the distance a point is from the start since the start is
        # not a line. We have to use ordinary distance formula instead.
        get_distance = lambda point: distance(point, start_point)
    else:
        end_point = points[-1]
        get_distance = lambda point: perpendicular_distance(point, start_point, end_point)

    # Find the farthest point from the norm.
    for i, point in enumerate(points[1:], 1):
        dist = get_distance(point)
        if dist > max_dist:
            max_dist = dist
            furthest = i

    # Recursively calculate the RDP approximation of the two polygonal chains formed by
    # slicing at the index of the furthest discovered point.
    prev_points = _rdp_approx(points[:furthest+1], tolerance, depth+1)
    next_points = _rdp_approx(points[furthest:], tolerance, depth+1)

    new_points = []
    for point in prev_points + next_points:
        # Filter out the duplicate points whilst maintaining order.
        # TODO:: There's probably some fancy slicing trick I just haven't figured out
        # that can be applied to prev_points and next_points so that we don't have to
        # do this, but it's not a huge bottleneck so we needn't worry about it now.
        if point not in new_points:
            new_points.append(point)

    return new_points 

def rdp_polygon_approximate(coordinates, tolerance):
    """
    Use the Ramer-Douglas-Peucker algorithm to approximate the points on a polygon.

    The RDP algorithm recursively cuts away parts of a polygon that stray from the
    average of the edges. It is a great algorithm for maintaining the overall form
    of the input polygon, however one should be careful when using this for larger
    polygons as the algorithm has an average complexity of T(n) = 2T(n/2) + O(n) and
    a worst case complexity of O(n^2).

    PARAMETERS
    ==========
        coordinates >> The coordinates of the polygon to approximate.

        tolerance >> The amount of tolerance the algorithm will use. The tolerance
            determines the minimum distance a point has to sway from the average
            before it gets deleted from the polygon. Thus, setting the tolerance to
            be higher should delete more points on the final polygon.

            That said, due to how the algorithm works there is a limit to the number
            of vertices that can be removed on a polygon. Setting the tolerance to
            float('inf') or sys.maxsize will not approximate the polygon to a single
            point. Usually the minimum points an approximated polygon can have if the
            original polygon had N points is between 2N/3 and N/3.

    FURTHER READING
    ===============
    For further reading on the Ramer-Douglas-Peucker algorithm, see
    http://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm
    """
    return _rdp_approx(coordinates, tolerance, 1)

### Put all raw coordinates into a list as a tuple ###
rpcor = []
for rpturtle in rplist:
    x, y = rpturtle.position()
    rpcor.append((x,y))

oldrdplist = rdp_polygon_approximate(rpcor, 20)

test = len(oldrdplist)

for i in range(1000):
    if len(rdp_polygon_approximate(oldrdplist, 20)) < test:
        test = len(rdp_polygon_approximate(oldrdplist, 20))
        oldrdplist = rdp_polygon_approximate(oldrdplist, 20)
    
xrdplist = [x[0] for x in oldrdplist]
xrdplistforDCJ = [x[0] for x in oldrdplist]
yrdplist = [x[1] for x in oldrdplist]

### Draw the RDP Algorithm line ###
rdpturtle = turtle.Turtle()
rdpturtle.up()
rdpturtle.color("green")
rdpturtle.goto(0,yrdplist[0])
rdpturtle.down()
rdpturtle.hideturtle()
rdpturtle.width(3)
for i in range(len(xrdplist)):
    rdpturtle.goto(xrdplist[i],yrdplist[i])

### DeCasteljau Algorithm ###
refined = []
refinedlist = []
def deCasteljau(args,t,i):
    global refined, refinedlist
    
    if(len(args) == 1):
        refined.append(args[0])
        refinedpoint = Points(i,args[0])
        refinedturtle = turtle.Turtle()
        refinedturtle.up()
        refinedturtle.color("blue")
        refinedturtle.hideturtle()
        refinedturtle.goto(xrdplistforDCJ
                           .pop(0), refinedpoint.ycor)
        refinedturtle.dot()
        refinedlist.append(refinedturtle)
        
        return args[0]

    newArgs = [0] * (len(args) - 1)
    for j in range(len(newArgs)):
        newArgs[j] = (1-t) * args[j] + t*args[j+1]
        
    deCasteljau(newArgs,t,i)

### Using deCasteljau Algorithm ###
for i in range(len(yrdplist)):
    t = i/len(yrdplist)
    deCasteljau(yrdplist,t,i)

### Extrapolate lines ###
eturtle = turtle.Turtle()
eturtle.up()
eturtle.color("blue")
eturtle.hideturtle()
eturtle.goto(refinedlist[0].position())
eturtle.down()
eturtle.width(3)
for refinedturtle in refinedlist:
    eturtle.goto(refinedturtle.position())

### Calculate area under 3 halves of the graph ###
check_division = len(refined)
L_division = int(check_division/3)
M_division = L_division
R_division = check_division - L_division - M_division

Larea = 0
Marea = 0
Rarea = 0
for i in range(L_division):
    Larea += refined[i] * (xrdplist[i+1]-xrdplist[i])
for i in range(L_division, M_division + L_division):
    Marea += refined[i] * (xrdplist[i+1]-xrdplist[i])
for i in range(M_division + L_division , check_division-1):
    Rarea += refined[i] * (xrdplist[i+1]-xrdplist[i])

if Larea>Marea and Larea>Rarea:
    print("Turn left")
elif Marea>Larea and Marea>Rarea:
    print("Go straight")
elif Rarea>Larea and Rarea>Marea:
    print("Turn right")

turtle.update()   
turtle.done()
