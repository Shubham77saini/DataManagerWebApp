import psycopg
from dotenv import load_dotenv

load_dotenv()
import os


def create_database_connection():
    DBNAME = os.getenv("DBNAME")
    USER = os.getenv("USER")
    PASSWORD = os.getenv("PASSWORD")
    connection_credentials = f"dbname='{DBNAME}' user='{USER}' password='{PASSWORD}'"
    conn = psycopg.connect(connection_credentials)
    return conn


def create_table(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS labelstudio.dataset_metadata
            (TIMESTAMP timestamp with time zone NOT NULL,
            cameraModel VARCHAR (25)  NOT NULL ,
            cameraName VARCHAR (25)  NOT NULL,
            viewName VARCHAR (50)  NOT NULL,
            tags JSONB,
            description VARCHAR (300),
            customer VARCHAR (25),
            site VARCHAR (25),
            fps INT,
            recordingResolution VARCHAR (20) ,
            exposure VARCHAR (20) ,
            reviewForViewChange boolean NOT NULL,
            padding JSONB,
            recordedUsing VARCHAR (25) NOT NULL,
            uploadPath VARCHAR (800)  NOT NULL,
            CONSTRAINT TIMESTAMP_cameraModel_cameraName_site_recordingResolution PRIMARY KEY (TIMESTAMP, cameraModel, cameraName, site,recordingResolution));
        """
        )


def insert_data(conn, values):
    with conn.cursor() as cur:
        insert_query = "INSERT INTO labelstudio.dataset_metadata (timestamp, cameraModel, cameraName, viewName, tags, description, customer, site, fps, recordingResolution, exposure, reviewForViewChange, padding, recordedUsing, uploadPath) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(insert_query, values)
        conn.commit()
