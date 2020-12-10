# https://math.stackexchange.com/questions/3528493/convert-3d-point-onto-a-2d-coordinate-plane-of-any-angle-and-location-within-the






# This function takes a four-number plane definition and creates
# a UV coordinate plane based on an origin point and another point which,
# relative to the origin point, defines the direction (but not the scale) of the U axis.







import numpy as np

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
	def __repr__(self):
		return f'UVCoordinateMapToPlaneIn3DSpace({self.O}, {self.U}, {self.V})'
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



p1 = np.array([0, 0, 0])
p2 = np.array([1, 1, 0])
p3 = np.array([0, 1, 0])

uvMap = UVCoordinateMapToPlaneIn3DSpace.from3Points(p1, p2, p3)

print(uvMap)

uv = uvMap.XYZToUV(np.array([0, 1, 0]))

print(uv)

xyz = uvMap.UVToXYZ(uv)

print(xyz)
