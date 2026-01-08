
import pytest
from helpers.logger import logger

if __name__ == "__main__":
    logger.info(f"{' Start testing ':=^50}\n")
    test_case_path: str = "testcases"
    mark: str = '-m role'
    pytest.main([test_case_path, mark])
    logger.success(f"{' End testing ':=^50}\n")