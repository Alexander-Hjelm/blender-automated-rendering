# Run as: blender -b <filename> -P <this_script> 
import bpy
import os
import sys
from math import radians

sceneKey = bpy.data.scenes.keys()[0] 

bpy.context.scene.render.alpha_mode = "TRANSPARENT"

cameraIndex = -1
for obj in bpy.data.objects: 
    # Find cameras 
    if ( obj.type =='CAMERA'):
        cameraIndex = cameraIndex + 1;

        # Find all meshes that are parented to the Armature
        for child_object in bpy.data.objects["Armature"].children:
            if(child_object.name.startswith("MSH_")):
                # Show current mesh
                child_object.hide_render = False;
                mesh_name = child_object.name.split("_", 1)[1] 

                #Disable all other meshes
                for child_object_2 in bpy.data.objects["Armature"].children:
                    if(child_object_2.name.startswith("MSH_")):
                        if(child_object_2 != child_object):
                            child_object_2.hide_render = True;

                # Iterate through all actions (animation clips)
                for action in bpy.data.actions:
                    bpy.data.objects["Armature"].animation_data.action = action

                    # Iterate through the frames of the current action
                    for frame in range(int(action.frame_range[1])):

                        # Set current frame
                        bpy.context.scene.frame_set(frame)
            
                        # Set Scenes camera and output filename 
                        bpy.data.scenes[sceneKey].camera = obj 
                        bpy.data.scenes[sceneKey].render.image_settings.file_format = 'PNG' 
                        bpy.data.scenes[sceneKey].render.filepath = "pixelart-out/out/" + mesh_name + "_" + action.name + "_" + str(frame) + "_dir_" + str(cameraIndex) + ".png" 

                        # Render Scene 
                        bpy.ops.render.render( write_still=True ) 
