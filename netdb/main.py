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
    """
    Called at API startup time. Initialize the database (i.e. make sure indexes are installed)
    unless started in read only mode.

    """
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
    """
    NetDB API error returns should have the same structure as normal returns. This handler
    implements that requirement in the case of Pydantic validation exceptions.

    request:
        The HTTP request context

    exc:
        The incoming Pydantic validation exception

    """
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
    """
    NetDB API error returns should have the same structure as normal returns. This handler
    implements that requirement in the case of HTTP 404 / not found errors.

    request:
        The HTTP request context

    exc:
        The incoming FastAPI HTTP 404 exception

    """
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
    """
    NetDB API error returns should have the same structure as normal returns. This handler
    implements that requirement in the case a NetDBException is thrown.

    request:
        The HTTP request context

    exc:
        The incoming NetDB exception

    """
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
def read_root() -> dict:
    """
    API root handler. Simply returns API name and status=up

    """
    return {
        'name': 'NetDB API version 2',
        'status': 'up',
    }


@app.get(
    '/column',
    tags=['list_columns'],
    response_class=PrettyJSONResponse,
)
def list_columns() -> NetDBReturn:
    """
    Return a list of available columns.

    """
    return NetDBReturn(
        out=COLUMN_TYPES,
        comment='Available NetDB columns.',
    )


@app.post('/validate', tags=['validate'])
def validate_column(
    data: RootContainer,
) -> NetDBReturn:
    """
    Validate column data. Can be used for dry runs before calling reload / add
    endpoints (which will also validate before adding.

    Most validation is already done by FastAPI / Pydantic by the time that
    control reaches this point.

    data:
        Column container with the column data to be validated.

    """
    ColumnODM(data).validate()

    return NetDBReturn(
        comment='Validation successful.',
    )


@app.post('/column', tags=['column'])
def reload_column(
    data: RootContainer,
    response: Response,
) -> NetDBReturn:
    """
    Replace entire column or parts of column filtered by datasource with new data.

    This endpoint is used by various SoT backends to manage 'their' portions of the
    configuration data column (as identified by the container  'datasource'
    attribute).

    data:
        Column container with the column data to be reloaded.

    response:
        HTTP response context passed in by FastAPI

    """
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
) -> NetDBReturn:
    """
    Get a column. Optionally filter the results using the following keys:

    column:
        Name of column to query (e.g. `bgp')

    datasource: ``None``
        Data source to query e.g. `netbox'

    set_id: ``None``
        Filter  query by `set_id' (this aligns with device name)

    device: ``None``
        Same as `set_id' key. Automatically uppercases input.

    category: ``None``
        Filter query by `category' key

    family: ``None``
        Filter query by `family' key

    element_id: ``None``
        Filter query by `element_id' key

    show_hidden: ``False``
        Return 'hidden' (i.e. weight < 1) elements

    Other arguments:

    response:
        HTTP response context passed in by FastAPI

    """
    # Shortcut for set_id. Only using uppercase device names for now.
    if device:
        set_id = str(device).upper()

    filt = generate_filter(datasource, set_id, category, family, element_id)

    out = ColumnODM(column_type=column).fetch(filt, show_hidden)

    return NetDBReturn(out=out, comment=f'Column data for {column} column.')


@app.put('/column', tags=['column'])
def replace_elements(
    data: RootContainer,
    response: Response,
) -> NetDBReturn:
    """
    Replace elements (or set in the case of 'flat' columns).

    data:
        Column container with the column data to be reloaded.

    response:
        HTTP response context passed in by FastAPI

    """
    if READ_ONLY:
        response.status_code = status.HTTP_403_NOT_ALLOWED
        return ERR_READONLY

    if count := ColumnODM(data).replace():
        # Successful return
        word = 'elements'
        if count == 1:
            word = 'element'

        return NetDBReturn(
            comment=f'{data.column_type} column: {count} {word} successfully replaced.'
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
) -> NetDBReturn:
    """
    Delete elements from a column. Delete column elements matching the following keys:

    column:
        Name of column to query (e.g. `bgp')

    datasource: ``None``
        Data source e.g. `netbox'

    set_id: ``None``
        Match by `set_id'

    category: ``None``
        Match by `category'

    family: ``None``
        Match by `family'

    element_id: ``None``
        Match by `element_id'

    Other arguments:

    response:
        HTTP response context passed in by FastAPI

    """
    if READ_ONLY:
        response.status_code = status.HTTP_403_NOT_ALLOWED
        return ERR_READONLY

    filt = generate_filter(datasource, set_id, category, family, element_id)

    count = ColumnODM(column_type=column).delete(filt)

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
) -> NetDBReturn:
    """
    Get a single set from a column identified by set_id.

    column:
        Name of column to query (e.g. `bgp')

    set_id:
        Set ID of set to query (this aligns with device name)

    response:
        HTTP response context passed in by FastAPI

    """

    # set_id is the same as device name and device names are capitalized. So
    # capitalize anything that comes in.
    filt = {'set_id': set_id.upper()}

    out = ColumnODM(column_type=column).fetch(filt)
    if not out:
        response.status_code = status.HTTP_404_NOT_FOUND

        return NetDBReturn(result=False, comment=f'No column data found for {set_id}')

    return NetDBReturn(out=out, comment=f'Column data for {column} column.')
