#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, February 2017

import os

import numpy as np
import scipy.io as sio

import utils.datasets as utils

# ---------------------------------------------------------------

# data set paths
__x_data_path = "{}/data/TecatorX.mat".format(os.path.split(__file__)[0])
__y_data_path = "{}/data/TecatorY.mat".format(os.path.split(__file__)[0])

__pickle_path = "{}/cache/nir_tecator.pickle".format(os.path.split(__file__)[0])

# ---------------------------------------------------------------


# TODO: Add docstring with usage examples (see 'uv_fuel' data set)

@utils.load_data_from_pickle(__pickle_path)
def load_nir_tecator():
    # loading matlab x data
    x_raw_data = sio.loadmat(__x_data_path)['TecatorX']
    x_rows, x_cols = x_raw_data.shape

    # loading matlab y data
    y_raw_data = np.ravel(sio.loadmat(__y_data_path)['TecatorY'])

    # threshold for the 2 classes
    fat_thres = 20.0

    # getting class labels
    classes = y_raw_data >= fat_thres

    # getting samples labels
    samples_labels = range(1, x_rows + 1)

    # getting features labels
    features_labels = range(1, x_cols + 1)

    return utils.build_data_set(data=x_raw_data, samples_labels=samples_labels, features_labels=features_labels, extra_cols={'fat': y_raw_data, 'class': classes.astype(int)})
