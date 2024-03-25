from pydantic import BaseModel
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK


class Status(BaseModel):
    status: str
    status_code: int = HTTP_200_OK
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "ok"
                },
                {
                    "status": "Something wrong with database"
                }
            ]
        }
    }

    def get_response(self) -> JSONResponse:
        return JSONResponse(
            status_code=self.status_code,
            content=self.model_dump(exclude={'status_code'})
        )
