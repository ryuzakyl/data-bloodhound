#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, January 2017

import os

import numpy as np
import pandas as pd
import scipy.io as sio

import utils.datasets as utils

# ---------------------------------------------------------------

# data set paths
__data_path = "{}/data/NMR_40wines.mat".format(os.path.split(__file__)[0])

__pickle_path = "{}/cache/nmr_wine.pickle".format(os.path.split(__file__)[0])

# ---------------------------------------------------------------

# TODO: Add docstring with usage examples (see 'uv_fuel' data set)


@utils.load_data_from_pickle(__pickle_path)
def load_nmr_wines():
    """Loads the NMR Wines data set.

    Returns:
        A Pandas DataFrame with all the data set info.

    Examples:
        >>> ds = load_nmr_wines()
        >>> ds['wine_data'].shape
        (40, 8729)
        >>> ds['wine_ints'].shape
        (22, 1)

    """

    # loading matlab data set object
    raw_data = sio.loadmat(__data_path)

    # validating loaded data
    if raw_data is None:
        raise Exception('Error while loading 1H-NMR Wines data.')

    # getting features labels
    features_labels = raw_data['ppm'][0].tolist()

    # getting properties labels
    props_labels = list(map(lambda x: x[0], raw_data['Label'][0]))

    # getting samples data
    data = raw_data['X']

    # getting properties data
    props_data = raw_data['Y']

    # creating the wine data set
    all_data = np.hstack([data, props_data])
    all_labels = range(all_data.shape[0])
    all_features = features_labels + props_labels
    wine_ds = utils.build_data_set(all_data.tolist(), all_labels, all_features)

    # ----------------------

    wine_ints_data = raw_data['wine_ints'][0]
    wine_ints_ds = pd.DataFrame(wine_ints_data)

    # ----------------------

    # the final data set
    ds = {
        'wine_data': wine_ds,
        'wine_ints': wine_ints_ds,
    }

    # returning the final data set
    return ds
