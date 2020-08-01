from scrapy.selector import Selector
import requests

def value(args):
    """Determines the value of a NGC graded coin given its certificate number and grade."""
    url = f"https://www.ngccoin.com/certlookup/{args['certNumber']}/{args['grade']}"
    response = requests.get(url)
    raw = Selector(text=response.text).css('.certlookup-stats-item-value::text').get()
    return raw.split(".")[0].replace("$", "").replace(",", "")

if __name__ == "__main__":
    print("Value:", value({"certNumber": "4395155-025", "grade": '62'}))