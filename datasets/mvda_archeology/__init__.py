#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, March 2017

import os

import pandas as pd

import utils.datasets as utils

# ---------------------------------------------------------------

# data set paths
__data_set_path = "{}/data/arch.xlsx".format(os.path.split(__file__)[0])

__pickle_path = "{}/cache/mvda_arch.pickle".format(os.path.split(__file__)[0])

# ---------------------------------------------------------------

# TODO: Add docstring with usage examples (see 'uv_fuel' data set)


@utils.load_data_from_pickle(__pickle_path)
def load_mvda_archeology():
    """Loads the MVDA Archeology data set.

    Returns:
        A Pandas DataFrame with all the data set info.

    Examples:
        >>> ds = load_mvda_archeology()
        >>> ds['train'].shape
        (63, 11)
        >>> ds['validate'].shape
        (12, 11)

    """

    # loading the data set using pandas
    arch_ds = pd.read_excel(__data_set_path)

    # getting the training data set
    train_arch_ds = arch_ds.iloc[:63, :]

    # getting the validate data set
    validate_arch_ds = arch_ds.iloc[63:, :]

    # 'building' the final data set
    ds = {
        'train':    train_arch_ds,
        'validate': validate_arch_ds
    }

    # returning the loaded data set
    return ds
