import numpy as np
import json
import math
import bpy

class BlenderBezier:
	def __init__(self):
		self.curve = bpy.data.curves.new('crv', 'CURVE')
		self.curve.dimensions = '3D'
		self.spline = self.curve.splines.new(type='BEZIER')
		self.object = bpy.data.objects.new('object_name', self.curve)
		bpy.context.scene.objects.link(self.object)
	def moveTo(self, point):
		self.spline.bezier_points[0].co = tuple(point)
		self.spline.bezier_points[0].handle_left_type = 'VECTOR'
	def bezierTo(self, handle1, handle2, point):
		self.spline.bezier_points.add(1)
		self.spline.bezier_points[-2].handle_right_type = 'FREE'
		self.spline.bezier_points[-2].handle_right = tuple(handle1)
		self.spline.bezier_points[-1].co = tuple(point)
		self.spline.bezier_points[-1].handle_left_type = 'FREE'
		self.spline.bezier_points[-1].handle_left = tuple(handle2)
	def lineTo(self, point):
		self.spline.bezier_points.add(1)
		self.spline.bezier_points[-2].handle_right_type = 'VECTOR'
		self.spline.bezier_points[-1].co = tuple(point)
		self.spline.bezier_points[-1].handle_left_type = 'VECTOR'
		self.spline.bezier_points[-1].handle_right_type = 'VECTOR'

class UVCoordinateMapToPlaneIn3DSpace:
	def __init__(self, O, U, V):
		self.O = O
		self.U = U
		self.V = V
		xyDivisor = U[0] * V[1] - V[0] * U[1]
		xzDivisor = U[0] * V[2] - V[0] * U[2]
		yzDivisor = U[1] * V[2] - V[1] * U[2]
		divisors = (xyDivisor, xzDivisor, yzDivisor)
		maxDivisor = max(divisors, key=abs)
		maxDivisorIndex = divisors.index(maxDivisor)
		valuePairs = ((0, 1), (0, 2), (1, 2))
		valuePair = valuePairs[maxDivisorIndex]
		self._divisor = maxDivisor
		self._valuePair = valuePair
	#def __repr__(self):
		#return f"UVCoordinateMapToPlaneIn3DSpace({self.O}, {self.U}, {self.V})"
	def XYZToUV(self, point):
		i = self._valuePair[0]
		j = self._valuePair[1]
		u = ((point[i] - self.O[i]) * self.V[j] - (point[j] - self.O[j]) * self.V[i]) / self._divisor
		v = ((point[j] - self.O[j]) * self.U[i] - (point[i] - self.O[i]) * self.U[j]) / self._divisor
		return np.array([u, v])
	def UVToXYZ(self, point):
		return np.array(list(map(lambda i: self.O[i] + point[0] * self.U[i] + point[1] * self.V[i], (0, 1, 2))))

def createUVCoordinateMapToPlaneIn3DSpaceFrom3Points(p1, p2, p3):

	# These two vectors are in the plane
	v1 = p3 - p1
	v2 = p2 - p1

	# the cross product is a vector normal to the plane
	cp = np.cross(v1, v2)

	uVector = p2 - p1
	vVector = np.cross(cp, uVector)
	u = uVector / np.linalg.norm(uVector)
	v = vVector / np.linalg.norm(vVector)

	return UVCoordinateMapToPlaneIn3DSpace(p1, u, v)

UVCoordinateMapToPlaneIn3DSpace.from3Points = createUVCoordinateMapToPlaneIn3DSpaceFrom3Points

class Arc:
	# Translated to Python from https://stackoverflow.com/a/26774423/2683626
	def __init__(self, center, radius, startAngle, sweepAngle):
		self.center = center
		self.radius = radius
		self.startAngle = startAngle
		self.sweepAngle = sweepAngle
	#def __repr__(self):
		#return f'Arc({self.center}, {self.radius}, {self.startAngle}, {self.sweepAngle})'
	def approximateAsBezierCurves(self):
		if(self.sweepAngle == 0):
			return

		curves = list()

		# if SweepAngle is too large, divide arc to smaller ones
		nCurves = math.ceil(abs(self.sweepAngle) / (math.pi/2))
		aSweep = self.sweepAngle / nCurves

		# calculates control points for Bezier approx. of arc with radius=1,
		# circle center at (0,0), middle of arc at (1,0)

		x0 = math.cos(aSweep / 2)
		y0 = math.sin(aSweep / 2)
		tx = (1 - x0) * 4 / 3
		ty = y0 - tx * x0 / (y0 + 0.0001)

		templateBezier = [
			np.array([x0, -y0]),
			np.array([x0 + tx, -ty]),
			np.array([x0 + tx, ty]),
			np.array([x0, y0])
		]

		for iCurve in range(nCurves):
			aStart = self.startAngle + aSweep * iCurve
			# rotation and translation of control points
			sweepVector = np.array([
				math.sin(aStart + aSweep / 2),
				math.cos(aStart + aSweep / 2)
			])
			curve = list()
			for i in range(0, 4):
				point = self.center + np.array([
					self.radius * np.cross(templateBezier[i], sweepVector),
					self.radius * np.dot(templateBezier[i], sweepVector)
				])
				curve.append(point)
			curves.append(curve)

		return curves









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

blenderPath = BlenderBezier()

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
