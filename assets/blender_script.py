import bpy

# Define the input BVH path, obj path and output video path directly
input_bvh_path = "/Users/hongjiji/Documents/Code/01_01.bvh"
input_obj_path = "/Users/hongjiji/Documents/Code/base_mesh.obj"  # You need to provide your mesh filename here
output_file_path = "/Users/hongjiji/Documents/Code"

# Clear all existing mesh objects (optional)
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# Clear existing armatures (optional but recommended for BVH)
bpy.ops.object.select_by_type(type='ARMATURE')
bpy.ops.object.delete()

# Import the BVH file
bpy.ops.import_anim.bvh(filepath=input_bvh_path)

rig_name = "01_01"
if rig_name in bpy.data.objects:
    rig = bpy.data.objects[rig_name]

    # Select the rig
    bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects
    rig.select_set(True)  # Select the rig

    # Set the active object to the rig (needed for the next operations)
    bpy.context.view_layer.objects.active = rig

    # Move the rig to the origin
    rig.location = (0, 0, 0)

    # Scale down the rig by 10 times
    rig.scale = (0.01, 0.01, 0.01)

# Import the OBJ mesh
bpy.ops.import_scene.obj(filepath=input_obj_path)

# Assuming the imported OBJ mesh is the last imported object
mesh = bpy.context.selected_objects[0]

# Set mesh as active object
bpy.context.view_layer.objects.active = mesh

# Deselect all and select the mesh
bpy.ops.object.select_all(action='DESELECT')
mesh.select_set(True)

# Scale down the mesh
mesh.scale = (0.27, 0.27, 0.27)

# Set the mesh's location to the origin
mesh.location = (0, 0, 0)

# ... [previous code]

# After scaling and moving the mesh to the origin

# Ensure both the mesh and rig are in object mode
bpy.ops.object.mode_set(mode='OBJECT')

# Select the mesh first
bpy.ops.object.select_all(action='DESELECT')
mesh.select_set(True)

# Now, select the rig while holding the mesh selection
rig.select_set(True)

# Set the active object to the rig, important for the next parenting step
bpy.context.view_layer.objects.active = rig

# Parent the mesh to the rig with automatic weights to link them
bpy.ops.object.parent_set(type='ARMATURE_AUTO')

# Now, the mesh is parented to the rig, and an armature modifier is added to the mesh.
# When you play the animation, the mesh should move based on the BVH animation.


# Ensure you are in object mode
bpy.ops.object.mode_set(mode='OBJECT')

# Define the vector by which you want to move the rig and the mesh
move_vector = (-1, -1, -1)  # Replace x, y, z with your desired values

# Adjust the rig's location
rig.location = (rig.location[0] + move_vector[0],
                rig.location[1] + move_vector[1],
                rig.location[2] + move_vector[2])

# Since the mesh is parented to the rig, it will automatically follow the rig's transformation.

# Set rendering engine to EEVEE
bpy.context.scene.render.engine = 'BLENDER_EEVEE'

# Set the output format to FFmpeg video
bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
bpy.context.scene.render.ffmpeg.format = 'MPEG4'
bpy.context.scene.render.ffmpeg.codec = 'H264'
bpy.context.scene.render.ffmpeg.constant_rate_factor = 'LOW'  # Low quality

bpy.context.scene.render.filepath = output_file_path

# Set render start and end frames
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 20

# Execute render operation
bpy.ops.render.render(animation=True)