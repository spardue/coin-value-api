#!/usr/bin/python3
import csv

import coinvalue

if __name__ == "__main__":
    with open('./test/test.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        totalValue = 0
        for row in reader:
            totalValue += float(coinvalue.get_value(row))
        print(totalValue)