from __future__ import print_function

import numpy as np
import cv2
from scipy.ndimage.interpolation import shift
from sklearn.datasets import fetch_mldata
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score
from sklearn.base import BaseEstimator, TransformerMixin

import config


def fetch_data():
    """
    Fetch and prepare MNIST data.

    Function downloads MNIST data from http://mldata.org. Downloaded set is divided into train and test data.

    :return: train and test samples and labels in form of (x_train, x_test, y_train, y_test) tuple
    """
    # fetch data
    mnist = fetch_mldata('MNIST original')

    # load train and test data
    x, y = mnist['data'], mnist['target']
    x_train, x_test, y_train, y_test = x[:60000], x[60000:], y[:60000], y[60000:]

    # shuffle train data
    shuffle_index = np.random.permutation(60000)
    x_train, y_train = x_train[shuffle_index], y_train[shuffle_index]
    return x_train, x_test, y_train, y_test


def generate_shifted_set(x, y):
    # copy original set
    new_x = x.copy()
    new_y = y.copy()
    l, _ = x.shape

    # for each sample in set
    for i, (sample, label) in enumerate(zip(x, y)):
        # check progress
        if i % 100 == 0:
            print("Progress: {:.2f}%".format(i*100./l))
        # reshape into 2d image
        reshaped_sample = sample.reshape((28, 28))
        # for all possible shifts
        for s in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            # generate shifted sample
            shifted_sample = shift(reshaped_sample, s)
            # reshape into flat array
            new_sample = shifted_sample.reshape(784)
            # append sample to new arrays
            new_x = np.append(new_x, [new_sample], axis=0)
            new_y = np.append(new_y, label)
    return new_x, new_y


def deskew(sample):
    """Deskew image by calculating skew based on central moments and applying affine transform to image

    :param sample: Image sample to deskew as flat numpy array
    :return: flat array containing deskewed sample
    """
    img = sample.reshape((28, 28))
    m = cv2.moments(img)
    if abs(m['mu02']) < 1e-2:
        # no deskewing needed.
        return img.copy()
    # Calculate skew based on central moments.
    skew = m['mu11'] / m['mu02']
    # Calculate affine transform to correct skewness.
    M = np.float32([[1, skew, -0.5 * 28 * skew], [0, 1, 0]])
    # Apply affine transform
    img = cv2.warpAffine(img, M, (28, 28), flags=cv2.WARP_INVERSE_MAP | cv2.INTER_LINEAR)
    return img.reshape((784, ))


class ImageDeskewApplier(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return np.apply_along_axis(deskew, 1, X)


def perform_grid_search(x_train, y_train):
    """Create model pipeline and perform grid search to find best hyperparams for model.

    Pipeline consist of two steps:
    * PCA reduces data dimensionality
    * kNN classifier is used as a estimator

    Tuned hyperparams:
    * PCA components count
    * Number of neighbours in kNN
    * metric used for calculating neighbour weight

    :param x_train: training samples feature matrix
    :param y_train: training samples labels
    :return: pipeline with optimal hyperparams
    """
    # define base pipeline
    pipeline = Pipeline([
        ('deskew', ImageDeskewApplier()),
        ('pca', PCA()),
        ('knn', KNeighborsClassifier())
    ])

    # create dict containing possible hyperparams values
    param_grid = {
        'pca__n_components': config.PCA_N_CHOICES,
        'knn__n_neighbors': config.KNN_N_CHOICES,
        'knn__weights': ('distance', )
    }

    # perform actual grid search
    grid_search = GridSearchCV(pipeline, param_grid, cv=config.CV_FOLDS, scoring='accuracy', verbose=10, n_jobs=-1)
    grid_search.fit(x_train, y_train)

    # return pipeline with best params
    return grid_search.best_estimator_


def train_model(model_path=config.MODEL_PATH):
    """
    Train model with optimal params and save it on disk

    :param model_path: path to file where model should be stored
    """
    # fetch data
    print('Fetching MNIST data')
    x_train, x_test, y_train, y_test = fetch_data()

    # perform grid search
    print('Performing grid search')
    best_estimator = perform_grid_search(x_train, y_train)

    # save best estimator to model file
    print('Saving model to: {}'.format(model_path))
    joblib.dump(best_estimator, model_path)

    # check test set accuracy score
    print('Model testing'.format(model_path))
    y_test_predicted = best_estimator.predict(x_test)
    accuracy = accuracy_score(y_test_predicted, y_test)
    print("Accuracy: {}%".format(accuracy))


if __name__ == '__main__':
    train_model()
