#pylint:disable=W0718
#pylint:disable=W0613
#pylint:disable=all
from io import BytesIO
from fastapi import APIRouter
from fastapi import Request
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.main.adapters.file_adapter import file_adapter
from src.errors.error_handle import error_handler

from src.main.composers.create_type_composer import create_type_composer
from src.main.composers.delete_type_composer import delete_type_composer
from src.main.composers.find_type_by_exact_name_composer import find_type_by_exact_name_composer
from src.main.composers.update_type_composer import update_type_composer
from src.main.composers.find_all_types_composer import find_all_types_composer