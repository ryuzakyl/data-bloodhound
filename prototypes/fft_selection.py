#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, September 2016

import random as rnd
import numpy as np


def fft_selection_from_lists(data, k, d):
    # validating data
    if data is None or not isinstance(data, list):
        raise ValueError('Data must be valid')

    # all samples must have the same size
    len_d_first = len(data[0]) if data else None
    if not all(isinstance(d, list) for d in data) or not all(len(d) == len_d_first for d in data):
        raise ValueError('Data must be a list of lists of the same size')

    # converting to ndarrays
    data_arr = np.array(data, float)

    return fft_selection_from_arrays(data_arr, k, d)


def fft_selection_from_arrays(data, k, d):
    # validating data
    if data is None or not isinstance(data, np.ndarray):
        raise ValueError('Data must be valid')

    # getting amount of samples
    data_count = data.shape[0]

    # list of prototypes selected
    protos = list()
    protos_idxs = list()

    # selecting a random sample as a first prototype
    p_idx = rnd.randint(0, data_count - 1)
    protos.append(data[p_idx, :])
    protos_idxs.append(p_idx)

    # k-1 times (select a prototype)
    for i in range(k-1):
        min_dis_prot = list()

        # for each sample in data
        for j, sj in enumerate(data):
            # ignoring samples already selected as prototypes
            if j in protos_idxs:
                continue

            # computing minimum distance of each sample to all prototypes
            d_to_ps = [min(map(lambda p: d(p, sj), protos))]

            # getting index sample with max (minimum distance) to all prototypes
            _, min_dis = min(enumerate(d_to_ps), key=lambda t: t[1])

            # appending minimum distance of sj to all prototypes
            min_dis_prot.append((j, min_dis))

        # getting sample with max (min distance) to all prototypes
        j_best, _ = max(min_dis_prot, key=lambda t: t[1])

        # storing current selected prototype
        protos.append(data[j_best, :])
        protos_idxs.append(j_best)

    return protos_idxs
