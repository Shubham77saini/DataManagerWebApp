import os
import json


def save_multiple_files_metadata(validated_data):
    selected_data = {}
    for index, each_dict in enumerate(validated_data["multiple_files"]):
        os.makedirs("temp", exist_ok=True)
        subdirectory = f"extracted_multiple_meta_data_json__from_a_uploaded_json"
        os.makedirs(os.path.join("temp", subdirectory), exist_ok=True)
        file_name = f"meta_data_{index + 1}.json"

        selected_data = {
            "date": each_dict["date"],
            "cameraModel": each_dict["cameraModel"],
            "cameraName": each_dict["cameraName"],
            "viewName": each_dict["viewName"],
            "tags": each_dict["tags"],
            "description": each_dict["description"],
            "customer": each_dict["customer"],
            "site": each_dict["site"],
            "fps": each_dict["fps"],
            "recordingResolution": each_dict["resolution"],
            "exposure": each_dict["exposure"],
            "reviewForViewChange": each_dict["reviewForViewChange"],
            "padding": each_dict["padding"],
            "recordedUsing": each_dict["recordedUsing"],
            "gain": each_dict["gain"],
        }

        with open(os.path.join("temp", subdirectory, file_name), "w") as file:
            json.dump(selected_data, file, indent=2)
