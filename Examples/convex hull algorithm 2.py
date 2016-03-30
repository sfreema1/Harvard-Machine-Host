import random
import matplotlib.pyplot as plt

def _makeRandomData(numPoints=10, sqrLength=10, addCornerPoints=0):
    "Generate a list of random points within a square."
    
    # Fill a square with random points.
    min, max = 0, sqrLength
    P = []
    for i in xrange(numPoints):
        rand = random.randint
        x = rand(min+1, max-1)
        y = rand(min+1, max-1)
        P.append((x, y))

    # Add some "outmost" corner points.
    if addCornerPoints != 0:
        P = P + [(min, min), (max, max), (min, max), (max, min)]

    return P

def _getColumn(list_, columnIndex):
	"Return all the elements of the given column of a 2D list"

	colList = []
	for index in range(len(list_)):
		colList.append(list_[index][columnIndex])

	return colList

s = _makeRandomData(100,100,1)
x = _getColumn(s,0)
y = _getColumn(s,1)

plt.scatter(x,y,label="Scatter")
plt.show()

