# This file is used to verify your http server acts as expected
# Run it with `python3 test.py``

import requests

model_inputs = {'prompt': 'Stable Diffusions ...via... 🍌 Banana Serverless'}

res = requests.post('http://localhost:8000/', json = model_inputs)

print(res.status_code)

path = "image_response.png"

with open(path, "wb") as f:
    f.write(res.content)

print(f"Saved {path=}")