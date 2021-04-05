import sys, bpy

if "--" not in sys.argv:  # if no args are passed
    obj = "CUBE"
    obj_color = [0, 0, 0, 1]
else:
    argv = sys.argv[sys.argv.index("--") + 1:]  # get all args after "--"
    obj = argv[0]
    obj_color = [float(el) for el in argv[1].strip('[]').split(',')]

bpy.data.materials['Material'].diffuse_color = obj_color[:3]

# Create object (cube or sphere)
if obj.lower() == "cube":
    bpy.ops.mesh.primitive_cube_add()
    bpy.ops.object.material_slot_add()
    bpy.data.objects['Cube'].material_slots[''].material = bpy.data.materials['Material']
elif obj.lower() == "sphere":
    bpy.ops.mesh.primitive_uv_sphere_add()
    bpy.ops.object.material_slot_add()
    bpy.data.objects['Sphere'].material_slots[''].material = bpy.data.materials['Material']
else:
    bpy.ops.mesh.primitive_cube_add()  # Default

# Render and save image
bpy.ops.render.render(write_still=True)
# bpy.ops.wm.save_mainfile()

exit()
