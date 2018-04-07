#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, January 2017

import os

import scipy.io as sio

import utils.datasets as utils

# ---------------------------------------------------------------

# data set paths
__data_set_path = "{}/data/peasraw-dataset.mat".format(os.path.split(__file__)[0])

__pickle_path = "{}/cache/mvda_peas_raw.pickle".format(os.path.split(__file__)[0])

# ---------------------------------------------------------------


# TODO: Add docstring with usage examples (see 'uv_fuel' data set)

@utils.load_data_from_pickle(__pickle_path)
def load_mvda_peas_raw():
    # loading matlab data set
    raw_data = sio.loadmat(__data_set_path)

    features_labels = raw_data['var_labels_all']

    data = raw_data['data_all']

    samples_labels = list(range(1, data.shape[0] + 1))

    return utils.build_data_set(data, samples_labels, features_labels)
