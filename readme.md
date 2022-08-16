# Modzy - Label Studio Sample Project
This sample project demonstrates how to use Modzy and Label studio to dynamically re-label production inferences using a combination of semi-supervised learning, explainable AI, and human-in-the-loop review. This combination of techniques provides a comprehensive and low-lift way to create training data sets, based on production data, that can be used to retrain a machine learning model.

This sample project uses:
* Modzy: For model serving and explainability
* Dropbox: For storing production images
* Label Studio: For labeling production inference results

As a result, you'll need:
* An instance of Modzy and an API key
* A Dropbox acccount and access token with the `files.content.write` and `files.content.read` permissions
* An instance of Label Studio