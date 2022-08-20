from bs4 import BeautifulSoup
import requests
import requests_cache
import time
from time import sleep
import webbrowser
import re
import pandas as pd
from pandas import ExcelWriter
from shutil import which
import linecache as lc
import os
import io
from io import open

f = open ('upc.txt')
all_upc = f.read().splitlines()
f.close()

f = open ('sku.txt')
all_sku = f.read().splitlines()
f.close()

all_url_products = []

all_data = {}

count = 0

try:

	for sku in all_sku:

		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36', 'referer':'https://google.es',}

		url = f'https://shopwilkinsons.xolights.com/catalog?itemNumVal={sku}'

		req = requests.get(url, headers=headers, timeout=10)

		sleep(2)

		soup = BeautifulSoup(req.text, "html.parser")

		try:
			products = soup.find_all('div', class_="itemBorderBox")

			if products:
				for product in products:
					product = product.find('a').get('href')
					product_url = f'https://shopwilkinsons.xolights.com/{product}'

					all_url_products.append(product_url)

					count += 1

					print(f"Url #{count} found.")

			else:
				all_url_products.append('Not found')
				count += 1
				print(f"Url #{count} not found.")


		except:
			print(f'Error2... {e}')
			pass
	
	all_data["UPC"] = all_upc
	all_data["SKU"] = all_sku
	all_data["URL"] = all_url_products

	
	all_data = pd.DataFrame(all_data, columns = ['UPC', 'SKU', 'URL'])

	with ExcelWriter('data.xlsx') as writer:

		all_data.to_excel(writer, 'Data', index=False)

except Exception as e:
	print(f'Error1... {e}')

input('Listo')