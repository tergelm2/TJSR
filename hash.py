import hashlib

with open("data/raw/annual_aqi_by_county_2023.zip", "rb") as f:
    data = f.read()

hash = hashlib.sha256(data).hexdigest()

print(hash)