project_names = ["s2u-connect-inbound", "bcheck", "s2u-connect-outbound"]

types_of_data = [
    "rawdata",
    "textcrops",
    "charactercrops",
    "logos",
    "barcodecrops",
    "barcodetextregioncrops",
    "qrcodecrops",
]

name_of_customer = ["PepsiCo"]

data_upload_formats = ["video", "zip", "image"]

name_of_system = ["koireader-rtx3090-us-0006"]

recorded__using = [
    "gstreamer",
    "vidgear",
    "cv2_plain",
    "ffmpegcv",
    "ffmpeg",
    "v4l2",
    "cv2_with_gstreamer",
    "cv2_with_v4l2",
    "cv2_with_ffmpeg",
    "ximea_sdk",
    "teledyne_sdk",
]

padding_positions = [
    "left",
    "right",
    "top",
    "bottom",
    "top_left",
    "top_right",
    "bottom_left",
    "bottom_right",
]

data_review = ["yes", "no"]

insert_data_in_db = """#!/bin/bash
                            # Set your AWS credentials
                            AWS_ACCESS_KEY_ID=""
                            AWS_SECRET_ACCESS_KEY=""

                            # Configure AWS CLI with the provided credentials
                            aws configure set aws_access_key_id "$AWS_ACCESS_KEY_ID"
                            aws configure set aws_secret_access_key "$AWS_SECRET_ACCESS_KEY"
                            """
