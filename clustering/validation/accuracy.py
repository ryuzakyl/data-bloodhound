#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, March 2017

import numpy as np

from sklearn.metrics import accuracy_score

# ----------------------------------------

def accuracy_index(labels, true_labels):
    # getting the values of labels as ndarrays
    y = labels.copy() if isinstance(labels, np.ndarray) else np.array(labels)
    y_true = true_labels.copy() if isinstance(true_labels, np.ndarray) else np.array(true_labels)

    # validating consistency between labels and ground-truth
    if y.shape[0] != y_true.shape[0]:
        raise ValueError('Amount of labels and ground-truth labels must be the same.')

    # returning the accuracy computed by sklearn
    return accuracy_score(true_labels, labels, normalize=True)
