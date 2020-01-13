from rest_framework import renderers


class BinaryFileRenderer(renderers.BaseRenderer):
    """
    Renderer which returns a binary file.
    """
    media_type = "application/data"
    charset = None

    def render(self, data, accepted_media_type=None, renderer_context=None):
        # Data must be binary
        if not isinstance(data, bytes):
            # Assume it's an error, and return the JSON rendering
            return renderers.JSONRenderer().render(data, accepted_media_type, renderer_context)

        return data
