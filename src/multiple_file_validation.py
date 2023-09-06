from pydantic.typing import Dict, List, Union, Optional
from pydantic import BaseModel, StrictStr, StrictInt, root_validator, StrictBool
from src.date_validate import validate_date_within_past_year
from src.validate_resolution import validate_resolution_format
from src.fps_check import fps_validate


class Multiple_File_Validation(BaseModel):
    date: StrictStr
    # Here I am checking the datatupe of the each value of json
    cameraModel: Optional[StrictStr] = ""
    viewName: StrictStr
    tags: Optional[
        Dict[StrictStr, StrictStr]
    ] = {}  # if tags not given in json file set {} empty dict.
    padding: Optional[Dict[StrictStr, StrictStr]] = {}
    description: Optional[StrictStr] = ""
    customer: StrictStr
    site: StrictStr
    fps: StrictInt
    resolution: StrictStr
    exposure: StrictStr
    reviewForViewChange: StrictBool
    typeOfData: StrictStr
    projectName: StrictStr
    systemName: StrictStr
    dataUploadFormat: StrictStr
    cameraName: StrictStr
    files: Union[StrictStr, List[StrictStr]]
    gain: Optional[StrictStr] = ""
    recordedUsing: StrictStr

    @root_validator(allow_reuse=True)
    def validate_all(cls, val):
        validate_date_within_past_year(cls, val)
        validate_resolution_format(cls, val)
        fps_validate(cls, val)

        return val
