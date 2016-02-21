from pathlib import Path
import json
from provider import Provider


def jsonPrint(dataDict):
    print(json.dumps(dataDict))


def consolePrint(dataDict):
    for k in dataDict.keys():
        v = dataDict[k]
        if type(v) is list:
            buf = ''
            outStr = k + ': '
            for i in range(len(k) + 2):
                buf = buf + ' '
            for e in v:
                print(outStr + e)
                outStr = buf
        else:
            print(k + ': ' + v)


def listMods():
    p = Path('providers')
    print("Available providers:")
    mods = list(p.glob('*.json'))
    for m in mods:
        print("- " + m.stem)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    # Required arguments
    parser.add_argument(
        'provider',
        nargs='?',
        help="Which provider to use (or, the type of object to query).")
    parser.add_argument(
        'query',
        nargs='?',
        help="The query for the provider to consume.")
    # Other options
    parser.add_argument('-p', '--providers', action='store_true',
                        help="List available providers and exit.")
    # These arguments affect the output and are exclusive
    outputGroup = parser.add_mutually_exclusive_group()
    outputGroup.add_argument('-c', '--console', action='store_true',
                             help="Output console-formatted text (default).")
    outputGroup.add_argument('-j', '--json', action='store_true',
                             help="Output json.")
    args = parser.parse_args()

    if args.providers:
        listMods()
    elif (not args.provider) and (not args.query):
        print("Provider and query required. See --help")
    elif args.json:
        mod = Provider(args.provider)
        jsonPrint(mod.scrape(args.query))
    else:
        mod = Provider(args.provider)
        consolePrint(mod.scrape(args.query))
