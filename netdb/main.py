from typing import Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.encoders import jsonable_encoder

import util.initialize as init
import util.api_resources as resources
from config.defaults import READ_ONLY
from models.root import RootContainer, COLUMN_TYPES
from odm.column_odm import ColumnODM
from util.exception import NetDBException

from util.api_resources import (
    NetDBReturn,
    generate_filter,
    PrettyJSONResponse,
    ERR_READONLY,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not READ_ONLY:
        init.initialize()
    yield


app = FastAPI(
    title="NetDB API Version 2",
    description=resources.DESCRIPTION,
    openapi_tags=resources.tags,
    lifespan=lifespan,
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    response = jsonable_encoder(
        NetDBReturn(
            result=False,
            out={'detail': errors},
            comment='NetDB says: FastAPI returned a validation error.',
        )
    )

    return JSONResponse(
        content=response, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    response = jsonable_encoder(
        NetDBReturn(
            result=False,
            error=True,
            comment='NetDB resource not found.',
        ),
        exclude_none=True,
    )

    return JSONResponse(content=response, status_code=status.HTTP_404_NOT_FOUND)


@app.exception_handler(NetDBException)
async def netdb__exception_handler(request: Request, exc: NetDBException):
    response = jsonable_encoder(
        NetDBReturn(
            result=False,
            error=True,
            comment=exc.message,
        ),
        exclude_none=True,
    )

    return JSONResponse(content=response, status_code=exc.code)


@app.get("/")
def read_root():
    return {
        'name': 'NetDB API version 2',
        'status': 'up',
    }


@app.get(
    '/column',
    tags=['list_columns'],
    response_class=PrettyJSONResponse,
)
def list_columns():
    return NetDBReturn(
        out=COLUMN_TYPES,
        comment='Available NetDB columns.',
    )


@app.post('/validate', tags=['validate'])
def validate_column(
    data: RootContainer,
):
    ColumnODM(data).validate()

    return NetDBReturn(
        comment='Validation successful.',
    )


@app.post('/column', tags=['column'])
def reload_column(
    data: RootContainer,
    response: Response,
):
    if READ_ONLY:
        response.status_code = status.HTTP_403_NOT_ALLOWED
        return ERR_READONLY

    if out := ColumnODM(data).reload():
        # Successful return
        return NetDBReturn(out=out, comment='Column reload successful.')

    # Empty result. Nothing was reloaded.
    response.status_code = status.HTTP_404_NOT_FOUND
    return NetDBReturn(result=False, comment='Nothing reloaded.')


@app.get(
    '/column/{column}',
    tags=['column'],
    response_class=PrettyJSONResponse,
)
def get_column(
    column: str,
    datasource: Optional[str] = None,
    set_id: Optional[str] = None,
    device: Optional[str] = None,
    category: Optional[str] = None,
    family: Optional[str] = None,
    element_id: Optional[str] = None,
    show_hidden: bool = False,
):
    # Shortcut for set_id. Only using uppercase device names for now.
    if device:
        set_id = str(device).upper()

    filt = generate_filter(datasource, set_id, category, family, element_id)

    out = ColumnODM(type=column).load_mongo(filt).fetch(show_hidden)

    return NetDBReturn(out=out, comment=f'Column data for {column} column.')


@app.put('/column', tags=['column'])
def replace_elements(
    data: RootContainer,
    response: Response,
):
    if READ_ONLY:
        response.status_code = status.HTTP_403_NOT_ALLOWED
        return ERR_READONLY

    if count := ColumnODM(data).replace():
        # Successful return
        word = 'elements'
        if count == 1:
            word = 'element'

        return NetDBReturn(
            comment=f'{data.column} column: {count} {word} successfully replaced.'
        )

    # Empty result. Nothing was replaced.
    response.status_code = status.HTTP_404_NOT_FOUND
    return NetDBReturn(result=False, comment='{data.column} column: nothing replaced.')


@app.delete('/column/{column}', tags=['column'])
def delete_elements(
    column: str,
    datasource: str,
    response: Response,
    set_id: Optional[str] = None,
    category: Optional[str] = None,
    family: Optional[str] = None,
    element_id: Optional[str] = None,
):
    if READ_ONLY:
        response.status_code = status.HTTP_403_NOT_ALLOWED
        return ERR_READONLY

    filt = generate_filter(datasource, set_id, category, family, element_id)

    count = ColumnODM(type=column).delete(filt)

    word = 'elements'
    if count == 1:
        word = 'element'

    return NetDBReturn(comment=f'{column} column: {count} {word} deleted.')


@app.get(
    '/column/{column}/{set_id}',
    tags=['device'],
    response_class=PrettyJSONResponse,
)
def get_column_set(
    column: str,
    set_id: str,
    response: Response,
):
    filt = {'set_id': set_id.upper()}

    out = ColumnODM(type=column).load_mongo(filt).fetch()
    if not out:
        response.status_code = status.HTTP_404_NOT_FOUND

        return NetDBReturn(result=False, comment=f'No column data found for {set_id}')

    return NetDBReturn(out=out, comment=f'Column data for {column} column.')
