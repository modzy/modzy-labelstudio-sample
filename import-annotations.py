import requests
import os

data = [{
  "data": {
    "image": "https://previews.dropbox.com/p/thumb/ABpFAjvEwRGMRYPekWNnSYAEjfYlaKAEtqx_UEGtV8yPzWvT41VWUPGWA64JI8rUm4gdsYr7I3dCC0ztGsf9lEx_x2GIcWZdw8JMKEVFO_iTpA38jq520nS-DhSld9BKvxoMZ1hKGEtZEXlHHxyk5vn22gfj1iB3ZAT2KifeAql7dqZ7Li212LtSBVJ1w6WgcoIirG0PEVEpOH9H0mm4NchnTpq71PuHMUPwZe-MnRuwUCKTVdrBMxDKcdE8CFoxsSxeSAWVOUjtInnJRk-L71mp84I3-xzrpV65fLmzoShyddGOsn_LGQsvAhoKbbkqT0agaCy9jIzqRb6AdYV9_lnkUFAjf5GGFzyLM9WQILMBzbgfIToU2YgiviJTHmir96g/p.jpeg" 
  },
  "predictions": [{
    "model_version": "1.0.1",
    "score": 0.986,
    "result": [
      {
        "id": "da9b3857-4e1c-4a8e-b023-18abf4cb1223",
        "type": "choices",
        "from_name": "location", "to_name": "image",
        "value": {
          "choices": ["Cairo, Northern Africa"]
      }
    }]
  }]
}]

labelStudioURL = 'http://localhost:8080/api/projects/1/import'
authHeader = 'Token ' + os.environ.get("LABEL_STUDIO_ACCESS_TOKEN")
r = requests.post(labelStudioURL, json=data, headers={'Authorization': authHeader})
