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
__data_set_path = "{}/data/SWRI_Diesel_NIR.mat".format(os.path.split(__file__)[0])

__pickle_path = "{}/cache/nir_fuel.pickle".format(os.path.split(__file__)[0])

# ---------------------------------------------------------------


# TODO: Add docstring with usage examples (see 'uv_fuel' data set)

@utils.load_data_from_pickle(__pickle_path)
def load_nir_fuel():
    # loading matlab data set
    raw_data = sio.loadmat(__data_set_path)

    # getting samples labels
    samples_labels = [int(l) for l in raw_data['diesel_spec'][0][0][8][0][0]]

    # getting features labels
    features_labels = [f for f in raw_data['diesel_spec'][0][0][12][1][0][0]]

    # getting properties values
    props_labels = [s.strip() for s in raw_data['diesel_prop'][0][0][8][1][0]]

    # getting spectra data
    data = raw_data['diesel_spec'][0][0][7]

    # getting properties data
    props_data = raw_data['diesel_prop'][0][0][7].T

    other_cols = {
        prop_name: prop_data
        for prop_name, prop_data in zip(props_labels, props_data)
    }

    # actually building the data set
    return utils.build_data_set(data, samples_labels, features_labels, extra_cols=other_cols)
