#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, February 2017

import numpy as np
from sklearn import svm
from sklearn.preprocessing import MinMaxScaler
from scipy.spatial.distance import pdist, squareform

import measures
import classification.validation.utils as clf_utils

# -----------------------------------------------------

# TODO: Add a validation method involving some sort of dissimilarity kernel. Ask Yeni.


def __valid_svm_params(params):
    """Whether supplied params are valid for an SVM classifier

    Args:
        params (dict): Dictionary of parameters and its values.

    Returns:
        Whether supplied params are valid or not.

    """

    # valid svm params
    svm_params = ['kernel', 'C', 'gamma']

    # the parameters for SVM are strictly the 3 stated above
    return len(set(params.keys()) & set(svm_params)) != 3


def grid_search_in_euc_space(X, labels, folds=5):
    """Grid search for SVM classifier.

    Args:
        X (np.ndarray): The data array.
        labels (list, np.ndarray): The data labels.
        folds (int): Amount of folds for validation

    Returns:
        The Grid search results for the given data and labels.

    """

    # validating 'data' and 'labels'
    if not isinstance(X, np.ndarray) or not (isinstance(labels, np.ndarray) or isinstance(labels, list)):
        raise ValueError('Verify data and labels.')

    # getting the values of labels as ndarray
    y = labels.copy() if isinstance(labels, np.ndarray) else np.array(labels)

    # validating consistency between samples and labels
    if X.shape[0] != y.shape[0]:
        raise ValueError('Amount of samples must be the same as the amount of labels.')

    # building svm classifier
    # . http://stackoverflow.com/questions/41486610/knowing-the-number-of-iterations-needed-for-convergence-in-svr-scikit-learn
    svm_clf = svm.SVC(verbose=2, max_iter=-1)

    # performing grid search
    # . https://stats.stackexchange.com/questions/37669/libsvm-reaching-max-number-of-iterations-warning-and-cross-validation
    parameters = {
        'kernel': ('linear', 'rbf', 'poly'),
        'C': [0.01, 0.1, 1.0, 10, 100],
    }

    # adding data normalization/scaling
    # . http://stackoverflow.com/questions/17455302/gridsearchcv-extremely-slow-on-small-dataset-in-scikit-learn
    # . https://stats.stackexchange.com/questions/37669/libsvm-reaching-max-number-of-iterations-warning-and-cross-validation
    X = MinMaxScaler(copy=True).fit_transform(X.T).T

    # storing results for debug purposes
    results = clf_utils.grid_search_cv(svm_clf, X, y, parameters, folds=folds)

    # returning the grid search results
    return results


def grid_search_in_euc_space_params(X, labels, params, folds=5):
    """Grid search for SVM classifier.

    Args:
        X (np.ndarray): The data array.
        labels (list, np.ndarray): The data labels.
        params (dict): Dictionary of parameters and its values.
        folds (int): Amount of folds for validation.

    Returns:
        The Grid search results for the given data and labels.

    """

    # validating 'data' and 'labels'
    if not isinstance(X, np.ndarray) or not (isinstance(labels, np.ndarray) or isinstance(labels, list)):
        raise ValueError('Verify data and labels.')

    # getting the values of labels as ndarray
    y = labels.copy() if isinstance(labels, np.ndarray) else np.array(labels)

    # validating consistency between samples and labels
    if X.shape[0] != y.shape[0]:
        raise ValueError('Amount of samples must be the same as the amount of labels.')

    # validating the parameters
    if not isinstance(params, dict) or not __valid_svm_params(params):
        raise AttributeError('Invalid parameters for SVM classifier.')

    # building svm classifier
    svm_clf = svm.SVC()

    # storing results for debug purposes
    results = clf_utils.grid_search_cv(svm_clf, X, y, params, folds=folds)

    # returning the grid search results
    return results


def grid_search_in_dis_space(X, labels, measure, folds=3):
    """Grid search for SVM classifier in a Dissimilarity Space.

    Args:
        X (np.ndarray): The data array.
        labels (list, np.ndarray): The data labels.
        measure (int): The type of dissimilarity to use as metric (see 'measures' module).
        folds (int): Amount of folds for validation

    Returns:
        The Grid search results for the given data and labels.

    """

    # validating 'data' and 'labels'
    if not isinstance(X, np.ndarray) or not (isinstance(labels, np.ndarray) or isinstance(labels, list)):
        raise ValueError('Verify data and labels.')

    # getting the values of labels as ndarray
    y = labels.copy() if isinstance(labels, np.ndarray) else np.array(labels)

    # validating consistency between samples and labels
    if X.shape[0] != y.shape[0]:
        raise ValueError('Amount of samples must be the same as the amount of labels.')

    # getting the metric function
    d = measures.measure_to_function[measure]

    # build distance/dissimilarity matrix
    dm = squareform(pdist(X, d))

    # returning result of grid search considering the dissimilarity space euclidean
    return grid_search_in_euc_space(dm, labels, folds)


def grid_search_in_dis_space_params(X, labels, measure, params, folds=3):
    """Grid search for SVM classifier in a Dissimilarity Space.

    Args:
        X (np.ndarray): The data array.
        labels (list, np.ndarray): The data labels.
        measure (int): The type of dissimilarity to use as metric (see 'measures' module).
        params (dict): Dictionary of parameters and its values.
        folds (int): Amount of folds for validation

    Returns:
        The Grid search results for the given data and labels.

    """

    # validating 'data' and 'labels'
    if not isinstance(X, np.ndarray) or not (isinstance(labels, np.ndarray) or isinstance(labels, list)):
        raise ValueError('Verify data and labels.')

    # getting the values of labels as ndarray
    y = labels.copy() if isinstance(labels, np.ndarray) else np.array(labels)

    # validating consistency between samples and labels
    if X.shape[0] != y.shape[0]:
        raise ValueError('Amount of samples must be the same as the amount of labels.')

    # validating the parameters
    if not isinstance(params, dict) or not __valid_svm_params(params):
        raise AttributeError('Invalid parameters for SVM classifier.')

    # getting the metric function
    d = measures.measure_to_function[measure]

    # build distance/dissimilarity matrix
    dm = squareform(pdist(X, d))

    # returning result of grid search considering the dissimilarity space euclidean
    return grid_search_in_euc_space_params(dm, labels, params, folds)
