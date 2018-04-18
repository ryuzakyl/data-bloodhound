#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, February 2017

from classification.validation import knn as knn_val
from classification.validation import svm as svm_val

# ---------------------------------------------------------------


def knn_accuracy_in_euc_space(X, labels, folds=3):
    """KNN classifier accuracy in an Euclidean Space.

    Args:
        X (np.ndarray): The data array.
        labels (list, np.ndarray): The data labels.
        folds (int): Amount of folds for validation.

    Returns:
        The result of the grid search procedure in an euclidean space.

    Notes:
        * The result is a list if `_CVScoreTuple` instances. If needed, the user should iterate over it and use relevant values for his/hers analysis.

    """

    return knn_val.grid_search_in_euc_space(X, labels, folds)


def knn_accuracy_in_pretopological_space(X, labels, measure, folds=3):
    """KNN classifier accuracy in a Pretopological Space.

    Args:
        X (np.ndarray): The data array.
        labels (list, np.ndarray): The data labels.
        measure (int): The type of dissimilarity to use as metric (see 'measures' module).
        folds (int): Amount of folds for validation.

    Returns:
        The result of the grid search procedure in a pretopological space.

    Notes:
        * The result is a list if `_CVScoreTuple` instances. If needed, the user should iterate over it and use relevant values for his/hers analysis.

    """

    return knn_val.grid_search_in_pretopological_space(X, labels, measure, folds)


def knn_accuracy_in_dis_space(X, labels, measure, folds=3):
    """KNN classifier accuracy in a Dissimilarity Space.

    Args:
        X (np.ndarray): The data array.
        labels (list, np.ndarray): The data labels.
        measure (int): The type of dissimilarity to use as metric (see 'measures' module).
        folds (int): Amount of folds for validation.

    Returns:
        The result of the grid search procedure in a dissimilarity space.

    Notes:
        * The result is a list if `_CVScoreTuple` instances. If needed, the user should iterate over it and use relevant values for his/hers analysis.

    """

    return knn_val.grid_search_in_dis_space(X, labels, measure, folds)


def svm_accuracy_in_euc_space(X, labels, folds=3):
    """SVM classifier accuracy in an Euclidean Space.

    Args:
        X (np.ndarray): The data array.
        labels (list, np.ndarray): The data labels.
        folds (int): Amount of folds for validation.

    Returns:
        The result of the grid search procedure in an euclidean space.

    Notes:
        * The result is a list if `_CVScoreTuple` instances. If needed, the user should iterate over it and use relevant values for his/hers analysis.

    """

    return svm_val.grid_search_in_euc_space(X, labels, folds)


def svm_accuracy_in_euc_space_params(X, labels, params, folds=3):
    """SVM classifier accuracy in an Euclidean Space.

    Args:
        X (np.ndarray): The data array.
        labels (list, np.ndarray): The data labels.
        params (dict): Dictionary of parameters and its values.
        folds (int): Amount of folds for validation.

    Returns:
        The result of the grid search procedure in an euclidean space.

    Notes:
        * The result is a list if `_CVScoreTuple` instances. If needed, the user should iterate over it and use relevant values for his/hers analysis.

    """

    return svm_val.grid_search_in_euc_space_params(X, labels, params, folds)


def svm_accuracy_in_dis_space(X, labels, measure, folds=3):
    """Grid search for SVM classifier in a Dissimilarity Space.

    Args:
        X (np.ndarray): The data array.
        labels (list, np.ndarray): The data labels.
        measure (int): The type of dissimilarity to use as metric (see 'measures' module).
        folds (int): Amount of folds for validation

    Returns:
        The Grid search results for the given data and labels.

    """

    return svm_val.grid_search_in_dis_space(X, labels, measure, folds)


def svm_accuracy_in_dis_space_params(X, labels, measure, params, folds=3):
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

    return svm_val.grid_search_in_dis_space_params(X, labels, measure, params, folds)
