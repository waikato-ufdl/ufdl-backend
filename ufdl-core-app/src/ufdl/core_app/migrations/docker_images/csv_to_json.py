# simple tool to convert .csv files with docker images into .json

import argparse
import csv
import json

from collections import OrderedDict


def convert(csv_file, json_file):
    """
    Converts a CSV file with docker images information to json.

    :param csv_file: the CSV file to convert
    :type csv_file: str
    :param json_file: the JSON file to save the information to
    :type json_file: str
    """
    images = []
    with open(csv_file) as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            info = OrderedDict()
            info["name"] = row["name"]
            info["version"] = row["version"]
            info["url"] = row["url"]
            info["registry"] = OrderedDict()
            info["registry"]["url"] = row["registry_url"]
            info["registry"]["user"] = row["registry_user"]
            info["registry"]["password"] = row["registry_password"]
            info["cuda_version"] = row["cuda_version"]
            info["framework"] = OrderedDict()
            info["framework"]["name"] = row["framework_name"]
            info["framework"]["version"] = row["framework_version"]
            info["domain"] = row["domain"]
            info["tasks"] = row["types"].split(",")
            info["min_hardware_generation"] = row["min_hardware_generation"]
            info["cpu"] = bool(row["cpu"])
            info["license"] = row["license"]
            images.append(info)

    with open(json_file, "w") as fp:
        json.dump(images, fp, indent=2)


def main(args=None):
    """
    Performs the conversion.
    Use -h to see all options.

    :param args: the command-line arguments to use, uses sys.argv if None
    :type args: list
    """

    parser = argparse.ArgumentParser(
        description='Convert docker images information from CSV to JSON.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-c", "--csv", dest="csv_file", metavar="FILE", required=True, help="The CSV file with information on docker images to convert.")
    parser.add_argument("-j", "--json", dest="json_file", metavar="FILE", required=True, help="The JSON file to save the information on docker images to.")
    parsed = parser.parse_args(args=args)
    convert(parsed.csv_file, parsed.json_file)


if __name__ == "__main__":
    main()
