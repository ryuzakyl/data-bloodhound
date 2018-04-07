#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, December 2016

import os

import pandas as pd

import utils.datasets as utils

# ---------------------------------------------------------------

# data set paths
__data_set_path = "{}/data/mud_data_all.csv".format(os.path.split(__file__)[0])

__pickle_path = "{}/cache/gc_mud.pickle".format(os.path.split(__file__)[0])

# ---------------------------------------------------------------


# TODO: Add docstring with usage examples (see 'uv_fuel' data set)

@utils.load_data_from_pickle(__pickle_path)
def load_gc_mud():
    # loading data set
    mud_ds = pd.read_csv(__data_set_path, sep=',', header=None)     # header=None as no header present in the .csv file

    # returning the mud data set
    return mud_ds
