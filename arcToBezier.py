import math

#calculates array of Bezier control points
#for circle arc with center CX, CY and radius R
def arcToBezier(cX, cY, r, startAngle, sweepAngle):
# Translated to Python from https://stackoverflow.com/a/26774423/2683626

	curves = list()

	px = list()
	py = list()

	if(sweepAngle == 0):
		return
	# if SweepAngle is too large, divide arc to smaller ones
	nCurves = math.ceil(abs(sweepAngle) / (math.pi/2))
	aSweep = sweepAngle / nCurves

	# calculates control points for Bezier approx. of arc with radius=1,
	# circle center at (0,0), middle of arc at (1,0)

	y0 = math.sin(aSweep / 2)
	x0 = math.cos(aSweep / 2)
	tx = (1 - x0) * 4 / 3
	ty = y0 - tx * x0 / (y0 + 0.0001)

	px.append(x0)
	py.append(-y0)
	px.append(x0 + tx)
	py.append(-ty)
	px.append(x0 + tx)
	py.append(ty)
	px.append(x0)
	py.append(y0)

	# rotation and translation of control points
	sn = math.sin(startAngle + aSweep / 2)
	cs = math.cos(startAngle + aSweep / 2)

	x = cX + round(r * (px[0] * cs - py[0] * sn), 6)
	y = cY + round(r * (px[0] * sn + py[0] * cs), 6)

	curves.append((x, y))
	svgPath = "M" + ",".join((str(x), str(y)))

	for iCurve in range(nCurves):
		aStart = startAngle + aSweep * iCurve
		sn = math.sin(aStart + aSweep / 2)
		cs = math.cos(aStart + aSweep / 2)
		curve = list()
		curveSVG = list()
		for i in range(1, 4):
			x = cX + round(r * (px[i] * cs - py[i] * sn), 6)
			y = cY + round(r * (px[i] * sn + py[i] * cs), 6)
			curve.append((x, y))
			pointText = (str(x), str(y))
			curveSVG.append(",".join(pointText))
		curves.append(curve)
		svgPath += " C" + " ".join(curveSVG)

	#return curves
	return svgPath

print(arcToBezier(200, 200, 100, math.pi * .3, -math.pi * 1.4))
