import bpy
import bpy.types
from bpy.props import (PointerProperty)

# import json
from .simplify_frames import *
from .panel import *

bl_info = {
    "name" : "CEB Simply Frames",
    "author" : "Carlos Barreto",
    "description" : "",
    "blender" : (5, 0, 0),
    "version" : (2, 2, 0),
    "location" : "UI > SidePanel",
    "warning" : "",
    "category" : "General"
}
# 2.3 - update pra rodar no blender 5x

classes = (
    SimplifyFrames,
    ExtractMarkedFrames,
    ClearMarkers,
    SimplifyAndClearMarkers,
    CreateMarkersFromFrames,
    QuickSaveMarkers,
    QuickLoadMarkers,
    QuickSaveMarkersClear,
    SFSettings,
)

def register():
    
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.sfsetting = PointerProperty(type=SFSettings)

def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls) 

if __name__ == "__main__":
    register()