import argparse
import json
from .api import GreyNoise, GreyNoiseError

def main():
    parser = argparse.ArgumentParser(description='Request GreyNoise')
    parser.add_argument('--list', '-l', help="List tags", action='store_true')
    parser.add_argument('--ip', '-i', help="Query an IP address")
    parser.add_argument('--tag', '-t', help="Query a tag")
    parser.add_argument('--format', '-f', help="Output format", choices=["csv", "json"], default="json")
    args = parser.parse_args()

    gn = GreyNoise()
    if args.list:
        res = gn.tags()
        if args.format == "json":
            print(json.dumps(res, indent=4, sort_keys=True))
        else:
            for i in res:
                print(i)
    elif args.ip:
        try:
            res = gn.query_ip(args.ip)
        except GreyNoiseError:
            print("IP not found")
        else:
            if args.format == "json":
                print(json.dumps(res, indent=4, sort_keys=True))
            else:
                print("Tag;Category;Confidence;Intention;First Seen;Last Seen;ASN;Datacenter;Link;Org;OS;RDNS;Tor")
                for r in res:
                    print("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s" % (
                            r["name"],
                            r["category"],
                            r["confidence"],
                            r["intention"],
                            r["first_seen"],
                            r["last_updated"],
                            r["metadata"]["asn"],
                            r["metadata"]["datacenter"],
                            r["metadata"]["link"],
                            r["metadata"]["os"],
                            r["metadata"]["org"],
                            r["metadata"]["rdns"],
                            r["metadata"]["tor"]
                        )
                    )
    elif args.tag:
        try:
            res = gn.query_tag(args.tag)
        except GreyNoiseError:
            print("TAG does not exist")
        else:
            if args.format == "json":
                print(json.dumps(res, indent=4, sort_keys=True))
            else:
                print("IP;Tag;Category;Confidence;Intention;First Seen;Last Seen;ASN;Datacenter;Link;Org;OS;RDNS;Tor")
                for r in res:
                    print("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s" % (
                            r["ip"],
                            r["name"],
                            r["category"],
                            r["confidence"],
                            r["intention"],
                            r["first_seen"],
                            r["last_updated"],
                            r["metadata"]["asn"],
                            r["metadata"]["datacenter"],
                            r["metadata"]["link"],
                            r["metadata"]["os"],
                            r["metadata"]["org"],
                            r["metadata"]["rdns"],
                            r["metadata"]["tor"]
                        )
                    )

    else:
        parser.print_help()
