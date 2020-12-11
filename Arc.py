import math
import numpy as np

#calculates array of Bezier control points
#for circle arc with center CX, CY and radius R

class Arc:
	# Translated to Python from https://stackoverflow.com/a/26774423/2683626
	def __init__(self, center, radius, startAngle, sweepAngle):
		self.center = center
		self.radius = radius
		self.startAngle = startAngle
		self.sweepAngle = sweepAngle
	def __repr__(self):
		return f'Arc({self.center}, {self.radius}, {self.startAngle}, {self.sweepAngle})'
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
