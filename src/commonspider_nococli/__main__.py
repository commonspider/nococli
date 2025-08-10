import json
import sys
from argparse import ArgumentParser

from pandas import DataFrame

from .api import API

arg_parser = ArgumentParser()
arg_parser.add_argument("-c", "--config", default="noco.json")
subparsers = arg_parser.add_subparsers(dest="command")

subparsers.add_parser("list-bases")

dump_base_parser = subparsers.add_parser("dump-base")
dump_base_parser.add_argument("base_id")

args = arg_parser.parse_args()

with open(args.config) as f:
    config = json.load(f)

api = API(**config)

if args.command == "list-bases":
    response = api.list_bases()
    df = DataFrame(response["list"])
    print(df[["id", "title", "type"]])

elif args.command == "dump-base":
    data = {}
    for table in api.list_tables(base_id=args.base_id)["list"]:
        if table["type"] != "table":
            continue
        records = api.list_table_records(table_id=table["id"])["list"]
        for record in records:
            record.pop("CreatedAt", None)
            record.pop("UpdatedAt", None)
        data[table["title"]] = records
    print(json.dumps(data, indent=2))

else:
    print(f"Unrecognized command: {args.command}")
    sys.exit(1)
