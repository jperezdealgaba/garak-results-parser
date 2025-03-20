#!/usr/bin/python3

import argparse
import csv
import json
import os
import sys
from datetime import datetime

file_name = "parsed_results_garak_" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".csv"


def check_names(path):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))


parser = argparse.ArgumentParser(description='Select file to parse.')
parser.add_argument('--file', dest='file',
                    default="garak-report.jsonl",
                    help='Select Garak JSONL file result to parse (default: garak-report.jsonl)')

parser.add_argument('--output', dest='output_destination',
                    default=r"results/" + file_name,
                    help='Select name of results file (the extension should be csv). If no file is specified, '
                         'a default parsed_results_<date>.csv file will be used. ')


args = parser.parse_args()
parsed_path = os.path.normpath(args.output_destination)

check_names(parsed_path)

json_list = []

if not os.path.isfile(args.file):
    print("Specified file name does not exist")
    sys.close(1)

with open(args.file, 'r') as jsonl_file:
    json_list = list(jsonl_file)

with open(parsed_path, 'x', newline='') as file:
    writer = csv.writer(file)
    field = ["Goal", "Prompt", "Output", "Trigger", "Detector"]
    writer.writerow(field)
    for json_str in json_list:
        json_line = json.loads(json_str)
        goal = ""
        prompt = ""
        output = ""

        if json_line["output"]:
            parsed_output = json.loads(json_line["output"])
            for elem in parsed_output:
                if json_line["goal"]:
                    goal = json_line["goal"].rstrip().replace("\n", "")
                if json_line["prompt"]:
                    prompt = json_line["prompt"].rstrip().replace("\n", "")
                output = parsed_output["response"].rstrip().replace("\n", "")
                if json_line["trigger"]:
                    trigger = json_line["trigger"].rstrip().replace("\n", "")
                else:
                    trigger = ""
                if json_line["trigger"]:
                    detector = json_line["detector"].rstrip().replace("\n", "")
                    detector = "https://reference.garak.ai/en/stable/garak.detectors." + detector.split('.')[0] + \
                               ".html" + "#garak.detectors." + detector
                else:
                    detector = ""
                parsed_line = [goal, prompt, output, trigger, detector]

        writer.writerow(parsed_line)
