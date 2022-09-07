import os
import dropbox
import requests
from modzy import ApiClient

#Initialize Modzy and Dropbox clients
dbx = dropbox.Dropbox(os.getenv("DROPBOX_ACCESS_TOKEN"))
mdz = ApiClient(base_url=f"{os.getenv('MODZY_BASE_URL')}/api", api_key=os.getenv("MODZY_API_KEY"))

def main():

  #Loops through all images in a dropbox folder and adds the image names and URLs to a dict
  jobs = []
  path_urls = {}
  images = dbx.files_list_folder("")
  for image in images.entries:
    job_ID = image.path_display[1:].split(".")[0]
    jobs.append(job_ID)
    path_urls[job_ID] = get_dropbox_URL(image.path_display)

  # next query results
  results_data = {}
  for i, job in enumerate(jobs):
    job_details = mdz.jobs.get(job)
    result = mdz.results.block_until_complete(job)
    input_filename = list(result["results"].keys())[0]
    results_data[f'job_{i}'] = {
      "job_id": job,
      "input_name": input_filename,
      "model_version": job_details["model"]["version"],
      "label": result["results"][input_filename]["results.json"]["data"]["result"]["classPredictions"][0]["class"],
      "score": result["results"][input_filename]["results.json"]["data"]["result"]["classPredictions"][0]["score"],
      "num_upvotes": result["results"][input_filename]["voting"]["up"],
      "num_downvotes": result["results"][input_filename]["voting"]["down"]
    }  

  data = [{
    "data": {
      "image": path_urls[results_data[f'job_{i}']["job_id"]],
      "predicted_value": predicted_value_msg(results_data[f'job_{i}']["label"], results_data[f'job_{i}']["score"], results_data[f'job_{i}']["num_upvotes"], results_data[f'job_{i}']["num_downvotes"]),
      "downvotes": results_data[f'job_{i}']["num_downvotes"],
      "explainable_url": explainable_url(results_data[f'job_{i}']["job_id"], results_data[f'job_{i}']["input_name"])
    },
    "predictions": [{
      "model_version": results_data[f'job_{i}']["model_version"],
      "score": results_data[f'job_{i}']["score"],
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

  #Posts pre-annotated image links and results to Label Studio
  labelStudioURL = 'http://localhost:8080/api/projects/1/import'
  authHeader = 'Token ' + os.getenv("LABEL_STUDIO_ACCESS_TOKEN")
  r = requests.post(labelStudioURL, json=data, headers={'Authorization': authHeader})

def get_dropbox_URL(image_path): 
  #Gets shareable link from dropbox
  sharedURL = dbx.sharing_create_shared_link(image_path).url
  cleanURL = sharedURL.replace("dl=0","raw=1")
  return cleanURL

def predicted_value_msg(label, score, upvotes, downvotes):
  msg = f"Predicted value: {label} ({score:.1%} certainty) 👍: {upvotes} 👎: {downvotes}"
  print(msg)
  return msg

def explainable_url(job_ID, input_name):
  url = f"{os.getenv('MODZY_BASE_URL')}/operations/explainability/{job_ID}/{input_name}"
  print(url)
  return url

if __name__ == '__main__':
    main()