from src.presentation.http_types.http_response import HttpResponse

async def insert_access_token(http_response:HttpResponse, token:str) -> HttpResponse:
    if token:
        http_response.body["access_token"] = token
        return http_response
    return http_response