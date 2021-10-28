import argparse
import os
import requests
import csv
from typing import Dict
from config import count_variables
import time
from datetime import datetime, timedelta
import argparse


def pull_data(count_vars: Dict, start_time: int, freq: str):
	
	with open(f'scmts_file_{start_time}_days.csv', 'w', newline='') as csvFile:
		for var_name, variable in count_vars.items():
			csv_writer = csv.writer(csvFile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
			csv_writer.writerow([f"Data for {var_name}"])
			frequency = variable[freq]
			request = f"http://things.ubidots.com/api/v1.6/variables/{frequency}/values?token=BBFF-M8Ztfi5FylKtixs7BWImIWDdhYkRBn&format=csv&start={start_time}&timeZone=America/Los_Angeles"
			req = requests.get(request)
			content_utf = req.content.decode('utf-8')
			csv_reader = csv.reader(content_utf.splitlines(), delimiter=',')
			counter_list = list(csv_reader)
			
			for row in counter_list:
				csv_writer.writerow(row)
			# print(f"Data for {var_name}: {content_utf}\n")
	csvFile.close()


def date_to_millisec(start: int):
	now = datetime.now()
	delta = timedelta(days=start)
	start_time = (now - delta).timestamp() * 1000
	return start_time

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--start_date', type=int, default=7)
	parser.add_argument('--end_date', type=int, default=0)
	parser.add_argument('--freq', choices=['daily', 'hourly'], default='hourly')
	return parser.parse_args()

def main():

	args = parse_args()
	start_time = int(date_to_millisec(args.start_date))
	frequency = args.freq
	print(f"Importing data from {start_time} ago")
	pull_data(count_variables, start_time, frequency)


main()