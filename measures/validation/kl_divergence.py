#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, February 2017

"""The Kullback-Leibler dissimilarity

This module aims at giving a simple and fast implementation of
`Kullback-Leibler dissimilarity` for dissimilarity validation.

For more information on this concept, please visit:
* `Kullback-Leibler Wikipedia entry`_.
* `Analysis of Kullback-Leibler divergence`_.
* `Kullback-Leibler divergence - interpretation`_.
* `Questions about KL divergence`_.

Note:
    * The KL divergence is not a true "distance" because it is asymmetric and, it does not satisfy the triangle inequality.

Todo:
    * Module TODOs here!!!
    * You have to also use ``sphinx.ext.todo`` extension

The `Google Python Style Guide`_ was used in this docstring.

.. _Kullback-Leibler Wikipedia entry:
    https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence

.. _Analysis of Kullback-Leibler divergence:
    http://stats.stackexchange.com/questions/111445/analysis-of-kullback-leibler-divergence

.. _Kullback-Leibler divergence - interpretation:
    http://stats.stackexchange.com/questions/6814/kullback-leibler-divergence-interpretation

.. _Questions about KL divergence:
    http://stats.stackexchange.com/questions/1028/questions-about-kl-divergence/1569#1569

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import numpy as np

from scipy.stats import entropy as kl_divergence

from measures.validation.utils import intra_inter_class_distances, intra_inter_class_dissimilarities
from measures.validation.utils import cvt_distributions_list_to_dicts

# ---------------------------------------------------------------


def kullback_leibler_divergence(d1, d2):
    """Computes the Kullback-Leibler dissimilarity between two probability distributions.

    Args:
        d1 (dict): First probability distribution.
        d2 (dict): Second probability distribution.

    Returns:
        The Kullback-Leibler dissimilarity value.

    Note:
        * The KL divergence is not a true "distance" because it is asymmetric and, it does not satisfy the triangle inequality.

    """

    # validating distributions
    if not isinstance(d1, dict) or not isinstance(d2, dict):
        raise ValueError('Distributions must be dictionaries.')

    # insignificant value
    eps = 1e-6

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

    # building array distributions
    arr_pdf1 = np.array(pdf1) + eps
    arr_pdf2 = np.array(pdf2) + eps

    # computing the distance between the 2 probability density functions
    return kl_divergence(arr_pdf1, arr_pdf2)


def kl_divergence_in_euc_space(X, labels):
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

    # converting distances to frequency dicts
    d1, d2 = cvt_distributions_list_to_dicts(d1, d2)

    # returning the decidability index
    return kullback_leibler_divergence(d1, d2)


def kl_divergence_in_dis_space(X, labels, measure):
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

    # converting distances to frequency dicts
    d1, d2 = cvt_distributions_list_to_dicts(d1, d2)

    # returning the decidability index
    return kullback_leibler_divergence(d1, d2)
