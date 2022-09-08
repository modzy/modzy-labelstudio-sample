import dropbox
import os
from modzy import ApiClient
from modzy._util import file_to_bytes

#Initializes Modzy and Dropbox clients
mdz = ApiClient(base_url=os.getenv('MODZY_BASE_URL'), api_key=os.getenv("MODZY_API_KEY"))
dbx = dropbox.Dropbox(os.getenv("DROPBOX_ACCESS_TOKEN"))

#Runs an inference on each image with a specified folder and then saves each to Dropbox
def main():

    #Defines the image folder being used, this can be changed to "images"
    image_folder = "images-test"

    for filename in os.listdir(image_folder):

        #Gets the filepath for each image
        f = os.path.join(image_folder,filename)
        
        #Sends the image to Modzy for inference and retrieves an inference job ID number
        job_ID = modzy_inference(f,filename)
        
        #Uploads the image to Dropbox and names it after the inference job ID number
        upload_image(f,job_ID)

        print(f"Inference ID {job_ID} complete")

#Submits an image to a model that performs Image-based Geolocation
def modzy_inference(image_path,image_ID):
    
    #This base64 encodes the image and formats it for this model
    sources = {}
    sources[image_ID] = {
        "image": file_to_bytes(image_path),
    }
    
    ##This is Modzy's unique ID for the Image-based Geolocation model
    model_id = "aevbu1h3yw"
    
    ##This is the version number of the model being used
    model_version = "1.0.1" 
    
    ##Submits the image for inference
    ##Adding "explain=True" enables explainability for each prediction
    job = mdz.jobs.submit_file(model_id, model_version, sources, explain=True)
    
    ##Returns the inference job ID
    return job.get("jobIdentifier")

#Uploads the image to Dropbox
def upload_image(image_path,image_ID):    
    dbx.files_upload(file_to_bytes(image_path),f"/{image_ID}.jpg")

if __name__ == '__main__':
    main()