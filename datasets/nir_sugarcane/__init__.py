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
__data_set_path = "{}/data/NIR_sugar.mat".format(os.path.split(__file__)[0])

__pickle_path = "{}/cache/nir_sugarcane.pickle".format(os.path.split(__file__)[0])

# ---------------------------------------------------------------


# TODO: Add docstring with usage examples (see 'uv_fuel' data set)

@utils.load_data_from_pickle(__pickle_path)
def load_nir_sugarcane():
    # loading matlab data set
    raw_data = sio.loadmat(__data_set_path)

    # getting 'X' data
    x_data = raw_data['X'][0][0][7]
    samples_count, features_count = x_data.shape

    # getting X samples labels
    samples_labels = range(1, samples_count + 1)

    # getting X features labels
    features_labels = [int(nm) for nm in raw_data['X'][0][0][8][1][0]]

    # getting 'Brix' data
    brix_arr = raw_data['Brix'][0][0][7]
    brix_data = [b[0] for b in brix_arr]

    # getting 'pol' data
    pol_arr = raw_data['pol'][0][0][7]
    pol_data = [p[0] for p in pol_arr]

    # getting classes descriptions
    classes_headers = [l[0] for l in raw_data['X'][0][0][12][0][1]]

    # getting classes data
    classes_data = [
        # corresponds to classes_headers[0]
        raw_data['X'][0][0][12][0][0][0][0].tolist(),

        # corresponds to classes_headers[1]
        raw_data['X'][0][0][12][0][0][1][0].tolist(),

        # corresponds to classes_headers[2]
        raw_data['X'][0][0][12][0][0][2][0].tolist(),
    ]

    # getting classesid maps (to be able to convert labels into semantic labels)
    classesid_map = [
        # id_map for classes_headers[0]
        {t[0][0][0]: t[1][0] for t in raw_data['X'][0][0][14][0][0]},

        # id_map for classes_headers[1]
        {t[0][0][0]: t[1][0] for t in raw_data['X'][0][0][14][0][1]},

        # id_map for classes_headers[1]
        {t[0][0][0]: t[1][0] for t in raw_data['X'][0][0][14][0][2]},
    ]

    # columns to add
    regression_cols = {'brix': brix_data, 'pol': pol_data}
    class_cols = {
        ch: list(map(lambda x: classesid_map[i][x], classes_data[i]))
        for i, ch in enumerate(classes_headers)
    }

    # actually building the data set
    return utils.build_data_set(x_data, samples_labels, features_labels, extra_cols={**regression_cols, **class_cols})
