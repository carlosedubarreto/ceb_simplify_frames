import bpy
from . simplify_frames import *


from bpy.props import (StringProperty,
                        BoolProperty,
                        FloatProperty,
                        IntProperty,
                        EnumProperty,
                        PointerProperty
                        )
from bpy.types import (PropertyGroup)

def is_graph_editor_open(context):
    """Checks if any area in the current screen is displaying the Graph Editor."""
    
    # Iterate through all screen layouts
    current_screen = context.screen
    for screen in bpy.data.screens:
        if screen == current_screen:
            # Iterate through all areas in the screen
            for area in screen.areas:
                # Check the 'type' property of the area
                if area.type == 'GRAPH_EDITOR':
                    # print(f"Graph Editor is open in screen: {screen.name}")
                    return True

def get_selected_fcurves_from_anywhere():
    """
    Retrieves selected F-Curves by overriding the context to a Graph Editor area.
    """
    # 1. Find the first open Graph Editor Area
    graph_area = None
    for area in bpy.context.screen.areas:
        if area.type == 'GRAPH_EDITOR':
            graph_area = area
            break
    #
    if not graph_area:
        # print("Error: No Graph Editor area is open in the current screen.")
        return []
    #
    # 2. Use a Context Override
    # This temporarily changes the context for the code block inside 'with'
    with bpy.context.temp_override(area=graph_area):
        # Now, this property correctly accesses the selection from the found area
        selected_curves = bpy.context.selected_editable_fcurves
        #   
        if selected_curves:
            # print(f"Found {len(selected_curves)} selected F-Curves (via context override).")
            # Example: Iterate and print their data path
            # for fcurve in selected_curves:
            #     print(f"  - {fcurve.data_path}[{fcurve.array_index}]")
            return selected_curves
        else:
            # print("No F-Curves selected in the Graph Editor.")
            return []

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
        if obj and obj.type == 'ARMATURE':
            obj_text = "Bones"
        else:
            obj_text = "Objects"
        row.label(text="Simplify "+obj_text)
        if obj and obj.type == 'ARMATURE':
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
        row.prop(sfsetting,'bool_show_quick_save_markers')

        graph_editor = is_graph_editor_open(context)
        if graph_editor:
            box = layout.box()
            col = box.column(align=True)
            col.label(text='Graph Editor Option')
            col.operator("ceb.simplifyframes",text="Simplify Selected Fcurves").option=3
            selected_curves = get_selected_fcurves_from_anywhere()
            path_small = ''
            axis= ''
            if selected_curves:
                col.label(text='Selected Curves')
                for fcurve in selected_curves:
                    bone = fcurve.data_path.split('"')[1]
                    path = fcurve.data_path.split('.')[-1]
                    if path == 'rotation_quaternion':
                        path_small = 'Rot Quat'
                    elif path == 'location':
                        path_small = 'Loc'
                    elif path == 'rotation_euler':
                        path_small = 'Rot Euler'
                    elif path == 'scale':
                        path_small = 'Scale'
                    elif len(fcurve.data_path.split('"')) > 3:
                        path_small = fcurve.data_path.split('"')[-2]
                    else:
                        path_small = path
                    if path in  ['location','rotation_euler','scale','rotation_quaternion']:
                        if path in  ['location','rotation_euler','scale']:
                            if fcurve.array_index == 0:
                                axis = 'X'
                            elif fcurve.array_index == 1:
                                axis = 'Y'
                            elif fcurve.array_index == 2:
                                axis = 'Z'
                            else:
                                axis = str(fcurve.array_index)
                        elif path == 'rotation_quaternion':
                            if fcurve.array_index == 0:
                                axis = 'W'
                            elif fcurve.array_index == 1:
                                axis = 'X'
                            elif fcurve.array_index == 2:
                                axis = 'Y'
                            elif fcurve.array_index == 3:
                                axis = 'Z'
                            else:
                                axis = str(fcurve.array_index)
                        
                    col.label(text=f'{bone}-{path_small}-{axis}')
                    


        if sfsetting.bool_show_quick_save_markers:
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


class SFSettings(bpy.types.PropertyGroup):
    bool_show_quick_save_markers: bpy.props.BoolProperty(name='Show Quick Save Markers',default=False) # type:ignore
    str_quick_save_marker1: bpy.props.StringProperty(name='Quick Save Marker 1') # type:ignore
    str_quick_save_marker2: bpy.props.StringProperty(name='Quick Save Marker 2') # type:ignore
    str_quick_save_marker3: bpy.props.StringProperty(name='Quick Save Marker 3') # type:ignore
    str_quick_save_marker4: bpy.props.StringProperty(name='Quick Save Marker 4') # type:ignore
    str_quick_save_marker5: bpy.props.StringProperty(name='Quick Save Marker 5') # type:ignore
    str_quick_save_marker6: bpy.props.StringProperty(name='Quick Save Marker 6') # type:ignore
    str_quick_save_marker7: bpy.props.StringProperty(name='Quick Save Marker 7') # type:ignore
    str_quick_save_marker8: bpy.props.StringProperty(name='Quick Save Marker 8') # type:ignore
    str_quick_save_marker9: bpy.props.StringProperty(name='Quick Save Marker 9') # type:ignore
    str_quick_save_marker10: bpy.props.StringProperty(name='Quick Save Marker 10') # type:ignore

    str_qs_label1: bpy.props.StringProperty(name='Quick Save Label 1') # type:ignore
    str_qs_label2: bpy.props.StringProperty(name='Quick Save Label 2') # type:ignore
    str_qs_label3: bpy.props.StringProperty(name='Quick Save Label 3') # type:ignore
    str_qs_label4: bpy.props.StringProperty(name='Quick Save Label 4') # type:ignore
    str_qs_label5: bpy.props.StringProperty(name='Quick Save Label 5') # type:ignore
    str_qs_label6: bpy.props.StringProperty(name='Quick Save Label 6') # type:ignore
    str_qs_label7: bpy.props.StringProperty(name='Quick Save Label 7') # type:ignore
    str_qs_label8: bpy.props.StringProperty(name='Quick Save Label 8') # type:ignore
    str_qs_label9: bpy.props.StringProperty(name='Quick Save Label 9') # type:ignore
    str_qs_label10: bpy.props.StringProperty(name='Quick Save Label 10') # type:ignore

    # enum_mode : bpy.props.EnumProperty(
    #     name="Mode",
    #     description="Choose a mode",
    #     items=[
    #         ("bone","bone","bone"),
    #         ("object","object","object"),
    #     ],)
