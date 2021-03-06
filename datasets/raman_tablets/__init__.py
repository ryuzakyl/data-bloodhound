#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, February 2017

import os

import scipy.io as sio

import utils.datasets as utils

# ---------------------------------------------------------------

# data set paths
__data_set_path = "{}/data/Ramandata_tablets.mat".format(os.path.split(__file__)[0])

__pickle_path = "{}/cache/raman_tablets.pickle".format(os.path.split(__file__)[0])

# ---------------------------------------------------------------


# TODO: Add docstring with usage examples (see 'uv_fuel' data set)

@utils.load_data_from_pickle(__pickle_path)
def load_raman_tablets():
    # loading matlab data set
    raw_data = sio.loadmat(__data_set_path)

    # getting samples labels
    samples_labels = raw_data['ObjLabels'].tolist()

    # getting features labels
    raw_features = raw_data['VarLabels'].tolist()
    features_labels = list(map(float, raw_features[2:]))

    # getting data
    raw_data = raw_data['Matrix']
    data = raw_data[:, 2:]

    # creating the extra columns
    other_cols = {
        'active (% w/w)':   raw_data[:, 0].tolist(),
        'Type':             raw_data[:, 1].astype(int).tolist(),
    }

    # returning the built data set
    return utils.build_data_set(data, samples_labels, features_labels, extra_cols=other_cols)
