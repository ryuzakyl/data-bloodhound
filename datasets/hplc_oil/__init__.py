#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, October 2016

import os
from collections import OrderedDict

import scipy.io as sio

import utils.datasets as utils

# ---------------------------------------------------------------

# data set paths
__data_set_path = "{}/data/HPLCforweb.mat".format(os.path.split(__file__)[0])
__pickle_path = "{}/cache/hplc_oil.pickle".format(os.path.split(__file__)[0])

# ---------------------------------------------------------------


# TODO: Add docstring with usage examples (see 'uv_fuel' data set)

@utils.load_data_from_pickle(__pickle_path)
def load_hplc_oil():
    # loading matlab data set object
    raw_data = sio.loadmat(__data_set_path)

    # validating loaded data
    if raw_data is None:
        raise Exception('Error while loading HPLC Oil data.')

    # getting 'HPLCforweb' info
    hplc_oil = raw_data['HPLCforweb']

    # getting samples labels
    samples_labels = list(hplc_oil['label'][0][0][0][0])

    # getting features labels
    features_labels = list(hplc_oil['include'][0][0][1][0][0])

    # getting samples data
    data = list(map(list, hplc_oil['data'][0][0]))

    # adding extra columns
    other_cols = OrderedDict()

    # getting samples classes
    class_labels = list(hplc_oil['class'][0][0][0][0][0])
    other_cols['class'] = class_labels

    classid_map = {
        # 1 --> not
        hplc_oil['classlookup'][0][0][0][0][1][0][0][0]: hplc_oil['classlookup'][0][0][0][0][1][1][0],
        # 2 --> olive
        hplc_oil['classlookup'][0][0][0][0][2][0][0][0]: hplc_oil['classlookup'][0][0][0][0][2][1][0],
        # 3 --> mix
        hplc_oil['classlookup'][0][0][0][0][3][0][0][0]: hplc_oil['classlookup'][0][0][0][0][3][1][0],
    }
    classids = list(map(lambda x: classid_map[x], class_labels))
    other_cols['classid'] = classids

    # actually building the data set
    return utils.build_data_set(data, samples_labels, features_labels, other_cols)
