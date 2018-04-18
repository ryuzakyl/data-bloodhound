#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, September 2016

import numpy as np
import random as rnd


def random_selection_from_lists(data, k):
    # validating data
    if data is None or not isinstance(data, list):
        raise ValueError('Data must be valid')

    # all samples must have the same size
    len_d_first = len(data[0]) if data else None
    if not all(isinstance(d, list) for d in data) or not all(len(d) == len_d_first for d in data):
        raise ValueError('Data must be a list of lists of the same size')

    # converting to ndarrays
    data_arr = np.array(data, float)

    return random_selection_from_arrays(data_arr, k)


def random_selection_from_arrays(data, k):
    # validating data
    if data is None or not isinstance(data, np.ndarray):
        raise ValueError('Data must be valid')

    # getting amount of samples
    data_count = data.shape[0]

    # selecting k indexes in a random manner
    return rnd.sample(range(data_count), k)
