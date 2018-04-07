#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, March 2017

import os

import h5py
import numpy as np
import pandas as pd

import utils.datasets as utils

# ---------------------------------------------------------------

# data set paths
__data_set_path = "{}/data/Wine_v7.mat".format(os.path.split(__file__)[0])

__pickle_path = "{}/cache/mw_gc_ms_wines.pickle".format(os.path.split(__file__)[0])

# ---------------------------------------------------------------

# TODO: Add docstring with usage examples (see 'uv_fuel' data set)


@utils.load_data_from_pickle(__pickle_path)
def load_mw_gc_ms_wines():
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

    # getting class labels
    wine_origin = np.squeeze(raw_data['Class'].value).tolist()

    hdf5_mass_labels = raw_data['Label_Mass_channels']
    ms_labels = [
        raw_data[hdf5_mass_labels[i][0]].value[0][0]
        for i in range(hdf5_mass_labels.size)
    ]

    hdf5_gc_labels = raw_data['Label_Elution_time']
    gc_labels = [
        raw_data[hdf5_gc_labels[i][0]].value[0][0]
        for i in range(hdf5_gc_labels.size)
    ]

    # building 'gc_ms' data set from unaligned data
    gc_ms_data_raw = raw_data['Data_GC_unaligned'].value
    ms_count, gc_count, wines_count = gc_ms_data_raw.shape
    gc_ms_data_raw_matlab_like = gc_ms_data_raw.reshape((wines_count, gc_count, ms_count))
    mw_gc_ms_raw = pd.Panel(gc_ms_data_raw_matlab_like, items=samples_labels, major_axis=gc_labels, minor_axis=ms_labels)

    # building 'gc_ms' data set from aligned data
    gc_ms_data = raw_data['Data_GC'].value
    ms_count, gc_count, wines_count = gc_ms_data_raw.shape
    gc_ms_data_matlab_like = gc_ms_data.reshape((wines_count, gc_count, ms_count))
    mw_gc_ms = pd.Panel(gc_ms_data_matlab_like, items=samples_labels, major_axis=gc_labels, minor_axis=ms_labels)

    # building the final data set structure
    data_set = {
        'gc_ms_unaligned':  mw_gc_ms_raw,
        'gc_ms_aligned':    mw_gc_ms,
        'origin':          wine_origin,
    }

    # returning the built data set
    return data_set
