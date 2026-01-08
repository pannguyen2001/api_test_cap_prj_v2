from requests import Response

def validate_response(funct_name: str = "", res: Response = None):
    if res.status_code >= 400:
        raise Exception(f"[{funct_name}] Request error: Status:{res.status_code}. Text:{res.text}")

    res = res.json()
    return res