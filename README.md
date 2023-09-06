# Streamlit Data Uploader Details Web App
## This is streamlit web app that can take the details from the users. Finally give the Path for uploading the data on aws S3 bucket and meta_data.json file.

### Requirements :
#### Direct python3 installation (cmd)
1. Check for python installation, print the current python version
    - python -–version
2. Install these modules
    - pip install streamlit
    - pip install pydantic
    - pip install python-dotenv
    - pip install nanoid
    - pip install psycopg
    - pip install streamlit-modal
    
3. Run streamlit :- 
```python
streamlit run main.py
```
Download python3: [python3] (https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe "python3")

4. Folders :
      - docs
           - docs folder contains 3 meta_data_sample files which can be use for testing purpose.
            - meta_data_sample_1.json - Incorrect file.
            - meta_data_sample_2.json - Incorrect file.
            - meta_data_sample_3.json - Correct file.

5. - Create .env file in your root directory and write copy this - bucket = "here_you_add_your_bucket_name", DBNAME = "your_database_name", USER = "user_name", PASSWORD = "your_password"


6. - src folder has (constants.py) that contains lists options (e.g., recorded_using = ["xyz"]).