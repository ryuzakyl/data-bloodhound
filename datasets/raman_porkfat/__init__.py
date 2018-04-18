#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, October 2016

import os
from collections import OrderedDict

import scipy.io as sio

import utils.datasets as utils

# ---------------------------------------------------------------

# data set paths
__data_set_path = "{}/data/ramanporkfat.mat".format(os.path.split(__file__)[0])
__pickle_path = "{}/cache/ramanporkfat.pickle".format(os.path.split(__file__)[0])

# ---------------------------------------------------------------


# TODO: Add docstring with usage examples (see 'uv_fuel' data set)

@utils.load_data_from_pickle(__pickle_path)
def load_raman_porkfat():
    # loading matlab data set object
    raw_data = sio.loadmat(__data_set_path)

    # validating loaded data
    if raw_data is None:
        raise Exception('Error while loading Raman Pork Fat data.')

    # getting X and Y info
    X = raw_data['X']
    Y = raw_data['Y']

    # getting samples labels
    samples_labels = list(X['label'][0][0][0][0])

    # getting features labels
    features_labels = list(map(str, list(X['axisscale'][0][0][1][0][0])))

    # getting samples data
    data = list(map(list, X['data'][0][0]))

    # adding extra columns
    other_cols = OrderedDict()

    # adding first labeling
    classes1 = list(X['class'][0][0][0][0][0][0])
    other_cols['classes1'] = classes1

    # adding second labeling
    classes2 = list(X['class'][0][0][0][0][1][0])
    other_cols['classes2'] = classes2

    # adding third labeling
    classes3 = list(X['class'][0][0][0][0][2][0])
    other_cols['classes3'] = classes3

    # adding properties
    props_labels = list(Y['label'][0][0][1][0])
    props = list(map(list, Y['data'][0][0].T))
    for i, pl in enumerate(props_labels):
        other_cols[pl] = props[i]

    # actually building the data set
    return utils.build_data_set(data, samples_labels, features_labels, other_cols)
