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
__glycol1_data_set_path = "{}/data/glycol1-dataset.mat".format(os.path.split(__file__)[0])

__glycol2_data_set_path = "{}/data/glycol2-dataset.mat".format(os.path.split(__file__)[0])

__pickle_path = "{}/cache/ms_glycol.pickle".format(os.path.split(__file__)[0])

# ---------------------------------------------------------------


# TODO: Add docstring with usage examples (see 'uv_fuel' data set)

@utils.load_data_from_pickle(__pickle_path)
def load_ms_glycol():
    """Loads the MS Glycol data set.

    Returns:
        A dictionary with all the data set info.

    Examples:
        >>> ds = load_ms_glycol()
        >>> ds['glycol1'].shape
        (162, 254)
        >>> ds['glycol2'].shape
        (126, 256)

    """

    # loading matlab data sets
    glycol1_raw_data = sio.loadmat(__glycol1_data_set_path)
    glycol2_raw_data = sio.loadmat(__glycol2_data_set_path)

    # validating loaded data
    if glycol1_raw_data is None or glycol2_raw_data is None:
        raise Exception('Error while loading Glycol data set.')

    # ----------------

    # getting samples labels
    glycol1_samples_labels = glycol1_raw_data['obj_labels_all'].tolist()

    # getting features labels
    glycol1_features_labels = glycol1_raw_data['var_labels_all'].tolist()

    # getting glycol1 data
    glycol1_data = glycol1_raw_data['data_all'].tolist()

    # building glycol1 data set
    glycol1_ds = utils.build_data_set(glycol1_data, glycol1_samples_labels, glycol1_features_labels)

    # ----------------

    glycol2_samples_labels = glycol2_raw_data['obj_labels_all']

    glycol2_features_labels = glycol2_raw_data['var_labels_all']

    glycol2_data = glycol2_raw_data['data_all']

    # building glycol2 data set
    glycol2_ds = utils.build_data_set(glycol2_data, glycol2_samples_labels, glycol2_features_labels)

    # ----------------

    # the glycol data set
    ds = {
        'glycol1': glycol1_ds,
        'glycol2': glycol2_ds,
    }

    # returning the final data set
    return ds
