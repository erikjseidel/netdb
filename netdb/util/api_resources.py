import json
from typing import Union, Any
from pydantic import BaseModel
from starlette.responses import Response

DESCRIPTION = """
Version 2 of the NetDB API. 🚀

For more information visit [NetDB at Github](https://github.com/erikjseidel/netdb/)
"""


# Used by FastAPI for docs / redoc generation
tags = [
    {
        "name": "list_columns",
        "description": "show a list of available columns",
    },
    {
        "name": "column",
        "description": "endpoints and methods for querying and manipulating column data",
    },
    {
        "name": "device",
        "description": "show a single set (e.g. device configuration) in a column",
    },
    {
        "name": "validate",
        "description": "validates an NetDBContainer configuration dataset without loading it",
    },
    {
        "name": "override",
        "description": "endpoints and methods for querying and manipulating overrides",
    },
]

ERR_READONLY = {
    'result': False,
    'comment': 'NetDB API is running in read only mode.',
}

ERR_OVERRIDE_DISABLED = {
    'result': False,
    'comment': 'NETDB API overrides disabled.',
}


class NetDBReturn(BaseModel):
    """
    A netdb return type which includes all the data expected to be fund in a return
    to a netdb consumer.

    """

    result: bool = True
    error: bool = False
    out: Union[dict, list, None] = None
    comment: Union[str, None] = None


def generate_filter(*args, **kwargs) -> dict:
    """
    A helper function to create MongoDB compatible query filters. Filters for
    the netdb standard document keys, i.e. the following keys:

    datasource: ``None``
        The datasource e.g. SoT with witch the netdb document is associated

    set_id: ``None``
        The top level sub-dict within a netdb column dict

    category: ``None``
        The optional category sub-dict of set_id in certain netdb columns

    family: ``None``
        The optional category sub-dict of category dicts in certain netdb columns

    element_id: ``None``
        The element_id inner-most dict in certain netdb columns

    """
    key_names = ['datasource', 'set_id', 'category', 'family', 'element_id']

    ret = {k: v for k, v in dict(zip(key_names, args)).items() if v}
    ret.update({k: v for k, v in kwargs.items() if v})

    return ret


class PrettyJSONResponse(Response):
    """
    Class to implement a FastAPI Response. Used to return a 'prettified' JSON
    response to the consumer.

    """

    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        """
        Implements FastAPI Response.render(). Returns 'prettified' JSON output.

        """
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=2,
            separators=(", ", ": "),
        ).encode("utf-8")
