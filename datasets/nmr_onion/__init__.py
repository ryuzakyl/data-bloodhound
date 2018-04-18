#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, January 2017

import os

import scipy.io as sio

import utils.datasets as utils

# ---------------------------------------------------------------

# data set paths
__data_path = "{}/data/onion_NMR.mat".format(os.path.split(__file__)[0])

__pickle_path = "{}/cache/nmr_onion.pickle".format(os.path.split(__file__)[0])

# ---------------------------------------------------------------

# TODO: Add docstring with usage examples (see 'uv_fuel' data set)


@utils.load_data_from_pickle(__pickle_path)
def load_nmr_onion():
    # loading matlab data set object
    raw_data = sio.loadmat(__data_path)

    # validating loaded data
    if raw_data is None:
        raise Exception('Error while loading 1H-NMR Onion data.')

    # getting samples labels
    samples_labels = list(map(lambda x: x[0][0], raw_data['Samples_name']))

    # getting features labels
    features_labels = raw_data['ppm'][0].tolist()

    # getting samples data
    data = raw_data['x'].tolist()

    # getting onion percent
    onion_percent = raw_data['onion'][0].tolist()

    # actually building the data set
    return utils.build_data_set(data, samples_labels, features_labels, {'% onion': onion_percent})
