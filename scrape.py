import re
import requests
import json

response = requests.get("https://www.statebicycle.com/collections/sale?sort_by=price-descending")
data = json.loads(re.findall("var meta = (.*);\\nfor", response.text)[0])
products = [p for p in data['products'] if p['vendor'].startswith("State")]

content = """
https://www.statebicycle.com/collections/sale?sort_by=price-descending

|price|type|name|
|---|---|---|
"""

for product in products:
    for variant in product['variants']:
        price = int(variant['price'] / 100)
        type_ = product['type'].replace("|", "!")
        name = variant['name']
        content += f"| ${price:>6} | {type_:<15.15} | {name} |\n"

with open("README.md", "w") as fp:
    fp.write(content)