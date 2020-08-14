#!/usr/bin/python3
import csv
import argparse

import coinvalue


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Calculate the value of a coin collection.")

    parser.add_argument('csv', help="Path of the CSV file to calculate the value of.")

    args = parser.parse_args()
    print("Calculating value for " +args.csv)
    with open(args.csv, newline='') as csvfile:

        reader = csv.DictReader(csvfile)
        totalValue = 0
        for row in reader:
            totalValue += float(coinvalue.get_value(row))
        print(totalValue)