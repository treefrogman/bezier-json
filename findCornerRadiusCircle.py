import numpy as np
from UVCoordinateMapToPlaneIn3DSpace import UVCoordinateMapToPlaneIn3DSpace
from Arc import Arc
import json
import svgwrite
import math
from BlenderBezier import BlenderBezier

def perpendicularTowardPoint(p1, p2):
	perpendicular = np.array([p1[1], -p1[0]])
	return min((perpendicular, -perpendicular), key = lambda u: np.linalg.norm(p1 + u - p2))


def findCornerRadiusArc(v1, v2, radius):
	v1Unit = v1 / np.linalg.norm(v1)
	v2Unit = v2 / np.linalg.norm(v2)
	rVector1 = perpendicularTowardPoint(v1Unit, v2Unit) * radius
	rVector2 = perpendicularTowardPoint(v2Unit, v1Unit) * radius
	cutoffLength = (rVector1 - rVector2) / (v2Unit - v1Unit)
	circleCenter = rVector2 + v2Unit * cutoffLength
	angle1 = math.atan2(-rVector1[1], rVector1[0])
	angle2 = math.atan2(-rVector2[1], rVector2[0])
	print(circleCenter)
	print(v1Unit)
	print(v2Unit)
	print(rVector1)
	print(rVector2)
	print(angle1)
	print(angle2)

	arc = Arc(circleCenter, radius, angle1, -angle2 + angle1)

	return arc


with open('bivvy-test-simple.json') as json_file:
	data = json.load(json_file)

print(data)

dwg = svgwrite.Drawing('test2.svg', profile='full', viewBox="-20 -20 40 40")

blenderPath BlenderBezier()

for i, point in enumerate(data['points']):
	if i == 0:
		blenderPath.moveTo(point)
		continue
	if i == len(data['points']) - 1:
		blenderPath.lineTo(point)
		continue
	p1 = np.array(data['points'][i - 1])
	p2 = np.array(point)
	p3 = np.array(data['points'][i + 1])
	# p2 is the first argument so it will be the origin (0, 0) of the UV plane
	uvPlane = UVCoordinateMapToPlaneIn3DSpace.from3Points(p2, p1, p3)
	uvP1 = uvPlane.XYZToUV(p1)
	uvP2 = uvPlane.XYZToUV(p2)
	uvP3 = uvPlane.XYZToUV(p3)
	print(uvP1, uvP2, uvP3)
	arc = findCornerRadiusArc(uvP1, uvP3, data['bendRadius'])
	beziers = arc.approximateAsBezierCurves()

	blenderPath.lineTo(uvPlane.UVToXYZ(beziers[0][0]))

	for i, bezier in enumerate(beziers):
		blenderPath.bezierTo(*map(uvPlane.UVToXYZ, bezier[1:]))
