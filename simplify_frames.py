import bpy
import bpy.types
import json

bl_info = {
    "name" : "CEB Simply Frames",
    "author" : "Carlos Barreto",
    "description" : "",
    "blender" : (4, 0, 0),
    "version" : (2, 1, 0),
    "location" : "UI > SidePanel",
    "warning" : "",
    "category" : "General"
}
# 2.1 - Added create markers from keyframes
#       Added create keyframes where markers are (if there isnt)
#       Fix the range where the keyframes were deleted (in relation to the markers)
class SimplifyFrames(bpy.types.Panel):
    bl_label = "Simplify frames"
    bl_category = "CEB"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        sfsetting = context.scene.sfsetting
        obj = context.object

        row = layout.column()
        # row.prop(sfsetting,'enum_mode')
        if obj.type == 'ARMATURE':
            obj_text = "Bones"
        else:
            obj_text = "Objects"
        row.label(text="Simplify "+obj_text)
        if obj.type == 'ARMATURE':
            row.operator("ceb.simplifyframes",text="Simplify All Bones").option=1
            row_slct_bones = row.column(align=True)
            if context.selected_pose_bones is not None and len(context.selected_pose_bones) > 0:
                row_slct_bones.enabled = True
            else:
                row_slct_bones.enabled = False
            row_slct_bones.operator("ceb.simplifyframes",text="Simplify Selected Bones").option=2
        else:
            row.operator("ceb.simplifyframes",text="Simplify Selected Objs").option=0
        row.separator()
        row.operator("ceb.clear_markers")
        row.operator("ceb.simplify_and_clear_markers")
        row.separator()
        row.operator("ceb.create_markers_from_frames")
        row = layout.column()
        row.separator()
        row.label(text="Quick Save/Load")
        
        # row = layout.row()
        row = layout.column()
        row.prop(sfsetting,'str_qs_label1',text='QS 1')
        if sfsetting.str_qs_label1 != '' or sfsetting.str_quick_save_marker1 != '':
            row_qs_ql = row.row(align=True)
            row_qs_ql.operator('ceb.quick_save_markers',text='QS 1').option=1
            row_ql = row_qs_ql.row(align=True)
            row_ql.enabled = False if sfsetting.str_quick_save_marker1 == '' else True
            row_ql.operator('ceb.quick_load_markers',text='QL 1').option=1
            row_ql.operator('ceb.quick_save_markers_clear',text='X').option=1

        row = layout.column()
        row.prop(sfsetting,'str_qs_label2',text='QS 2')
        if sfsetting.str_qs_label2 != '' or sfsetting.str_quick_save_marker2 != '':
            row_qs_ql = row.row(align=True)
            row_qs_ql.operator('ceb.quick_save_markers',text='QS 2').option=2
            row_ql = row_qs_ql.row(align=True)
            row_ql.enabled = False if sfsetting.str_quick_save_marker2 == '' else True
            row_ql.operator('ceb.quick_load_markers',text='QL 2').option=2
            row_ql.operator('ceb.quick_save_markers_clear',text='X').option=2

        row = layout.column()
        row.prop(sfsetting,'str_qs_label3',text='QS 3')
        if sfsetting.str_qs_label3 != '' or sfsetting.str_quick_save_marker3 != '':
            row_qs_ql = row.row(align=True)
            row_qs_ql.operator('ceb.quick_save_markers',text='QS 3').option=3
            row_ql = row_qs_ql.row(align=True)
            row_ql.enabled = False if sfsetting.str_quick_save_marker3 == '' else True
            row_ql.operator('ceb.quick_load_markers',text='QL 3').option=3
            row_ql.operator('ceb.quick_save_markers_clear',text='X').option=3

        row = layout.column()
        row.prop(sfsetting,'str_qs_label4',text='QS 4')
        if sfsetting.str_qs_label4 != '' or sfsetting.str_quick_save_marker4 != '':
            row_qs_ql = row.row(align=True)
            row_qs_ql.operator('ceb.quick_save_markers',text='QS 4').option=4
            row_ql = row_qs_ql.row(align=True)
            row_ql.enabled = False if sfsetting.str_quick_save_marker4 == '' else True
            row_ql.operator('ceb.quick_load_markers',text='QL 4').option=4
            row_ql.operator('ceb.quick_save_markers_clear',text='X').option=4

        row = layout.column()
        row.prop(sfsetting,'str_qs_label5',text='QS 5')
        if sfsetting.str_qs_label5 != '' or sfsetting.str_quick_save_marker5 != '':
            row_qs_ql = row.row(align=True)
            row_qs_ql.operator('ceb.quick_save_markers',text='QS 5').option=5
            row_ql = row_qs_ql.row(align=True)
            row_ql.enabled = False if sfsetting.str_quick_save_marker5 == '' else True
            row_ql.operator('ceb.quick_load_markers',text='QL 5').option=5
            row_ql.operator('ceb.quick_save_markers_clear',text='X').option=5

        row = layout.column()
        row.prop(sfsetting,'str_qs_label6',text='QS 6')
        if sfsetting.str_qs_label6 != '' or sfsetting.str_quick_save_marker6 != '':
            row_qs_ql = row.row(align=True)
            row_qs_ql.operator('ceb.quick_save_markers',text='QS 6').option=6
            row_ql = row_qs_ql.row(align=True)
            row_ql.enabled = False if sfsetting.str_quick_save_marker6 == '' else True
            row_ql.operator('ceb.quick_load_markers',text='QL 6').option=6
            row_ql.operator('ceb.quick_save_markers_clear',text='X').option=6

        row = layout.column()
        row.prop(sfsetting,'str_qs_label7',text='QS 7')
        if sfsetting.str_qs_label7 != '' or sfsetting.str_quick_save_marker7 != '':
            row_qs_ql = row.row(align=True)
            row_qs_ql.operator('ceb.quick_save_markers',text='QS 7').option=7
            row_ql = row_qs_ql.row(align=True)
            row_ql.enabled = False if sfsetting.str_quick_save_marker7 == '' else True
            row_ql.operator('ceb.quick_load_markers',text='QL 7').option=7
            row_ql.operator('ceb.quick_save_markers_clear',text='X').option=7

        row = layout.column()
        row.prop(sfsetting,'str_qs_label8',text='QS 8')
        if sfsetting.str_qs_label8 != '' or sfsetting.str_quick_save_marker8 != '':
            row_qs_ql = row.row(align=True)
            row_qs_ql.operator('ceb.quick_save_markers',text='QS 8').option=8
            row_ql = row_qs_ql.row(align=True)
            row_ql.enabled = False if sfsetting.str_quick_save_marker8 == '' else True
            row_ql.operator('ceb.quick_load_markers',text='QL 8').option=8
            row_ql.operator('ceb.quick_save_markers_clear',text='X').option=8

        row = layout.column()
        row.prop(sfsetting,'str_qs_label9',text='QS 9')
        if sfsetting.str_qs_label9 != '' or sfsetting.str_quick_save_marker9 != '':
            row_qs_ql = row.row(align=True)
            row_qs_ql.operator('ceb.quick_save_markers',text='QS 9').option=9
            row_ql = row_qs_ql.row(align=True)
            row_ql.enabled = False if sfsetting.str_quick_save_marker9 == '' else True
            row_ql.operator('ceb.quick_load_markers',text='QL 9').option=9
            row_ql.operator('ceb.quick_save_markers_clear',text='X').option=9

        row = layout.column()
        row.prop(sfsetting,'str_qs_label10',text='QS 10')
        if sfsetting.str_qs_label10 != '' or sfsetting.str_quick_save_marker10 != '':
            row_qs_ql = row.row(align=True)
            row_qs_ql.operator('ceb.quick_save_markers',text='QS 10').option=10
            row_ql = row_qs_ql.row(align=True)
            row_ql.enabled = False if sfsetting.str_quick_save_marker10 == '' else True
            row_ql.operator('ceb.quick_load_markers',text='QL 10').option=10
            row_ql.operator('ceb.quick_save_markers_clear',text='X').option=10

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
    
class SFSettings(bpy.types.PropertyGroup):
    str_quick_save_marker1: bpy.props.StringProperty(name='Quick Save Marker 1')
    str_quick_save_marker2: bpy.props.StringProperty(name='Quick Save Marker 2')
    str_quick_save_marker3: bpy.props.StringProperty(name='Quick Save Marker 3')
    str_quick_save_marker4: bpy.props.StringProperty(name='Quick Save Marker 4')
    str_quick_save_marker5: bpy.props.StringProperty(name='Quick Save Marker 5')
    str_quick_save_marker6: bpy.props.StringProperty(name='Quick Save Marker 6')
    str_quick_save_marker7: bpy.props.StringProperty(name='Quick Save Marker 7')
    str_quick_save_marker8: bpy.props.StringProperty(name='Quick Save Marker 8')
    str_quick_save_marker9: bpy.props.StringProperty(name='Quick Save Marker 9')
    str_quick_save_marker10: bpy.props.StringProperty(name='Quick Save Marker 10')

    str_qs_label1: bpy.props.StringProperty(name='Quick Save Label 1')
    str_qs_label2: bpy.props.StringProperty(name='Quick Save Label 2')
    str_qs_label3: bpy.props.StringProperty(name='Quick Save Label 3')
    str_qs_label4: bpy.props.StringProperty(name='Quick Save Label 4')
    str_qs_label5: bpy.props.StringProperty(name='Quick Save Label 5')
    str_qs_label6: bpy.props.StringProperty(name='Quick Save Label 6')
    str_qs_label7: bpy.props.StringProperty(name='Quick Save Label 7')
    str_qs_label8: bpy.props.StringProperty(name='Quick Save Label 8')
    str_qs_label9: bpy.props.StringProperty(name='Quick Save Label 9')
    str_qs_label10: bpy.props.StringProperty(name='Quick Save Label 10')

    # enum_mode : bpy.props.EnumProperty(
    #     name="Mode",
    #     description="Choose a mode",
    #     items=[
    #         ("bone","bone","bone"),
    #         ("object","object","object"),
    #     ],)

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

def register():
    bpy.utils.register_class(SimplifyFrames)
    bpy.utils.register_class(ExtractMarkedFrames)
    bpy.utils.register_class(ClearMarkers)
    bpy.utils.register_class(SimplifyAndClearMarkers)
    bpy.utils.register_class(CreateMarkersFromFrames)
    bpy.utils.register_class(QuickSaveMarkers)
    bpy.utils.register_class(QuickLoadMarkers)
    bpy.utils.register_class(QuickSaveMarkersClear)
    bpy.utils.register_class(SFSettings)
    bpy.types.Scene.sfsetting = bpy.props.PointerProperty(type=SFSettings)

def unregister():
    bpy.utils.unregister_class(SimplifyFrames)
    bpy.utils.unregister_class(ExtractMarkedFrames)
    bpy.utils.unregister_class(ClearMarkers)
    bpy.utils.unregister_class(SimplifyAndClearMarkers)
    bpy.utils.unregister_class(CreateMarkersFromFrames)
    bpy.utils.unregister_class(QuickSaveMarkers)
    bpy.utils.unregister_class(QuickLoadMarkers)
    bpy.utils.unregister_class(QuickSaveMarkersClear)
    bpy.utils.unregister_class(SFSettings)

if __name__ == "__main__":
    register()
