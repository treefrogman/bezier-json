import bpyPrint
import bpy

coords_list = [[0,1,2], [1,2,3], [-3,2,1], [0,0,-4]]

crv = bpy.data.curves.new('crv', 'CURVE')
crv.dimensions = '3D'
spline = crv.splines.new(type='BEZIER')

spline.bezier_points[0].handle_right = (.2, 0, 0)
spline.bezier_points[0].handle_right_type = 'VECTOR'
spline.bezier_points[0].co = (.1, 0, 0)

print(spline.bezier_points[0].co)

spline.bezier_points.add(1)

spline.bezier_points[1].handle_right = (-.2, 0, 0)
spline.bezier_points[1].co = (-.1, 0, 0)
spline.bezier_points[1].handle_left_type = 'VECTOR'

# make a new object with the curve
obj = bpy.data.objects.new('object_name', crv)
bpy.context.scene.objects.link(obj)
