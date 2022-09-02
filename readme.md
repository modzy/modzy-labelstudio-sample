# Modzy - Label Studio Sample Project
This sample project demonstrates how to use Modzy and Label studio to dynamically re-label production inferences using a combination of semi-supervised learning, explainable AI, and human-in-the-loop review. This combination of techniques provides a comprehensive and low-lift way to create training data sets from production data that can be used to retrain a machine learning model.

This sample project uses:
* Modzy: For model serving and explainability
* Dropbox: For storing images
* Label Studio: For labeling production inference results

As a result, you'll need:
* An instance of Modzy
* A Dropbox acccount
* An instance of Label Studio

## Getting started

### Label Studio set-up
First, install Label Studio and start it up. Instructions can be found (here)[https://github.com/heartexlabs/label-studio#try-out-label-studio] (installing with PIP was a breeze).

Once it's running, log in and download your API (access token)[https://labelstud.io/guide/api.html#Authenticate-to-the-API].

### Modzy Set-up
In your instance of Modzy, (create a project)[https://docs.modzy.com/docs/how-to-create-a-project] and then download your project (api key)[https://docs.modzy.com/docs/how-to-use-a-project]

### Dropbox Set-up
If you don't have one, create a free Dropbox account.

Then, you'll need to create a (Dropbox App)[https://www.dropbox.com/developers/reference/getting-started]

Next, give your app the following permissions: `files.metadata.write` `files.content.write` `files.content.read` `sharing.write`

Finally, generate an (access token)[https://dropbox.tech/developers/generate-an-access-token-for-your-own-account]

### Inference Set-Up
Before you can start running the sample images as inferences, you'll need to do the following:
 * Clone this repo
 * [Optional, but recommended] Create a virtual environment within your project folder and activate it
 * Run `$ pip install -r requirements.txt` to install all necessary dependencies
 * Create a copy of `.env-sample` and rename it to `.env`. Then update it to include your API access tokens for Modzy, Dropbox, and Label Studio.
 * Run `$ source .env` to load your environment variables
 * Update the `base_url` variable in `inference.py` to the URL of your instance of Modzy

### Run inference.py
Run `$ python3 inference.py`
This should send all of the images in the images-test folder to a model in Modzy, and upload all of those images to your dropbox account

### Label Studio Set-up
* Update the `base_url` variable in `import-annotations.py` to the URL of your instance of Modzy
* Update the `labelStudioURL` variable in `import-annotations.py` to the URL of your instance of Label Studio

### Run import-annotations.py
Run `$ python3 import-annotations.py`
This should send all of the predictions generated from Modzy over to Label Studio for review and labeling.