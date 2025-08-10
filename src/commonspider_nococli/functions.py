from pandas import DataFrame

from .api import API


def list_bases(api: API):
    response = api.list_bases()
    df = DataFrame(response["list"])
    return df[["id", "title"]]


def dump_base(api: API, base_id: str, skip: list[str] = ()):
    data = {}
    for table in api.list_tables(base_id=base_id)["list"]:
        if table["type"] != "table":
            continue
        if table["title"] in skip:
            continue
        records = api.list_table_records(table_id=table["id"])["list"]
        for record in records:
            record.pop("CreatedAt", None)
            record.pop("UpdatedAt", None)
        data[table["title"]] = records
    return data
