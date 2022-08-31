import os
import dropbox
import requests
from modzy import ApiClient

""" client = ApiClient(base_url=os.getenv("MODZY_URL"), api_key=os.getenv("MODZY_API_KEY"))
jobs = ["2c793d35-9180-453e-b522-7da461dd8b8a", "0e695113-43e0-4b09-a198-a9b720e3945e", "26367a86-08f1-42fb-9819-b7c69643dfe0", "11024c64-fddc-435c-b50b-7123faa08905", "9ac42c64-a891-49d0-a850-cb17f28731b9"]
​
'''
The remainder of this script can be adopted to generalize the programmatic creation of the label studio pre-annotations data.
There are two things the user must prepare to leverage the below code:
  1. Assemble all image URLs into a dictionary where each key-value pair represents the image name (e.g., image.jpg), and the corresponding value represents the full image URL
  2. Query all job IDs in Modzy to query results for
'''
​
# next query results
results_data = {}
for i, job in enumerate(jobs):
  result = client.results.block_until_complete(job)
  input_filename = list(result["results"].keys())[0]
  results_data[f'job_{i}'] = {
    "job_id": job,
    "input_name": input_filename,
    "label": result["results"][input_filename]["results.json"]["data"]["result"]["classPredictions"][0]["class"],
    "score": result["results"][input_filename]["results.json"]["data"]["result"]["classPredictions"][0]["score"],
    "num_upvotes": result["results"][input_filename]["voting"]["up"],
    "num_downvotes": result["results"][input_filename]["voting"]["down"]
  }  
  print(f"Results saved for {job}")
​
​
data = [{
  "data": {
    "image": path_urls[results_data[f'job_{i}']["input_name"]]
  },
  "predictions": [{
    "model_version": MODEL_VERSION,
    "score": results_data[f'job_{i}']["score"],
    # "Upvotes": results_data[f'job_{i}']["num_upvotes"],
    # "Downvotes": results_data[f'job_{i}']["num_downvotes"],
    "result": [
      {
        "id": results_data[f'job_{i}']["job_id"],
        "type": "choices",
        "from_name": "location", 
        "to_name": "image",
        "value": {
          "choices": [results_data[f'job_{i}']["label"]]
      }
    }]
  }]
} for i in range(len(results_data))]
​
print(data) """

def get_dropbox_URL(image_path):
    #Creates a Dropbox client
    dbx = dropbox.Dropbox(os.environ.get("DROPBOX_ACCESS_TOKEN"))
    
    #Gets shareable link from dropbox
    sharedURL = dbx.sharing_create_shared_link(image_path).url
    cleanURL = sharedURL.replace("dl=0","raw=1")
    print(cleanURL)
url = '/d8237400-a78f-4e2a-b715-89cfd0df4e49.jpg'
get_dropbox_URL(url)

#labelStudioURL = 'http://localhost:8080/api/projects/1/import'
#authHeader = 'Token ' + os.environ.get("LABEL_STUDIO_ACCESS_TOKEN")
#r = requests.post(labelStudioURL, json=data, headers={'Authorization': authHeader})
