import bpyPrint
import bpy

class BlenderBezier:
	def __init__(self):
		self.curve = bpy.data.curves.new('crv', 'CURVE')
		self.curve.dimensions = '3D'
		self.spline = self.curve.splines.new(type='BEZIER')
		self.object = bpy.data.objects.new('object_name', self.curve)
		bpy.context.scene.objects.link(self.object)
	def moveTo(point):
		self.spline.bezier_points[0].co = tuple(point)
	def bezierTo(handle1, handle2, point):
		self.spline.bezier_points.add(1)
		self.spline.bezier_points[-2].handle_right_type = 'FREE'
		self.spline.bezier_points[-2].handle_right = tuple(handle1)
		self.spline.bezier_points[-1].co = tuple(point)
		self.spline.bezier_points[-1].handle_left_type = 'FREE'
		self.spline.bezier_points[-1].handle_left = tuple(handle1)
	def lineTo(point):
		self.spline.bezier_points.add(1)
		self.spline.bezier_points[-2].handle_right_type = 'VECTOR'
		self.spline.bezier_points[-1].co = tuple(point)
		self.spline.bezier_points[-1].handle_left_type = 'VECTOR'
