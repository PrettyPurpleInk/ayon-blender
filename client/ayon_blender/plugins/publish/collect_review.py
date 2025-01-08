import bpy
import pyblish.api
from ayon_blender.api import plugin


class CollectReview(plugin.BlenderInstancePlugin):
    """Collect Review data

    """

    order = pyblish.api.CollectorOrder + 0.3
    label = "Collect Review Data"
    families = ["review"]

    def process(self, instance):

        self.log.debug(f"instance: {instance}")

        datablock = instance.data["transientData"]["instance_node"]

        # get cameras
        cameras = [
            obj
            for obj in datablock.all_objects
            if isinstance(obj, bpy.types.Object) and obj.type == "CAMERA"
        ]

        assert len(cameras) == 1, (
            f"Not a single camera found in extraction: {cameras}"
        )
        camera = cameras[0].name
        self.log.debug(f"camera: {camera}")

        focal_length = cameras[0].data.lens

        shading_type = instance.data["creator_attributes"]["shadingType"]

        # get isolate objects list
        # All types of objects: 'MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'ARMATURE', 'LATTICE', 'EMPTY', 'GPENCIL', 'CAMERA', 'LIGHT', 'SPEAKER', 'LIGHT_PROBE'
        types_exclude = {"EMPTY", "CAMERA", "ARMATURE", "LIGHT", "LIGHT_PROBE", "SPEAKER"}
        isolate_objects = [
            obj
            for obj in instance
            if isinstance(obj, bpy.types.Object) and not obj.type in types_exclude
        ]

        # Store focal length in `burninDataMembers`
        burninData = instance.data.setdefault("burninDataMembers", {})
        burninData["focalLength"] = focal_length

        instance.data.update({
            "review_camera": camera,
            "fps": instance.context.data["fps"],
            "shadingType": shading_type,
            "isolate": isolate_objects,
        })

        self.log.debug(f"instance data: {instance.data}")

        # TODO : Collect audio
        # audio_tracks = []
        # instance.data["audio"] = [
        #     {
        #         "offset": track.offset.get(),
        #         "filename": track.filename.get(),
        #     }
        #     for track in audio_tracks
        # ]
