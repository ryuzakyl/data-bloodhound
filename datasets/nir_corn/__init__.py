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
__data_set_path = "{}/data/corn.mat".format(os.path.split(__file__)[0])

__pickle_path = "{}/cache/nir_corn.pickle".format(os.path.split(__file__)[0])

# ---------------------------------------------------------------


# TODO: Add docstring with usage examples (see 'uv_fuel' data set)

@utils.load_data_from_pickle(__pickle_path)
def load_nir_corn():
    """Loads the NIR Corn data set.

    Returns:
        A dictionary with all the data set info.

    Examples:
        >>> ds = load_nir_corn()
        >>> ds['m5_nbs'].shape
        (3, 700)
        >>> ds['m5_spec'].shape
        (80, 700)
        >>> ds['mp5_nbs'].shape
        (4, 700)
        >>> ds['mp5_spec'].shape
        (80, 700)
        >>> ds['mp6_nbs'].shape
        (4, 700)
        >>> ds['mp6_spec'].shape
        (80, 700)
        >>> ds['propvals'].shape
        (80, 4)

    """

    # loading matlab data set
    raw_data = sio.loadmat(__data_set_path)

    # building features labels
    features_labels = list(range(1, 701))

    # ---------------- m5 info ----------------

    m5nbs_data = raw_data['m5nbs'][0][0][7]
    m5_nbs_ds = utils.build_data_set(m5nbs_data, list(range(1, m5nbs_data.shape[0] + 1)), features_labels)

    m5spec_data = raw_data['m5spec'][0][0][7]
    m5_spec_ds = utils.build_data_set(m5spec_data, list(range(1, m5spec_data.shape[0] + 1)), features_labels)

    # ---------------- mp5 info ----------------

    mp5nbs_data = raw_data['mp5nbs'][0][0][7]
    mp5_nbs_ds = utils.build_data_set(mp5nbs_data, list(range(1, mp5nbs_data.shape[0] + 1)), features_labels)

    mp5spec_data = raw_data['mp5spec'][0][0][7]
    mp5_spec_ds = utils.build_data_set(mp5spec_data, list(range(1, mp5spec_data.shape[0] + 1)), features_labels)

    # ---------------- mp6 info ----------------

    mp6nbs_data = raw_data['mp6nbs'][0][0][7]
    mp6_nbs_ds = utils.build_data_set(mp6nbs_data, list(range(1, mp6nbs_data.shape[0] + 1)), features_labels)

    mp6spec_data = raw_data['mp6spec'][0][0][7]
    mp6_spec_ds = utils.build_data_set(mp6spec_data, list(range(1, mp6spec_data.shape[0] + 1)), features_labels)

    # ---------------- propvals info ----------------

    prop_values = raw_data['propvals'][0][0][7]
    prop_names = list(map(lambda s: s.strip(), raw_data['propvals'][0][0][8][1][0]))

    propvals_ds = utils.build_data_set(prop_values, list(range(1, prop_values.shape[0] + 1)), prop_names)

    # ----------------

    # actually building the joint data set
    ds = {
        'm5_nbs': m5_nbs_ds,

        'm5_spec': m5_spec_ds,

        'mp5_nbs': mp5_nbs_ds,

        'mp5_spec': mp5_spec_ds,

        'mp6_nbs': mp6_nbs_ds,

        'mp6_spec': mp6_spec_ds,

        'propvals': propvals_ds,
    }

    return ds
