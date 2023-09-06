# This is used for check the fps of multiple dict
def fps_validate(cls, val):
    if val["fps"] < 9 or val["fps"] > 60:
        raise ValueError(
            "FPS should be between 9 and 60 (inclusive). Minimum FPS should be 9."
        )
