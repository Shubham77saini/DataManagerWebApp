import os
import streamlit as st
import sys

sys.dont_write_bytecode = True

from src.add_logo_and_favicon_remove_hamburger_icon import (
    hide_hamburger,
    add_logo,
    replace_favicon,
)

replace_favicon()  # This must be the first Streamlit command used on an app page, and must only be set once per page.

import json
from pydantic.typing import List
from pydantic import BaseModel


from botocore.exceptions import ClientError

from dotenv import load_dotenv

load_dotenv()

import os
import boto3


from src.constants import insert_data_in_db
from src.multiple_file_validation import Multiple_File_Validation
from src.save_multiple_files import save_multiple_files_metadata
from src.convert_timestamp_to_date_only import converts_timestamp_to_date_only
from src.json_file_uploader import json_uploader
from src.single_file_path_generator import form_for_single_path


from src.database_handler import create_database_connection, create_table, insert_data
from streamlit_modal import Modal
import psycopg

# ===================================================================================================================

hide_hamburger()  # Hide the Hamburger and Logo of streamlit form the web_app.
add_logo()


# Detailed_multiple_file_check Inheritr the BaseModel
class Detailed_multiple_file_check(BaseModel):
    multiple_files: List[Multiple_File_Validation]
    """Multiple_File_Validation is class which contain a function (validate_all) that is used to validate
    the json file"""


JSON_FILE = (
    json_uploader()
)  # json_uploader is a function that is used for uploding the json file.

BUCKET = os.getenv("BUCKET")  # Bucket name will be fetching from here

CONN = (
    create_database_connection()
)  # This function is used for createing the database connection

create_table(CONN)  # This function is used for creating the tabel


if JSON_FILE:
    try:
        data = json.loads(JSON_FILE)

        validated_data = Detailed_multiple_file_check(**data).dict()

        save_multiple_files_metadata(validated_data)

        duplicate_data_count = 0

        def process_data_entry(conn, length, duplicate_data_count, insert_data_in_db):
            for each_dict in validated_data[
                "multiple_files"
            ]:  # Here I am iterarting on each dict after validating the json.
                date_only = converts_timestamp_to_date_only(
                    each_dict
                )  # This function is used for Extracting  the date from timestamp.That is used in s3 upload_cmd.

                download_s3_cmd = ""
                uploadPath = ""
                uploadPath_for_key = []

                for each_path in each_dict[
                    "files"
                ]:  # Here I create the s3 Upload command and Upload Path
                    aws_s3_path = f"{each_dict['projectName']}/{each_dict['typeOfData']}/{date_only}/{each_dict['dataUploadFormat']}/{each_dict['systemName']}/"
                    path = f"s3://{BUCKET}/source/{aws_s3_path}"
                    s3_upload_path = f"{each_path} {path}"
                    s3_path = f"aws s3 cp {s3_upload_path}"
                    uploadPath += f"\n{s3_upload_path}\n"  # Save in database
                    download_s3_cmd += f"\n{s3_path} \n"  # Download
                    uploadPath_for_key.append(
                        s3_upload_path
                    )  # This i upload path is use for making object_key.

                # Extracting the values from each_dict for save in database
                timestamp = each_dict["date"]
                cameraModel = each_dict["cameraModel"]
                cameraName = each_dict["cameraName"]
                viewName = each_dict["viewName"]
                tags = json.dumps(each_dict["tags"])
                description = each_dict["description"]
                customer = each_dict["customer"]
                site = each_dict["site"]
                fps = each_dict["fps"]
                recordingResolution = each_dict["resolution"]
                exposure = each_dict["exposure"]
                reviewForViewChange = each_dict["reviewForViewChange"]
                padding = json.dumps(each_dict["padding"])
                recordedUsing = each_dict["recordedUsing"]

                # Values use when we perform insert operation in data base.
                values = (
                    timestamp,
                    cameraModel,
                    cameraName,
                    viewName,
                    tags,
                    description,
                    customer,
                    site,
                    fps,
                    recordingResolution,
                    exposure,
                    reviewForViewChange,
                    padding,
                    recordedUsing,
                    uploadPath,
                )

                try:
                    insert_data(conn, values)  # Inserting the data in database table

                    insert_data_in_db += download_s3_cmd
                    # On each sucessful insertion insert_data_in_db will update and at the last it will be pass as paramter to download functionality

                except psycopg.IntegrityError as error:
                    # check Duplicate key value error.

                    if "duplicate key value violates unique constraint" in str(error):
                        # aws check
                        for each_uploadPath in uploadPath_for_key:
                            split_path = each_uploadPath.split()

                            path = split_path[1]

                            file_name = split_path[0].split("/")[-1]

                            aws_object_key = f"{path}{file_name}"

                            split_path_bucket = aws_object_key.split(
                                f"{BUCKET}/"
                            )  # source/bcheck/rawdata/2023-03-29/zip/koireader-rtx3090-us-0006/

                            bucket_name = f"{BUCKET}"

                            split_path_in_two_part = aws_object_key.split("s3:/")

                            split_the_path_file_name = split_path_in_two_part[0].split(
                                "/"
                            )

                            object_key = (
                                split_path_bucket[1] + split_the_path_file_name[-1]
                            )  # source/bcheck/rawdata/2023-03-29/zip/koireader-rtx3090-us-0006/file_name

                            # Create an S3 client
                            s3_client = boto3.client("s3")

                            try:
                                response = s3_client.head_object(
                                    Bucket=bucket_name, Key=object_key
                                )

                                print("Found S3 object.")

                            except ClientError as key_error:
                                if key_error.response["Error"]["Code"] == "404":
                                    print("No object found.")

                                    insert_data_in_db += (
                                        f"\n aws s3 cp {each_uploadPath} \n"
                                    )
                                    duplicate_data_count -= 1

                                else:
                                    print("An error occurred:", key_error)

                        duplicate_data_count += 1
                        # Here I increase the duplicate_data_count by 1 if (duplicate key value violates unique constraint)"""

                        if (
                            "duplicate key value violates unique constraint"
                            in str(error)
                            and duplicate_data_count == length
                        ):  # Here I put the check if duplicate_data_count == length (length = how many dict have in json) means If all the dict of json not present in db then print Duplicate Data Entry Already Exits in the Database.
                            modal = Modal(" ", key=5)

                            with modal.container():
                                st.error(
                                    "Duplicate Data Entry Already Exits in the Database."
                                )

                    else:
                        st.write(f"Error: {error}")
                    conn.rollback()
                except Exception as error:
                    st.write(f"Error: {error}")
                    conn.rollback()
                else:
                    conn.commit()

            modal = Modal(" ", key=1)

            if (
                duplicate_data_count != length
            ):  # this check I use to solve ovelapping problem if data is not Duplicate the Download Button will be popup.
                with modal.container():
                    st.download_button(
                        "Download",
                        insert_data_in_db,
                        file_name="Your_upload_commands.sh",
                    )

        process_data_entry(
            CONN,
            len(validated_data["multiple_files"]),
            duplicate_data_count,
            insert_data_in_db,
        )

    except (
        Exception
    ) as e:  # If any Error occur while validating the json file then this will run for showing the error in modal.
        error_message = str(e)
        modal = Modal(" ", key=1)
        with modal.container():
            st.code(error_message)
            st.error("PLEASE UPLOAD A VALID JSON.")

st.markdown(
    "<p style='text-align: center; font-size: 40px;'>--------------------------OR--------------------------</p>",
    unsafe_allow_html=True,
)


# --------------------------- From Here Single Path Generator Code Started -----------------------------------------

form_for_single_path()
