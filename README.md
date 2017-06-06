# Digit recognition using scikit-learn and MNIST database

Simple web application for recognition of handwritten digits. User draws digits on HTML canvas, then the resulting image
is sent to [Flask](http://flask.pocoo.org/)-powered backend. Image is transformed to proper format using 
[Pillow](https://pypi.python.org/pypi/Pillow/). Then model created with [scikit-learn](http://scikit-learn.org/stable/)
 trained on [MNIST database](http://yann.lecun.com/exdb/mnist/) is used to provide final prediction.
 
## Setup

1. Download repository
2. Install libs from `requirements.txt` (may require installing non-python dependencies)
3. Train model or provide own (more info below)
4. Run `app.py`
5. Open your browser and navigate to http://127.0.0.1:5000/

## Model training

Base model used project consists of two-step pipeline:
* PCA reduces data dimensionality ([wiki](https://en.wikipedia.org/wiki/Principal_component_analysis))
* kNN classifier is used as a estimator ([wiki](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm))

During training, the following parameters are tuned:
* PCA components count
* Number of neighbours in kNN
* metric used for calculating neighbour weight

To run model training run:
```
python train.py
```
**This can take few hours to complete**. To speed up you can change `PCA_N_CHOICES` and `KNN_N_CHOICES`.

After training `model.pkl` file will be created. Then it can be used for user input recognition. 

## Custom model

Alternatively you can use your custom model with web app. Every scikit-learn estimator/pipeline that handles MNIST input
(784-d vector) should work. Fit your model and save it to file using scikit function:
```
from sklearn.externals import joblib

joblib.dump(estimator, 'model.pkl')
```
Then copy `model.pkl` to project folder and run web app. 

## Future work

* Extraction of configuration params (model path, training hyperparams etc.)
* Improving model accuracy
* Provide additional features using OpenCV
