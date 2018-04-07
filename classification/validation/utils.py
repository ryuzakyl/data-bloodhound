#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, February 2017

import numpy as np
from sklearn import grid_search

# -----------------------------------------------------


def grid_search_cv(clf, X, labels, params, folds=3):
    """Grid search for SVM classifier.

    Args:
        clf: Classifier to perform grid search on.
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

    # creating the generic grid searcher
    gs = grid_search.GridSearchCV(clf, params, cv=folds, verbose=3)

    # fitting the grid searcher
    gs.fit(X, y)

    # sorting by cross validation accuracy
    sorted_scores = sorted(gs.grid_scores_, key=lambda x: x[1], reverse=True)

    # returning scores in such order
    return sorted_scores

