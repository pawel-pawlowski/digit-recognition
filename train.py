from __future__ import print_function

import numpy as np
from sklearn.datasets import fetch_mldata
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score

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
        ('pca', PCA()),
        ('knn', KNeighborsClassifier())
    ])

    # create dict containing possible hyperparams values
    param_grid = {
        'pca__n_components': config.PCA_N_CHOICES,
        'knn__n_neighbors': config.KNN_N_CHOICES,
        'knn__weights': ('uniform', 'distance')
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
