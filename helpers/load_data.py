import json
import os
import pandas as pd
from typing import Dict, Any, List
from .logger import logger
from configs.constants import FILETYPE

FILE_TYPE = list(map(lambda c: c.value, FILETYPE))

def load_json_file(file_path: str = "", *args, **kwargs) -> Dict:
    with open(file_path, *args, **kwargs) as f:
        return json.load(f)

def load_text_file(file_path: str = "", *args, **kwargs) -> str:
    with open(file_path, *args, **kwargs) as f:
        return f.read()

def load_csv(file_path, *args, **kwargs) -> List:
        return pd.read_csv(file_path, *args, **kwargs).to_dict(orient="records")

def load_excel(file_path, *args, **kwargs) -> List:
        return pd.read_excel(file_path, engine="calamine", *args, **kwargs).to_dict(orient="records")

def load_data(
    file_path: str = "",
    data_type: FILE_TYPE = "excel",
    *args,
    **kwargs
    ) -> Any:
    load_data_funct_mapping: Dict = {
        "json": load_json_file,
        "text": load_text_file,
        "csv": load_csv,
        "excel": load_excel
    }
    if not os.path.exists(file_path):
        raise Exception(f"File not found: '{file_path}'.")

    logger.info(f"Loading data from '{file_path}'.")
    data: Any = load_data_funct_mapping[data_type](file_path, *args, **kwargs)
    if not data:
        logger.error(f"Error loading data from '{file_path}'.")
        return

    logger.success(f"Complete loading data from '{file_path}'.")
    return data
