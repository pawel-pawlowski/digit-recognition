# Digit recognition using scikit-learn and MNIST database

Simple web application for recognition of handwritten digits. User draws digits on HTML canvas, then the resulting image
is sent to [Flask](http://flask.pocoo.org/)-powered backend. Image is transformed to proper format using 
[Pillow](https://pypi.python.org/pypi/Pillow/). Then model created with [scikit-learn](http://scikit-learn.org/stable/)
 trained on [MNIST database](http://yann.lecun.com/exdb/mnist/) is used to provide final prediction.