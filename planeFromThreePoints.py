import numpy as np

def planeFromThreePoints(p1, p2, p3):

	# These two vectors are in the plane
	v1 = p3 - p1
	v2 = p2 - p1

	# the cross product is a vector normal to the plane
	cp = np.cross(v1, v2)
	a, b, c = cp

	# This evaluates a * x3 + b * y3 + c * z3 which equals d
	d = np.dot(cp, p3)

	return np.array([a, b, c, d])

p1 = np.array([1, 2, 3])
p2 = np.array([4, 6, 9])
p3 = np.array([12, 11, 9])

p1 = np.array([3, 0, 0])
p2 = np.array([0, 3, 0])
p3 = np.array([0, 0, 0])

print(planeFromThreePoints(p1, p2, p3))
