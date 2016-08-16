import turtle, random, math

### Generate random seed ###
random.seed()

### Set point class to set coordinates ###
class Points:   
    def __init__(self, xcor, ycor):
        self.xcor = xcor
        self.ycor = ycor        
            
### Create turtle window ###
turtle.reset()
turtle.setworldcoordinates(0,0,128,160)
turtle.tracer(False)
turtle.hideturtle()

### Set ccd_raw data points ###
ccd_raw = [0] * 128
ccd_raw [0] = 69
ccd_raw [10] = 53       
ccd_raw [20] = 34
ccd_raw [30] = 69
ccd_raw [40] = 87
ccd_raw [50] = 78
ccd_raw [60] = 55
ccd_raw [70] = 66
ccd_raw [80] = 43
ccd_raw [90] = 67
ccd_raw [100] = 54
ccd_raw [110] = 23
ccd_raw [120] = 89
ccd_raw [127] = 90

firstval = 0
lastval = 0
for i in range(128):
    if ccd_raw[i] == 0:
        try:
            for j in range(i+1, 128):
                if ccd_raw[j] != 0:
                    firstval = ccd_raw[j]
                    for k in range(j+1, 128):
                        if ccd_raw[k] != 0:
                            lastval = ccd_raw[k]
                            break
                    break
            if firstval < lastval:
                ccd_raw[i] = random.randint(firstval, lastval)
            elif firstval > lastval:
                ccd_raw[i] = random.randint(lastval, firstval)
            else:
                ccd_raw[i] = random.randint(lastval-4, lastval+4)
        except IndexError:
            pass
        except ValueError:
            pass
        
### Make ccd_raw points as objects and store in a list as turtles ###
rplist = []
for rawpoint in range(len(ccd_raw)):
    rp = Points(rawpoint, ccd_raw[rawpoint])
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

### DeCasteljau Theorem ###
ccd_refined = []
refinedlist = []
def deCasteljau(args,t,i):
    global ccd_refined
    
    if(len(args) == 1):
        ccd_refined.append(args[0])
        refinedpoint = Points(i,args[0])
        refinedturtle = turtle.Turtle()
        refinedturtle.up()
        refinedturtle.color("red")
        refinedturtle.hideturtle()
        refinedturtle.goto(refinedpoint.xcor, refinedpoint.ycor)
        refinedturtle.dot()
        refinedlist.append(refinedturtle)
        
        return args[0]

    newArgs = [0] * (len(args) - 1)
    for j in range(len(newArgs)):
        newArgs[j] = (1-t) * args[j] + t*args[j+1]
        
    deCasteljau(newArgs,t,i)

### Using deCasteljau Algorithm ###
for i in range(len(ccd_raw)):
    t = i/len(ccd_raw)
    deCasteljau(ccd_raw,t,i)

### Extrapolate lines ###
eturtle = turtle.Turtle()
eturtle.up()
eturtle.color("green")
eturtle.hideturtle()
eturtle.goto(refinedlist[0].position())
eturtle.down()
#eturtle.width(5)
for refinedturtle in refinedlist:
    eturtle.goto(refinedturtle.position())

turtle.update()
turtle.done()
