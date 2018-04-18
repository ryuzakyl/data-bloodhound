#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, February 2017

import numpy as np
import sklearn.neighbors as nn
from scipy.spatial.distance import pdist, squareform

import measures
from classification.validation import utils as clf_utils

# ---------------------------------------------------------------


def grid_search_in_euc_space(X, labels, folds=3):
    """KNN classifier accuracy in an Euclidean Space.

    Args:
        X (np.ndarray): The data array.
        labels (list, np.ndarray): The data labels.
        folds (int): Amount of folds for validation.

    Returns:
        The result of the grid search procedure in an euclidean space.

    Notes:
        * The result is a list if ``_CVScoreTuple`` instances. If needed, the user should iterate over it and use relevant values for his/hers analysis.

    """

    # validating 'data' and 'labels'
    if not isinstance(X, np.ndarray) or not (isinstance(labels, np.ndarray) or isinstance(labels, list)):
        raise ValueError('Verify data and labels.')

    # getting the values of labels as ndarray
    y = labels.copy() if isinstance(labels, np.ndarray) else np.array(labels)

    # validating consistency between samples and labels
    if X.shape[0] != y.shape[0]:
        raise ValueError('Amount of samples must be the same as the amount of labels.')

    # creating a KNN classifier with euclidean metric
    knn = nn.KNeighborsClassifier(metric='euclidean')

    # list of `k` neighbours to test for
    params = {'n_neighbors': [1, 3, 5]}

    # performing grid search with cross validation
    gs_results = clf_utils.grid_search_cv(knn, X, y, params, folds=folds)

    # returning the grid search validation results
    return gs_results


def grid_search_in_pretopological_space(X, labels, measure, folds=3):
    """KNN classifier accuracy in a Pretopological Space.

    Args:
        X (np.ndarray): The data array.
        labels (list, np.ndarray): The data labels.
        measure (int): The type of dissimilarity to use as metric (see 'measures' module).
        folds (int): Amount of folds for validation.

    Returns:
        The result of the grid search procedure in a pretopological space.

    Notes:
        * The result is a list if ``_CVScoreTuple`` instances. If needed, the user should iterate over it and use relevant values for his/hers analysis.

    """

    # validating 'data' and 'labels'
    if not isinstance(X, np.ndarray) or not (isinstance(labels, np.ndarray) or isinstance(labels, list)):
        raise ValueError('Verify data and labels.')

    # getting the values of labels as ndarray
    y = labels.copy() if isinstance(labels, np.ndarray) else np.array(labels)

    # validating consistency between samples and labels
    if X.shape[0] != y.shape[0]:
        raise ValueError('Amount of samples must be the same as the amount of labels.')

    # the specified metric must be one of the implemented measures
    if measure not in measures.measure_to_function:
        raise ValueError('Unknown dissimilarity measure.')

    # creating a KNN classifier with a custom metric
    knn = nn.KNeighborsClassifier(metric=measures.measure_to_function[measure])

    # list of `k` neighbours to test for
    params = {'n_neighbors': [1, 3, 5]}

    # performing grid search with cross validation
    gs_results = clf_utils.grid_search_cv(knn, X, y, params, folds=folds)

    # returning the grid search validation results
    return gs_results


def grid_search_in_dis_space(X, labels, measure, folds=3):
    """KNN classifier accuracy in a Dissimilarity Space.

    Args:
        X (np.ndarray): The data array.
        labels (list, np.ndarray): The data labels.
        measure (int): The type of dissimilarity to use as metric (see 'measures' module).
        folds (int): Amount of folds for validation.

    Returns:
        The result of the grid search procedure in a dissimilarity space.

    Notes:
        * The result is a list if ``_CVScoreTuple`` instances. If needed, the user should iterate over it and use relevant values for his/hers analysis.

    """

    # validating 'data' and 'labels'
    if not isinstance(X, np.ndarray) or not (isinstance(labels, np.ndarray) or isinstance(labels, list)):
        raise ValueError('Verify data and labels.')

    # getting the values of labels as ndarray
    y = labels.copy() if isinstance(labels, np.ndarray) else np.array(labels)

    # validating consistency between samples and labels
    if X.shape[0] != y.shape[0]:
        raise ValueError('Amount of samples must be the same as the amount of labels.')

    # the specified metric must be one of the implemented measures
    if measure not in measures.measure_to_function:
        raise ValueError('Unknown dissimilarity measure.')

    # getting the metric function
    d = measures.measure_to_function[measure]

    # build distance/dissimilarity matrix
    dm = squareform(pdist(X, d))

    # returning the accuracy considering the dissimilarity space euclidean
    return grid_search_in_euc_space(dm, y, folds)
