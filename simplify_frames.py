import bpy
import bpy.types
import json


class ExtractMarkedFrames(bpy.types.Operator):
    bl_idname = "ceb.simplifyframes"
    bl_label = "Simplify"
    bl_description = "Simplify"
    bl_options = {"REGISTER", "UNDO"}

    option: bpy.props.IntProperty(name='',default=0) #0 for objects, #1 for all bones, #2 for selected bones


    def execute(self,context):
        # Pegar frames onde tem marcador
        markers = []
        for m in bpy.context.scene.timeline_markers:
            markers.append(m.frame)
        markers.sort() #order the frames

        # apagar keyframes exceto dos que estao no "markers"

        if self.option == 0: #run for objects only
            #for objects
            for f in range(markers[0],markers[-1]+1):
                for ob in context.selected_objects:
                    # Create keyframes where markers are for the current channels of the object
                    fcurves = ob.animation_data.action.fcurves
                    for frame in markers:
                        for fcurve in fcurves:
                            keyframe = fcurve.keyframe_points.insert(frame, fcurve.evaluate(frame))
                    # Remove keyframe that are not at the markers
                    if f not in markers:
                        ob.keyframe_delete(data_path='rotation_quaternion',frame=f)
                        ob.keyframe_delete(data_path='location',frame=f)
                        ob.keyframe_delete(data_path='rotation_euler',frame=f)
                        ob.keyframe_delete(data_path='scale',frame=f)

            # convert points to Bezier
            for ob in context.selected_objects:
                    for fc in ob.animation_data.action.fcurves:
                        for kp in fc.keyframe_points:
                            kp.interpolation = 'BEZIER'

        if self.option == 1: #run for all bones
            obj = context.active_object
            if obj.type == 'ARMATURE':
                fcurves = obj.animation_data.action.fcurves
                for frame in markers:
                    for fcurve in fcurves:
                        keyframe = fcurve.keyframe_points.insert(frame, fcurve.evaluate(frame))
                for f in range(markers[0],markers[-1]+1):
                        for bone in obj.pose.bones:
                            if f not in markers:
                                bone.keyframe_delete(data_path='rotation_quaternion',frame=f)
                                bone.keyframe_delete(data_path='location',frame=f)
                                bone.keyframe_delete(data_path='rotation_euler',frame=f)
                                bone.keyframe_delete(data_path='scale',frame=f)

                # for fc in ob.animation_data.action.fcurves:
                #convertendo a interpolação para bezier
                for fc in fcurves:
                    for kp in fc.keyframe_points:
                        kp.interpolation = 'BEZIER'

        if self.option == 2: #run for selected bones
            obj = context.active_object
            if obj.type == 'ARMATURE':

                # save selected bones names
                slcted_bones = []
                for sb in context.selected_pose_bones:
                    slcted_bones.append(sb.name)

                ## Create keyframes where markers are for the current channels of the selected bones
                for fc in obj.animation_data.action.fcurves:
                    if fc.data_path.split('"')[1] in slcted_bones:
                        print('bone create missing keyframe:',fc.data_path.split('"')[1])
                        for frame in markers:
                            fc.keyframe_points.insert(frame, fc.evaluate(frame))
                



                # Clear keyframes that are not at the markers
                for f in range(markers[0],markers[-1]+1):
                    for bone in context.selected_pose_bones:
                        if f not in markers:
                            bone.keyframe_delete(data_path='rotation_quaternion',frame=f)
                            bone.keyframe_delete(data_path='location',frame=f)
                            bone.keyframe_delete(data_path='rotation_euler',frame=f)
                            bone.keyframe_delete(data_path='scale',frame=f)

                #convertendo a interpolação para bezier
                for fc in obj.animation_data.action.fcurves:
                    if fc.data_path.split('"')[1] in slcted_bones:
                        print('bone to make bezier:',fc.data_path.split('"')[1])
                        for kp in fc.keyframe_points:
                            kp.interpolation = 'BEZIER'

        if self.option == 3: #run for selected fcurves
            # obj = context.active_object
            # if obj.type == 'ARMATURE':

            #     # save selected bones names
            #     slcted_bones = []
            #     for sb in context.selected_pose_bones:
            #         slcted_bones.append(sb.name)

            from .panel import get_selected_fcurves_from_anywhere
            selected_curves = get_selected_fcurves_from_anywhere()

            ## Create keyframes where markers are for the current channels of the selected bones
            for fc in selected_curves:
                # if fc.data_path.split('"')[1] in slcted_bones:
                print('bone create missing keyframe:',fc.data_path.split('"')[1])
                for frame in markers:
                    fc.keyframe_points.insert(frame, fc.evaluate(frame))

                keyframe_points = fc.keyframe_points
                for kp in reversed(keyframe_points):
                    if kp.co[0] not in markers:
                        keyframe_points.remove(kp)
                

                #convertendo a interpolação para bezier
                for fc in selected_curves:
                    # if fc.data_path.split('"')[1] in slcted_bones:
                    print('bone to make bezier:',fc.data_path.split('"')[1])
                    for kp in fc.keyframe_points:
                        kp.interpolation = 'BEZIER'


        return{'FINISHED'}
    
class ClearMarkers(bpy.types.Operator):
    bl_idname = "ceb.clear_markers"
    bl_label = "Clear Markers"
    bl_description = "Clear Markers"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self,context):
        bpy.context.scene.timeline_markers.clear()
        return{'FINISHED'}

class SimplifyAndClearMarkers(bpy.types.Operator):
    bl_idname = "ceb.simplify_and_clear_markers"
    bl_label = "Simplify & Clear"
    bl_description = "Simplify and Clear Markers"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self,context):

        bpy.ops.ceb.simplifyframes()
        bpy.ops.ceb.clear_markers()

        return{'FINISHED'}
    

class CreateMarkersFromFrames(bpy.types.Operator):
    bl_idname = "ceb.create_markers_from_frames"
    bl_label = "Create Markers From Frames"
    bl_description = "Create Markers From Frames"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self,context):

        #clear markers
        bpy.ops.ceb.clear_markers()

        # Get the active object
        obj = bpy.context.object

        # Get the animation data
        anim_data = obj.animation_data

        # Check if the object has animation data
        if anim_data is not None:
            # Get the keyframe points
            fcurves = anim_data.action.fcurves
            all_frames = []
            
            for fcurve in fcurves:
                keyframes = fcurve.keyframe_points
                for keyframe in keyframes:
                    frame = keyframe.co[0]
                    all_frames.append(frame)

            print('all_frames: ',all_frames)
            all_frames.sort()
            f_keyframes = list(set(all_frames)) #order and distinct 
            # Create a marker for each keyframe
            for f_keyframe in f_keyframes:
                bpy.context.scene.timeline_markers.new(name="F_"+str(int(f_keyframe)), frame=int(f_keyframe))

        return{'FINISHED'}


class QuickSaveMarkers(bpy.types.Operator):
    bl_idname = "ceb.quick_save_markers"
    bl_label = "Quick Save Markers"
    bl_description = "Quick Save Markers"
    bl_options = {"REGISTER", "UNDO"}

    option: bpy.props.IntProperty(name='',default=1) #escolher qual "bank" salvar

    def execute(self,context):
        sfsetting = context.scene.sfsetting
        

        markers = []
        for m in bpy.context.scene.timeline_markers:
            markers.append([m.name,m.frame])
        if self.option == 1:
            sfsetting.str_quick_save_marker1 = json.dumps(markers)
        elif self.option == 2:
            sfsetting.str_quick_save_marker2 = json.dumps(markers)
        elif self.option == 3:
            sfsetting.str_quick_save_marker3 = json.dumps(markers)
        elif self.option == 4:
            sfsetting.str_quick_save_marker4 = json.dumps(markers)
        elif self.option == 5:
            sfsetting.str_quick_save_marker5 = json.dumps(markers)
        elif self.option == 6:
            sfsetting.str_quick_save_marker6 = json.dumps(markers)
        elif self.option == 7:
            sfsetting.str_quick_save_marker7 = json.dumps(markers)
        elif self.option == 8:
            sfsetting.str_quick_save_marker8 = json.dumps(markers)
        elif self.option == 9:
            sfsetting.str_quick_save_marker9 = json.dumps(markers)
        elif self.option == 10:
            sfsetting.str_quick_save_marker10 = json.dumps(markers)
        else:
            print('Bank limit')


        return{'FINISHED'}
    
class QuickLoadMarkers(bpy.types.Operator):
    bl_idname = "ceb.quick_load_markers"
    bl_label = "Quick Load Markers"
    bl_description = "Quick Load Markers"
    bl_options = {"REGISTER", "UNDO"}

    option: bpy.props.IntProperty(name='',default=1) #escolher qual "bank" salvar

    def execute(self,context):
        sfsetting = context.scene.sfsetting

        if self.option == 1:
            quick_load = json.loads(sfsetting.str_quick_save_marker1)
        elif self.option == 2:
            quick_load = json.loads(sfsetting.str_quick_save_marker2)
        elif self.option == 3:
            quick_load = json.loads(sfsetting.str_quick_save_marker3)
        elif self.option == 4:
            quick_load = json.loads(sfsetting.str_quick_save_marker4)
        elif self.option == 5:
            quick_load = json.loads(sfsetting.str_quick_save_marker5)
        elif self.option == 6:
            quick_load = json.loads(sfsetting.str_quick_save_marker6)
        elif self.option == 7:
            quick_load = json.loads(sfsetting.str_quick_save_marker7)
        elif self.option == 8:
            quick_load = json.loads(sfsetting.str_quick_save_marker8)
        elif self.option == 9:
            quick_load = json.loads(sfsetting.str_quick_save_marker9)
        elif self.option == 10:
            quick_load = json.loads(sfsetting.str_quick_save_marker10)
        else:
            print("No more banks")

        # if sfsetting.bool_clear_before_load_quickload:
        bpy.context.scene.timeline_markers.clear()

        for ql in quick_load:
            context.scene.timeline_markers.new(ql[0], frame=ql[1])
        
        return{'FINISHED'}
    
class QuickSaveMarkersClear(bpy.types.Operator):
    bl_idname = "ceb.quick_save_markers_clear"
    bl_label = "Clear Quick Save Markers"
    bl_description = "Clear Quick Save Markers"
    bl_options = {"REGISTER", "UNDO"}

    option: bpy.props.IntProperty(name='',default=0) #0 limpa todos

    def execute(self,context):
        sfsetting = context.scene.sfsetting

        if self.option == 0:
            sfsetting.str_quick_save_marker1 = ''
            sfsetting.str_quick_save_marker2 = ''
            sfsetting.str_quick_save_marker3 = ''
            sfsetting.str_quick_save_marker4 = ''
            sfsetting.str_quick_save_marker5 = ''
            sfsetting.str_quick_save_marker6 = ''
            sfsetting.str_quick_save_marker7 = ''
            sfsetting.str_quick_save_marker8 = ''
            sfsetting.str_quick_save_marker9 = ''
            sfsetting.str_quick_save_marker10 = ''

        elif self.option == 1:
            sfsetting.str_quick_save_marker1 = ''
        elif self.option == 2:
            sfsetting.str_quick_save_marker2 = ''
        elif self.option == 3:
            sfsetting.str_quick_save_marker3 = ''
        elif self.option == 4:
            sfsetting.str_quick_save_marker4 = ''
        elif self.option == 5:
            sfsetting.str_quick_save_marker5 = ''
        elif self.option == 6:
            sfsetting.str_quick_save_marker6 = ''
        elif self.option == 7:
            sfsetting.str_quick_save_marker7 = ''
        elif self.option == 8:
            sfsetting.str_quick_save_marker8 = ''
        elif self.option == 9:
            sfsetting.str_quick_save_marker9 = ''
        elif self.option == 10:
            sfsetting.str_quick_save_marker10 = ''

        else:
            print("No more banks")
        
        return{'FINISHED'}
