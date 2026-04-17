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
    current_screen = context.screen
    for screen in bpy.data.screens:
        if screen == current_screen:
            for area in screen.areas:
                if area.type == 'GRAPH_EDITOR':
                    return True

def get_selected_fcurves_from_anywhere():
    """
    Retrieves selected F-Curves by overriding the context to a Graph Editor area.
    """
    graph_area = None
    for area in bpy.context.screen.areas:
        if area.type == 'GRAPH_EDITOR':
            graph_area = area
            break

    if not graph_area:
        return []

    with bpy.context.temp_override(area=graph_area):
        selected_curves = bpy.context.selected_editable_fcurves
        if selected_curves:
            return selected_curves
        else:
            return []


def _parse_fcurve_label(fcurve):
    """
    Safely parse a bone name, property type, and axis from an FCurve.
    Returns (bone_or_obj, path_small, axis) strings.
    """
    data_path = fcurve.data_path
    parts = data_path.split('"')

    # Bone curve: pose.bones["BoneName"].location etc.
    if len(parts) >= 2:
        bone = parts[1]
    else:
        # Object-level curve (no quoted bone name)
        bone = data_path.split('.')[-1] if '.' in data_path else data_path

    path = data_path.split('.')[-1]

    path_map = {
        'rotation_quaternion': 'Rot Quat',
        'location': 'Loc',
        'rotation_euler': 'Rot Euler',
        'scale': 'Scale',
    }

    if path in path_map:
        path_small = path_map[path]
    elif len(parts) > 3:
        path_small = parts[-2]
    else:
        path_small = path

    axis = ''
    if path in ('location', 'rotation_euler', 'scale'):
        axis = {0: 'X', 1: 'Y', 2: 'Z'}.get(fcurve.array_index, str(fcurve.array_index))
    elif path == 'rotation_quaternion':
        axis = {0: 'W', 1: 'X', 2: 'Y', 3: 'Z'}.get(fcurve.array_index, str(fcurve.array_index))

    return bone, path_small, axis


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
            if selected_curves:
                col.label(text='Selected Curves')
                for fcurve in selected_curves:
                    try:
                        bone, path_small, axis = _parse_fcurve_label(fcurve)
                        col.label(text=f'{bone}-{path_small}-{axis}')
                    except Exception:
                        col.label(text=fcurve.data_path)

        if sfsetting.bool_show_quick_save_markers:
            row.separator()
            row.label(text="Quick Save/Load")

            for i in range(1, 11):
                label_prop = f'str_qs_label{i}'
                marker_prop = f'str_quick_save_marker{i}'
                row = layout.column()
                row.prop(sfsetting, label_prop, text=f'QS {i}')
                if getattr(sfsetting, label_prop) != '' or getattr(sfsetting, marker_prop) != '':
                    row_qs_ql = row.row(align=True)
                    row_qs_ql.operator('ceb.quick_save_markers', text=f'QS {i}').option = i
                    row_ql = row_qs_ql.row(align=True)
                    row_ql.enabled = False if getattr(sfsetting, marker_prop) == '' else True
                    row_ql.operator('ceb.quick_load_markers', text=f'QL {i}').option = i
                    row_ql.operator('ceb.quick_save_markers_clear', text='X').option = i


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