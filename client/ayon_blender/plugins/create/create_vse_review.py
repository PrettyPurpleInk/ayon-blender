"""Create review."""

from ayon_blender.api import plugin, lib


class CreateVSEReview(plugin.BlenderCreator):
    """VSE timeline."""

    identifier = "io.openpype.creators.blender.vse-review"
    label = "VSE Review"
    product_type = "vse-review"
    icon = "video-camera"

    def create(
        self, product_name: str, instance_data: dict, pre_create_data: dict
    ):
        # Run parent create method
        collection = super().create(
            product_name, instance_data, pre_create_data
        )

        if pre_create_data.get("use_selection"):
            selected = lib.get_selection()
            for obj in selected:
                collection.objects.link(obj)

        return collection

    def get_instance_attr_defs(self):
        defs = lib.collect_vse_defs(self.create_context)

        return defs
