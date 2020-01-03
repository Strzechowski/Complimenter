#!/usr/bin/env python3

import requests, json

request = requests.get("https://complimentr.com/api")
compliment = request.json()['compliment']

letter_counter = 0

for letter in compliment:
    letter_counter += 1

print('#'*letter_counter)
print(compliment.upper())
print('#'*letter_counter)