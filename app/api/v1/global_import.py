from starlette.responses import JSONResponse

class FastApiResponse:
    successful = "Successful"
    failure = lambda msg: JSONResponse(status_code=500, content={"message": str(msg)})
