import json

from rest_framework.renderers import JSONRenderer


class ProfileJSONRenderer(JSONRenderer):
    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context.get("response").status_code
        errors = data.get("errors", None)

        is_invalid = errors is not None

        if is_invalid:
            return super().render(data)

        return json.dumps({"status_code": status_code, "profile": data})


class ProfilesJSONRenderer(JSONRenderer):
    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context.get("response").status_code
        errors = data.get("errors", None)

        is_invalid = errors is not None

        if is_invalid:
            return super().render(data)

        return json.dumps({"status_code": status_code, "profiles": data})
