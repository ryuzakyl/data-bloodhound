#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, February 2017

from math import exp

import numpy as np

from measures.validation.utils import intra_inter_class_distances, intra_inter_class_dissimilarities, cvt_distributions_list_to_dicts

# ---------------------------------------------------------------


def distribution_overlap_area(d1, d2):
    # validating distributions are lists
    if not isinstance(d1, list) or not isinstance(d2, list):
        raise ValueError('Distributions must be lists')

    # converting to distributions to dictionaries
    d1, d2 = cvt_distributions_list_to_dicts(d1, d2)

    # declaring probability density functions
    pdf1 = []
    pdf2 = []

    # for each 'event' in distribution 1
    for k1 in d1:
        # adding p(k1) to pdf1
        pdf1.append(d1[k1])

        # if event 'k1' also occurs in d2
        if k1 in d2.keys():
            pdf2.append(d2[k1])
        else:
            pdf2.append(0)

    # for events only occurring in d2
    for k2 in d2:
        # if event k2 only occurs in d2
        if k2 not in d1.keys():
            pdf1.append(0)
            pdf2.append(d2[k2])

    # computing overlap values and overlap area
    overlap = [min(f1, f2) for f1, f2 in zip(pdf1, pdf2)]
    overlap_area = sum(overlap)

    # returning the 'normalized' area of distributions 'd1' and 'd2'
    return overlap_area / (sum(pdf1) + sum(pdf2) - overlap_area)


def intra_inter_class_separation(d1, d2):
    # validating distributions are lists
    if not isinstance(d1, list) or not isinstance(d2, list):
        raise ValueError('Distributions must be lists')

    # building nd arrays from
    d1_arr = np.array(d1)
    d2_arr = np.array(d2)

    # getting extreme points
    lb, ub = d1_arr.min(), d2_arr.max()

    # normalizing both distributions
    d1_arr = (d1_arr - lb) / (ub - lb)
    d2_arr = (d2_arr - lb) / (ub - lb)

    # returning index value
    return 1.0 - 1.0 / (exp(exp(d2_arr.mean() - d1_arr.mean())))


def intra_inter_class_separation_in_euc_space(X, labels):
    # validating 'data' and 'labels'
    if not isinstance(X, np.ndarray) or not (isinstance(labels, np.ndarray) or isinstance(labels, list)):
        raise ValueError('Verify data and labels.')

    # getting the values of labels as ndarray
    y = labels.copy() if isinstance(labels, np.ndarray) else np.array(labels)

    # validating consistency between samples and labels
    if X.shape[0] != y.shape[0]:
        raise ValueError('Amount of samples must be the same as the amount of labels.')

    # computing intra and inter class distances for euclidean space
    d1, d2 = intra_inter_class_distances(X, y, metric='euclidean')

    # returning the decidability index
    return intra_inter_class_separation(d1, d2)


def intra_inter_class_separation_in_dis_space(X, labels, measure):
    # validating 'data' and 'labels'
    if not isinstance(X, np.ndarray) or not (isinstance(labels, np.ndarray) or isinstance(labels, list)):
        raise ValueError('Verify data and labels.')

    # getting the values of labels as ndarray
    y = labels.copy() if isinstance(labels, np.ndarray) else np.array(labels)

    # validating consistency between samples and labels
    if X.shape[0] != y.shape[0]:
        raise ValueError('Amount of samples must be the same as the amount of labels.')

    # computing intra and inter class dissimilarities
    d1, d2 = intra_inter_class_dissimilarities(X, labels, measure)

    # returning the decidability index
    return intra_inter_class_separation(d1, d2)
