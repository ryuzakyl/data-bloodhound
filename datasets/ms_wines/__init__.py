#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, March 2017

import os

import h5py
import numpy as np

import utils.datasets as utils

# ---------------------------------------------------------------

# data set paths (taking data from the Multiway GC-MS data set)
__data_set_path = "{}/../mw_gc_ms_wines/data/Wine_v7.mat".format(os.path.split(__file__)[0])

__pickle_path = "{}/cache/ms_wines.pickle".format(os.path.split(__file__)[0])

# ---------------------------------------------------------------

# TODO: Add docstring with usage examples (see 'uv_fuel' data set)


@utils.load_data_from_pickle(__pickle_path)
def load_ms_wines():
    # loading matlab (v7.3) data
    raw_data = h5py.File(__data_set_path)

    # validating loaded data
    if raw_data is None:
        raise Exception('Error while loading GC-MS Wines data.')

    # https://groups.google.com/forum/#!topic/h5py/FT7nbKnU24s
    hdf5_samples_labels = raw_data['Label_Wine_samples']
    samples_labels = [
        ''.join(chr(c) for c in raw_data[hdf5_samples_labels[0][i]].value)
        for i in range(hdf5_samples_labels.size)
    ]

    # gettting class labels
    wine_origin = np.squeeze(raw_data['Class'].value).tolist()

    hdf5_mass_labels = raw_data['Label_Mass_channels']
    ms_labels = [
        raw_data[hdf5_mass_labels[i][0]].value[0][0]
        for i in range(hdf5_mass_labels.size)
    ]

    ms_data = raw_data['Mass_profiles'].value.T

    # returning the built data set
    return utils.build_data_set(ms_data, samples_labels, ms_labels, extra_cols={'origin': wine_origin})
