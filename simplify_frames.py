import bpy
import bpy.types
import json


def get_fcurves(obj):
    """
    Returns all FCurves for the given object, compatible with Blender 5.0+.
    In 5.0, fcurves live in ChannelBags inside the action's layers/strips.
    Falls back to legacy action.fcurves for older versions.
    """
    anim_data = obj.animation_data
    if not anim_data or not anim_data.action:
        return []

    action = anim_data.action

    # Blender 5.0+: ChannelBag API
    if hasattr(action, 'layers'):
        fcurves = []
        for layer in action.layers:
            for strip in layer.strips:
                if hasattr(strip, 'channelbag'):
                    # single channelbag per strip
                    cb = strip.channelbag(anim_data.action_slot)
                    if cb:
                        fcurves.extend(cb.fcurves)
                elif hasattr(strip, 'channelbags'):
                    for cb in strip.channelbags:
                        fcurves.extend(cb.fcurves)
        return fcurves

    # Blender 4.x legacy fallback
    if hasattr(action, 'fcurves'):
        return list(action.fcurves)

    return []


def get_bone_name_from_fcurve(fcurve):
    """Safely extract bone name from fcurve data_path. Returns None if not a bone curve."""
    parts = fcurve.data_path.split('"')
    if len(parts) >= 2:
        return parts[1]
    return None


class ExtractMarkedFrames(bpy.types.Operator):
    bl_idname = "ceb.simplifyframes"
    bl_label = "Simplify"
    bl_description = "Simplify"
    bl_options = {"REGISTER", "UNDO"}

    option: bpy.props.IntProperty(name='', default=0)  # 0=objects, 1=all bones, 2=selected bones, 3=selected fcurves

    def execute(self, context):
        markers = []
        for m in bpy.context.scene.timeline_markers:
            markers.append(m.frame)
        markers.sort()

        if not markers:
            self.report({'WARNING'}, "No timeline markers found.")
            return {'CANCELLED'}

        if self.option == 0:  # objects
            for ob in context.selected_objects:
                if not ob.animation_data or not ob.animation_data.action:
                    continue
                fcurves = get_fcurves(ob)

                # Insert keyframes at markers
                for frame in markers:
                    for fcurve in fcurves:
                        fcurve.keyframe_points.insert(frame, fcurve.evaluate(frame))

                # Remove keyframes outside markers
                for f in range(markers[0], markers[-1] + 1):
                    if f not in markers:
                        ob.keyframe_delete(data_path='rotation_quaternion', frame=f)
                        ob.keyframe_delete(data_path='location', frame=f)
                        ob.keyframe_delete(data_path='rotation_euler', frame=f)
                        ob.keyframe_delete(data_path='scale', frame=f)

                # Set interpolation to Bezier
                for fcurve in get_fcurves(ob):
                    for kp in fcurve.keyframe_points:
                        kp.interpolation = 'BEZIER'

        if self.option == 1:  # all bones
            obj = context.active_object
            if obj and obj.type == 'ARMATURE':
                fcurves = get_fcurves(obj)

                for frame in markers:
                    for fcurve in fcurves:
                        fcurve.keyframe_points.insert(frame, fcurve.evaluate(frame))

                for f in range(markers[0], markers[-1] + 1):
                    if f not in markers:
                        for bone in obj.pose.bones:
                            bone.keyframe_delete(data_path='rotation_quaternion', frame=f)
                            bone.keyframe_delete(data_path='location', frame=f)
                            bone.keyframe_delete(data_path='rotation_euler', frame=f)
                            bone.keyframe_delete(data_path='scale', frame=f)

                for fcurve in get_fcurves(obj):
                    for kp in fcurve.keyframe_points:
                        kp.interpolation = 'BEZIER'

        if self.option == 2:  # selected bones
            obj = context.active_object
            if obj and obj.type == 'ARMATURE':
                selected_bone_names = [sb.name for sb in context.selected_pose_bones]
                fcurves = get_fcurves(obj)

                # Insert keyframes at markers for selected bones
                for fcurve in fcurves:
                    bone_name = get_bone_name_from_fcurve(fcurve)
                    if bone_name in selected_bone_names:
                        for frame in markers:
                            fcurve.keyframe_points.insert(frame, fcurve.evaluate(frame))

                # Remove keyframes outside markers for selected bones
                for f in range(markers[0], markers[-1] + 1):
                    if f not in markers:
                        for bone in context.selected_pose_bones:
                            bone.keyframe_delete(data_path='rotation_quaternion', frame=f)
                            bone.keyframe_delete(data_path='location', frame=f)
                            bone.keyframe_delete(data_path='rotation_euler', frame=f)
                            bone.keyframe_delete(data_path='scale', frame=f)

                # Set interpolation to Bezier for selected bones
                for fcurve in get_fcurves(obj):
                    bone_name = get_bone_name_from_fcurve(fcurve)
                    if bone_name in selected_bone_names:
                        for kp in fcurve.keyframe_points:
                            kp.interpolation = 'BEZIER'

        if self.option == 3:  # selected fcurves from graph editor
            from .panel import get_selected_fcurves_from_anywhere
            selected_curves = get_selected_fcurves_from_anywhere()

            if not selected_curves:
                self.report({'WARNING'}, "No F-Curves selected in the Graph Editor.")
                return {'CANCELLED'}

            for fc in selected_curves:
                # Insert keyframes at markers
                for frame in markers:
                    fc.keyframe_points.insert(frame, fc.evaluate(frame))

                # Remove keyframes outside markers
                for kp in reversed(list(fc.keyframe_points)):
                    if kp.co[0] not in markers:
                        fc.keyframe_points.remove(kp)

                # Set interpolation to Bezier
                for kp in fc.keyframe_points:
                    kp.interpolation = 'BEZIER'

        return {'FINISHED'}


class ClearMarkers(bpy.types.Operator):
    bl_idname = "ceb.clear_markers"
    bl_label = "Clear Markers"
    bl_description = "Clear Markers"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        bpy.context.scene.timeline_markers.clear()
        return {'FINISHED'}


class SimplifyAndClearMarkers(bpy.types.Operator):
    bl_idname = "ceb.simplify_and_clear_markers"
    bl_label = "Simplify & Clear"
    bl_description = "Simplify and Clear Markers"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        bpy.ops.ceb.simplifyframes()
        bpy.ops.ceb.clear_markers()
        return {'FINISHED'}


class CreateMarkersFromFrames(bpy.types.Operator):
    bl_idname = "ceb.create_markers_from_frames"
    bl_label = "Create Markers From Frames"
    bl_description = "Create Markers From Frames"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        bpy.ops.ceb.clear_markers()

        obj = bpy.context.object
        if not obj or not obj.animation_data:
            self.report({'WARNING'}, "No animation data found on active object.")
            return {'CANCELLED'}

        fcurves = get_fcurves(obj)
        all_frames = []

        for fcurve in fcurves:
            for keyframe in fcurve.keyframe_points:
                all_frames.append(keyframe.co[0])

        if not all_frames:
            self.report({'WARNING'}, "No keyframes found.")
            return {'CANCELLED'}

        unique_frames = sorted(set(all_frames))
        for f in unique_frames:
            bpy.context.scene.timeline_markers.new(name="F_" + str(int(f)), frame=int(f))

        return {'FINISHED'}


class QuickSaveMarkers(bpy.types.Operator):
    bl_idname = "ceb.quick_save_markers"
    bl_label = "Quick Save Markers"
    bl_description = "Quick Save Markers"
    bl_options = {"REGISTER", "UNDO"}

    option: bpy.props.IntProperty(name='', default=1)

    def execute(self, context):
        sfsetting = context.scene.sfsetting
        markers = [[m.name, m.frame] for m in bpy.context.scene.timeline_markers]

        prop = f'str_quick_save_marker{self.option}'
        if 1 <= self.option <= 10:
            setattr(sfsetting, prop, json.dumps(markers))
        else:
            self.report({'WARNING'}, "Bank limit exceeded.")

        return {'FINISHED'}


class QuickLoadMarkers(bpy.types.Operator):
    bl_idname = "ceb.quick_load_markers"
    bl_label = "Quick Load Markers"
    bl_description = "Quick Load Markers"
    bl_options = {"REGISTER", "UNDO"}

    option: bpy.props.IntProperty(name='', default=1)

    def execute(self, context):
        sfsetting = context.scene.sfsetting
        prop = f'str_quick_save_marker{self.option}'

        if not (1 <= self.option <= 10):
            self.report({'WARNING'}, "No more banks.")
            return {'CANCELLED'}

        data = getattr(sfsetting, prop, '')
        if not data:
            self.report({'WARNING'}, f"Bank {self.option} is empty.")
            return {'CANCELLED'}

        quick_load = json.loads(data)
        bpy.context.scene.timeline_markers.clear()
        for ql in quick_load:
            context.scene.timeline_markers.new(ql[0], frame=ql[1])

        return {'FINISHED'}


class QuickSaveMarkersClear(bpy.types.Operator):
    bl_idname = "ceb.quick_save_markers_clear"
    bl_label = "Clear Quick Save Markers"
    bl_description = "Clear Quick Save Markers"
    bl_options = {"REGISTER", "UNDO"}

    option: bpy.props.IntProperty(name='', default=0)  # 0 = clear all

    def execute(self, context):
        sfsetting = context.scene.sfsetting

        if self.option == 0:
            for i in range(1, 11):
                setattr(sfsetting, f'str_quick_save_marker{i}', '')
        elif 1 <= self.option <= 10:
            setattr(sfsetting, f'str_quick_save_marker{self.option}', '')
        else:
            self.report({'WARNING'}, "No more banks.")

        return {'FINISHED'}