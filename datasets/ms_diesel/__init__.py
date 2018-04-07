#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, January 2017

import os

import pandas as pd

import utils.datasets as utils

# ---------------------------------------------------------------

# data set paths
__data_set_path = "{}/data/diesel.xlsx".format(os.path.split(__file__)[0])

__pickle_path = "{}/cache/ms_diesel.pickle".format(os.path.split(__file__)[0])

# ---------------------------------------------------------------


# TODO: Add docstring with usage examples (see 'uv_fuel' data set)

@utils.load_data_from_pickle(__pickle_path)
def load_ms_diesel():
    # loading data set
    diesel_ds = pd.read_excel(__data_set_path)

    # returning the diesel data set
    return diesel_ds
