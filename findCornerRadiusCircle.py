import numpy as np

def perpendicularTowardPoint(p1, p2):
	perpendicular = np.array([p1Normalized[1], -p1Normalized[0]])
	return min((perpendicular, -perpendicular, key=lambda u: np.linalg.norm(p1 + u - p2))

def thing(v1, v2, radius):
	v1Unit = v1 / np.linalg.norm(v1)
	v2Unit = v2 / np.linalg.norm(v2)
	rVector1 = perpendicularTowardPoint(v1Unit, v2Unit) * radius
	rVector2 = perpendicularTowardPoint(v2Unit, v1Unit) * radius
	cutoffLength = (rVector1 - rVector2) / (v2Unit - v1Unit)
	circleCenter = rVector1 + v1Unit * cutoffLength



v1 = p1 - p2
v2 = p3 - p2
r = 5
thing(v1, v2, r)
