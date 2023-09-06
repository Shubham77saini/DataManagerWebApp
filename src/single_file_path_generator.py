import streamlit as st
from src.constants import (
    types_of_data,
    project_names,
    name_of_customer,
    data_upload_formats,
    name_of_system,
    recorded__using,
    padding_positions,
    data_review,
)
import datetime as date
import re
from nanoid import generate
from streamlit_modal import Modal
import json
import os
from dotenv import load_dotenv

load_dotenv()


BUCKET = os.getenv("BUCKET")


def form_for_single_path():
    def projectName():
        projectName = st.selectbox("Project Name *", options=project_names)

        return projectName

    project_name = projectName()

    def typeOfData():
        selectTypeOfData = st.selectbox(
            "Type of Data *",
            options=types_of_data + ["Another option..."],
        )

        if selectTypeOfData == "Another option...":
            otherOption = st.text_input("Type of data... *")

        if selectTypeOfData != "Another option...":
            pass
        else:
            selectTypeOfData = otherOption
        return selectTypeOfData

    selectTypeOfData = typeOfData()

    def currentDate():
        current_date = date.date.today()
        one_year_ago = current_date - date.timedelta(days=365)
        userTimestampInput = st.text_input(
            "Timestamp YYYY-MM-DD hh:"
            + "\u200Bmm"
            + ":"
            + "\u200Bss (e.g., 2023-05-16 10:12:03)*"
        )
        try:
            user_date = date.datetime.strptime(
                userTimestampInput, "%Y-%m-%d %H:%M:%S"
            ).date()

            if user_date <= current_date and user_date >= one_year_ago:
                pass
            else:
                st.error(
                    "Invalid Timestamp.Please check the date should be within the past year from current date."
                )

        except ValueError:
            if userTimestampInput != "":
                st.error(
                    "Please enter the Timestamp in the format YYYY-MM-DD hh:"
                    + "\u200Bmm"
                    + ":"
                    + "\u200Bss (e.g., 2023-05-16 10:12:03)."
                )

        return userTimestampInput

    userTimestampInput = currentDate()

    def customerName():
        customerName = st.selectbox("Customer Name *", name_of_customer)

        return customerName

    customer_name = customerName()

    def dataUploadFormat():
        dataUploadFormat = st.selectbox(
            "Data Upload Format *", options=data_upload_formats
        )
        return dataUploadFormat

    data_upload_format = dataUploadFormat()

    def systemName():
        systemName = st.selectbox("Upload System Name *", options=name_of_system)
        return systemName

    system_name = systemName()

    def siteName():
        siteName = st.text_input("Site Name *")
        return siteName

    site_name = siteName()

    def fps():
        fps = st.number_input("fps *", min_value=9)
        if fps < 9 or fps > 60:
            st.error(
                "fps should be between 9 and 60 (inclusive). Minimum fps should be 9."
            )
        return fps

    fps_ = fps()

    def validateDimension(dimension):
        pattern = re.compile(r"^\d{1,20}\s*x\s*\d{1,20}$")
        if not re.match(pattern, dimension):
            st.error(
                "Invalid dimension format. Please use the 'width x height' format (e.g., 2464x2056)."
            )
            return False
        return True

    def resolutionInput():
        def validate_resolution(resolution):
            pattern = re.compile(r"^\d{1,20}\s*x\s*\d{1,20}$")
            if not re.match(pattern, resolution):
                st.error(
                    "Invalid resolution format. Please use the 'width x height' format (e.g., 1920x1080)."
                )
                return False
            return True

        resolutionInput = st.text_input("Resolution (width x height) *")

        if resolutionInput:
            if validate_resolution(resolutionInput):
                pass
            else:
                st.warning("Invalid resolution. Please enter a valid resolution.")

        return resolutionInput

    resolution_input = resolutionInput()

    # def validateDimension(dimension):
    #     pattern = re.compile(r"^\d{1,20}\s*x\s*\d{1,20}$")
    #     if not re.match(pattern, dimension):
    #         st.error(
    #             f"Invalid format. Please use the 'width x height' format (e.g., 2464x2056)----."
    #         )
    #         return False
    #     return True

    # def resolutionInput():
    #     resolutionInput = st.text_input("Resolution (width x height) *")

    #     if resolutionInput:
    #         if not validateDimension(resolutionInput):
    #             pass

    #     return resolutionInput

    # resolution_input = resolutionInput()

    def description():
        description = st.text_area("Description", height=20, max_chars=250)
        return description

    description_ = description()

    def reviewData():
        selection = st.selectbox(
            "Review Data for Change in View *", options=data_review
        )
        if selection == "no":
            boolean_val = False
        else:
            boolean_val = True
        return boolean_val

    reviewForChange = reviewData()

    def cameraModel():
        cameraModel = st.text_input("Camera Model")
        return cameraModel

    camera_model = cameraModel()

    def viewName():
        viewName = st.text_input("View Name *")
        return viewName

    view_name = viewName()

    def exposure():
        exposure = st.text_input("exposure *")
        return exposure

    exposure_ = exposure()

    def gain():
        gain = st.text_input("Gain")
        return gain

    gain_ = gain()

    def cameraName():
        cameraName = st.text_input("Camera Name *")
        return cameraName

    camera_name = cameraName()

    def recordedUsing():
        recordedUsing = st.selectbox("Recorded Using *", options=recorded__using)
        return recordedUsing

    recorded_using = recordedUsing()

    def getPaddingInput():
        st.subheader("Padding")

        dimension_input = st.text_input("Dimension (width x height)")
        position_input = st.selectbox("Position", options=padding_positions)

        if dimension_input and validateDimension(dimension_input):
            padding = {"dimension": dimension_input, "position": position_input}
            return padding
        else:
            return {}

    padding = getPaddingInput()

    def tags():
        final_dict = {}
        random_key = generate(size=10)

        st.subheader("Tags")

        col1, col2 = st.columns(2)

        tags = st.session_state.get("tags", random_key)

        for i, tag in enumerate(tags):
            with col1:
                key = st.text_input(f"Key", key=f"key_{i}")
            with col2:
                value = st.text_input(f"Value", key=f"value_{i}")

            if key and value:
                final_dict[key] = value
            else:
                break

        if st.button("Add Tag"):
            addTag()

        return final_dict

    def addTag():
        tags = st.session_state.get("tags")
        if tags:
            tags.append("")
        else:
            tags = [""]
        st.session_state["tags"] = tags

    tagsDict = tags()

    def validateMandatoryFields(
        project_name,
        userTimestampInput,
        data_upload_format,
        site_name,
        system_name,
        fps_,
        resolution_input,
        view_name,
        reviewForChange,
        exposure_,
        camera_name,
        recorded_using,
    ):
        if not (
            project_name
            and userTimestampInput
            and data_upload_format
            and site_name
            and system_name
            and fps_
            and resolution_input
            and view_name
            and reviewForChange
            and exposure_
            and camera_name
            and recorded_using
        ):
            st.error("Please fill in all the mandatory fields. *")
            return False

        # Check if date is valid
        try:
            user_date = date.datetime.strptime(
                userTimestampInput, "%Y-%m-%d %H:%M:%S"
            ).date()
            current_date = date.date.today()
            one_year_ago = current_date - date.timedelta(days=365)
            if user_date > current_date or user_date <= one_year_ago:
                st.error(
                    "Invalid Timestamp. Please enter a date within the past year from the current date."
                )
                return False

        except ValueError:
            st.error(
                "Please enter the Timestamp in the format YYYY-MM-DD hh:"
                + "\u200Bmm"
                + ":"
                + "\u200Bss (e.g., 2023-05-16 10:12:03)."
            )
            return False

        if fps_ < 9 or fps_ > 60:
            st.error(
                "fps should be between 9 and 60 (inclusive). Minimum fps should be 9."
            )
            return False

        # Check if resolution is valid
        pattern = re.compile(r"^\d{1,20}\s*x\s*\d{1,20}$")
        if not re.match(pattern, resolution_input):
            st.error(
                "Invalid resolution format. Please use the 'width x height' format (e.g., 1920x1080)."
            )
            return False

        return True

    st.write("--------------------------------------------------------------")

    submit_button = st.button("Submit")

    if submit_button:
        if validateMandatoryFields(
            project_name,
            userTimestampInput,
            data_upload_format,
            site_name,
            system_name,
            fps_,
            resolution_input,
            view_name,
            reviewForChange,
            exposure_,
            camera_name,
            recorded_using,
        ):

            def meta_data():
                data = {
                    "date": userTimestampInput,
                    "cameraModel": camera_model,
                    "cameraName": camera_name,
                    "viewName": view_name,
                    "tags": tagsDict,
                    "description": description_,
                    "customer": customer_name,
                    "site": site_name,
                    "fps": fps_,
                    "recordingResolution": resolution_input,
                    "exposure": exposure_,
                    "reviewForViewChange": reviewForChange,
                    "padding": padding,
                    "recordedUsing": recorded_using,
                    "gain": gain_,
                }
                user_date = date.datetime.strptime(
                    userTimestampInput, "%Y-%m-%d %H:%M:%S"
                ).date()
                s3_path = f"{project_name}/{selectTypeOfData}/{user_date}/{data_upload_format}/{system_name}/"

                path = f"s3://{BUCKET}/source/{s3_path}"

                s3_upload_path = f"aws s3 cp <source> {path}"
                modal = Modal(" ", key=10)
                with modal.container():
                    st.write(f"Your s3 path is :- {path}")
                    st.write(
                        "Path for uploading the data on S3 :- ", f"{s3_upload_path}"
                    )

                json_data = json.dumps(data, indent=2)
                return json_data

            os.makedirs("temp/json_according_to_user_provided_input", exist_ok=True)

            meta_data = meta_data()
            with open(
                "temp/json_according_to_user_provided_input/meta_data.json", "w"
            ) as file:
                file.write(meta_data)
