from scrapy.selector import Selector
import requests

def get_graded_value(args):
    fn = {
        "ngc" : {
            "url" : lambda args : f"https://www.ngccoin.com/certlookup/{args['certNumber']}/{args['grade']}",
            "selector" : lambda selector : selector.css('.certlookup-stats-item-value::text')
        },
        "pcgs": {
            "url" : lambda args : f"https://www.pcgs.com/cert/{args['certNumber']}",
            "selector" : lambda selector: selector.xpath("//a[contains(@href, '/pricehistory')]/text()"),
        }
    }[args["type"]]

    url = fn["url"](args)
    response = requests.get(url)
    raw =  fn["selector"](Selector(text=response.text)).get()
    return raw.split(".")[0].replace("$", "").replace(",", "")


def get_spot_value(args):
    metalMap = {
        "silver" : "USD-XAG",
        "gold" : "USD-XAU"
    }
    response = requests.get(
        f"https://data-asg.goldprice.org/GetData/{metalMap[args['type']]}/1", 
        headers={'User-Agent': 'All those moments will be lost in time, like tears in rain.'})
    return response.json()[0].split(",")[1]


def controller(args):
    if args["type"] in ["pcgs", "ngc"]:
        return get_graded_value(args)
    elif args["type"] in ["gold", "silver"]:
        return get_spot_value(args)

if __name__ == "__main__":
    print("Value:", controller({"certNumber": "31611193", "type": "pcgs"}))
    print("Value:", controller({"certNumber": "4395155-025", "grade": '62', "type": "ngc"}))
    print("Value:", controller({"type": "gold"}))
    print("Value:", controller({"type": "silver"}))
    print("Value:", controller({"type": "chicken"}))