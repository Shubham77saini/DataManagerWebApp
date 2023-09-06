import re


def validate_resolution_format(cls, val):
    pattern = re.compile(r"^\d{1,20}\s*x\s*\d{1,20}$")
    if not re.match(pattern, val["resolution"]):
        raise ValueError(
            "Invalid resolution format. Please use the 'width x height' format (e.g., 1920x1080)."
        )
    if val["padding"]:
        if not re.match(pattern, val["padding"]["dimension"]):
            raise ValueError(
                "Invalid padding format. Please check dimension value use the 'width x height' format (e.g., 1920x1080)."
            )
