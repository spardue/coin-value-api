from scrapy.selector import Selector
import requests

cache = {}

def get_graded_value(args):
    """Get the graded value of NGC or PCGS coins."""
    fn = {
        "ngc" : {
            "url" : lambda args : f"https://www.ngccoin.com/certlookup/{args['certNumber']}/{args['grade']}",
            "selector" : lambda selector : selector.css('.certlookup-stats-item-value::text')
        },
        "pcgs": {
            "url" : lambda args : f"https://www.pcgs.com/cert/{args['certNumber']}",
            "selector" : lambda selector : selector.xpath("//a[contains(@href, '/pricehistory')]/text()"),
        }
    }[args["type"]]

    url = fn["url"](args)
    response = requests.get(url)
    raw =  fn["selector"](Selector(text=response.text)).get()
    return raw.split(".")[0].replace("$", "").replace(",", "")

cached_spot = {}
def get_spot_value(args):
    """Get the spot value of a metal object."""
    metalMap = {
        "silver" : "USD-XAG",
        "gold" : "USD-XAU"
    }

    spot = None
    try:
        spot = cached_spot[metalMap[args['type']]]
    except KeyError:
        response = requests.get(
            f"https://data-asg.goldprice.org/GetData/{metalMap[args['type']]}/1", 
            headers={'User-Agent': 'All those moments will be lost in time, like tears in rain.'})
        spot = response.json()[0].split(",")[1]
        cached_spot[metalMap[args['type']]] = spot        
    
    oz = float(args["oz"])
    value = float(spot) * oz
    return value

def _get_value(args):
    """Non safe value lookup."""
    if args["type"] in ["pcgs", "ngc"]:
        return get_graded_value(args)
    elif args["type"] in ["gold", "silver"]:
        return get_spot_value(args)

def get_value(args):
    """Value lookup that uses a cached value on failure."""
    argsHash = hash(frozenset(args.items()))
    try:
        value = _get_value(args)
        cache[argsHash] = value
    except:
        print("There was a failure so reading from the cache.")
        value = cache[argsHash]
    return value


if __name__ == "__main__":
    print("Value:", get_value({"certNumber": "31611193", "type": "pcgs"}))
    print("Value:", get_value({"certNumber": "4395155-025", "grade": '62', "type": "ngc"}))
    print("Value:", get_value({"type": "gold", "oz" : "1"}))
    print("Value:", get_value({"type": "gold", "oz" : "2"}))
    print("Value:", get_value({"type": "gold", "oz" : "0.5"}))
    print("Value:", get_value({"type": "silver", "oz" : "0.9"}))
    #curl -O "https://docs.google.com/spreadsheets/d/1l38jWmjcF0jLp8b45tFLN-2-zuyvGfOYAie4TXmxPtA/gviz/tq?tqx=out:csv&sheet=Sheet1"