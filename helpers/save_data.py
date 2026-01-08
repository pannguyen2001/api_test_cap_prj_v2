import json
import os
import pandas as pd
from typing import Dict, Any, Optional
from configs.constants import FILETYPE
from .logger import logger
from .logger_wrapper import logger_wrapper

FILE_TYPE = list(map(lambda c: c.value, FILETYPE))

def save_to_json_file(file_path: str = "", data: Dict = None) -> Optional[bool]:
    with open(file_path, "w") as f:
        json.dump(data, f, separators=(",", ":"))
    return True

def save_to_text_file(file_path: str = "", data: str = "") -> Optional[bool]:
    with open(file_path, "w") as f:
        f.write(data)
    return True

def save_to_csv_file(file_path: str = "", data: Dict | pd.DataFrame | pd.Series = None, *args, **kwargs) -> Optional[bool]:
    data.to_csv(file_path, *args, **kwargs)
    return True

def save_to_excel_file(file_path: str = "", data: Dict | pd.DataFrame | pd.Series = None, *args, **kwargs) -> Optional[bool]:
    data.to_excel(file_path, *args, **kwargs)
    return True

@logger_wrapper
def save_data(
    file_path: str = "",
    data: Any =  None,
    file_type: str = "csv",
    *args,
    **kwargs
    ) -> None:
    save_data_to_file_funct_mapping: Dict = {
        "json": save_to_json_file,
        "text": save_to_text_file,
        "csv": save_to_csv_file,
        "excel": save_to_excel_file
    }
    if not os.path.exists(file_path):
        raise Exception(f"File not found: {file_path}")

    logger.info(f"Save data to file: '{file_path}.'")
    save_data_result: Any = save_data_to_file_funct_mapping[file_type](file_path)
    if not save_data_result:
        logger.error(f"Error saving data to file: '{file_path}'.")
        return

    logger.success(f"Save data successfully to file: '{file_path}'.")
