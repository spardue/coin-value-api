from scrapy.selector import Selector
import requests

def parse_value(func):
    def wrapper():

        func()
    return wrapper

def value(args):
    """Determines the value of a NGC graded coin given its certificate number and grade."""
    url = f"https://www.pcgs.com/cert/{args['certNumber']}"
    response = requests.get(url)
    raw = Selector(text=response.text).xpath("//a[contains(@href, '/pricehistory')]/text()").get()
    return raw.split(".")[0].replace("$", "").replace(",", "")


def get_value(urlFn, selectorFn, args):
    url = urlFn(args)
    response = requests.get(url)
    raw = selectorFn(Selector(text=response.text)).get()
    return raw.split(".")[0].replace("$", "").replace(",", "")


urlFn = lambda args : f"https://www.pcgs.com/cert/{args['certNumber']}"
selectorFn = lambda selector : selector.xpath("//a[contains(@href, '/pricehistory')]/text()")

if __name__ == "__main__":
    print("Value:", get_value(urlFn, selectorFn, {"certNumber": "31611193"}))