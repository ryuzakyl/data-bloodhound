#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, January 2017

import os

import pandas as pd
import scipy.io as sio

import utils.datasets as utils

# ---------------------------------------------------------------

# data set paths
__data_set_path = "{}/data/alcohol-dataset.mat".format(os.path.split(__file__)[0])

__pickle_path = "{}/cache/nir_alcohol.pickle".format(os.path.split(__file__)[0])

# ---------------------------------------------------------------


# TODO: Add docstring with usage examples (see 'uv_fuel' data set)

@utils.load_data_from_pickle(__pickle_path)
def load_nir_alcohol():
    """Loads the NIR Alcohol data set.

    Returns:
        A Pandas DataFrame with all the data set info.

    Examples:
        >>> ds = load_nir_alcohol()
        >>> ds.ix['train'].shape
        (27, 104)
        >>> ds.ix['new'].shape
        (13, 104)
        >>> ds.ix['msc'].shape
        (27, 104)

    """

    # loading matlab data set
    raw_data = sio.loadmat(__data_set_path)

    # ----------------

    # getting all variable/features labels
    var_labels_all = raw_data['var_labels_all'].tolist()

    # getting spectra labels
    var_labels_spectra = [int(l) for l in var_labels_all[3:]]

    # getting properties labels
    var_labels_properties = var_labels_all[:3]

    # ----------------

    # getting all data (train-new-msc)
    data_all = raw_data['data_all']

    # getting spectra data
    data_spectra = data_all[:, 3:]

    # getting properties data
    data_properties = data_all[:, :3]

    # ----------------

    obj_labels_train = raw_data['obj_labels_train'].tolist()
    data_train = data_spectra[:27, :]
    other_cols_train = {p_name: p_data for p_name, p_data in zip(var_labels_properties, data_properties[:27, :].T)}

    ds_train = utils.build_data_set(data_train, obj_labels_train, var_labels_spectra, extra_cols=other_cols_train)

    # ----------------

    obj_labels_new = raw_data['obj_labels_new'].tolist()
    data_new = data_spectra[27:40, :]
    other_cols_new = {p_name: p_data for p_name, p_data in zip(var_labels_properties, data_properties[27:40, :].T)}

    ds_new = utils.build_data_set(data_new, obj_labels_new, var_labels_spectra, extra_cols=other_cols_new)

    # ----------------

    obj_labels_msc = raw_data['obj_labels_mscorrected'].tolist()
    data_msc = data_spectra[40:, :]
    other_cols_msc = {p_name: p_data for p_name, p_data in zip(var_labels_properties, data_properties[40:, :].T)}

    ds_msc = utils.build_data_set(data_msc, obj_labels_msc, var_labels_spectra, extra_cols=other_cols_msc)

    # ----------------

    # training/validation data sets and labels
    data_sets = [ds_train, ds_new, ds_msc]
    labels = ['train', 'new', 'msc']

    # actually building the joint data set
    ds = pd.concat(data_sets, keys=labels)

    # returning the final data set
    return ds
