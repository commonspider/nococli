import inspect
from functools import wraps
from inspect import Parameter
from string import Formatter
from typing import Any, TypedDict
from urllib.parse import urljoin

from requests import Session


def api(method: str, endpoint: str):
    def decorator(function):
        @wraps(function)
        def wrapper(self, **kwargs):
            return self.request(method, endpoint, defaults | kwargs)

        defaults = {}
        for name, value in inspect.signature(function).parameters.items():
            if value.default != Parameter.empty:
                defaults[name] = value.default
        return wrapper
    return decorator


class PageInfo(TypedDict):
    isFirstPage: bool
    isLastPage: bool
    page: int
    pageSize: int
    totalRows: int


class Base(TypedDict):
    id: str
    title: str


class BasesList(TypedDict):
    list: list[Base]
    pageInfo: PageInfo


class Table(TypedDict):
    id: str
    base_id: str
    table_name: str
    title: str
    type: str


class TablesList(TypedDict):
    list: list[Table]


class TableRecords(TypedDict):
    list: list[dict]
    pageInfo: PageInfo


class API:
    def __init__(self, base_url: str, api_token: str):
        self._session = Session()
        self._base_url = base_url
        self._api_token = api_token

    def request(self, method: str, endpoint: str, data: dict[str, Any] = None):
        data = data or {}
        endpoint = urljoin(self._base_url, endpoint.format(**data))
        path_vars = [fn for _, fn, _, _ in Formatter().parse(endpoint) if fn is not None]
        data = {name: value for name, value in data.items() if name not in path_vars and value is not None}
        response = self._session.request(
            method=method,
            url=endpoint,
            params=data,
            headers={"xc-token": self._api_token}
        )
        content = response.json()
        if response.status_code != 200:
            raise Exception(content)
        return content

    @api("GET", "/api/v2/meta/bases")
    def list_bases(self) -> TablesList:
        ...

    @api("GET", "/api/v2/meta/bases/{base_id}/tables")
    def list_tables(self, *, base_id: str) -> TablesList:
        ...

    @api("GET", "/api/v2/tables/{table_id}/records")
    def list_table_records(self, *, table_id: str, offset: int = None, limit: int = None, where: str = None) -> TableRecords:
        ...
