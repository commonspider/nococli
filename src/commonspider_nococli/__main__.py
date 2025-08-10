import json
import sys
from argparse import ArgumentParser

from .api import API
from .functions import list_bases, dump_base

arg_parser = ArgumentParser()
arg_parser.add_argument("-c", "--config", default="noco.json")
subparsers = arg_parser.add_subparsers(dest="command")

subparsers.add_parser("list-bases")

dump_base_parser = subparsers.add_parser("dump-base")
dump_base_parser.add_argument("--skip", action="extend", nargs="+")
dump_base_parser.add_argument("base_id")

args = arg_parser.parse_args()

with open(args.config) as f:
    config = json.load(f)

api = API(**config)

if args.command == "list-bases":
    df = list_bases(api)
    print(df)

elif args.command == "dump-base":
    data = dump_base(api, args.base_id, args.skip)
    print(json.dumps(data, indent=2))

else:
    print(f"Unrecognized command: {args.command}")
    sys.exit(1)
