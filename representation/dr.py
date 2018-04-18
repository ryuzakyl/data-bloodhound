#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, August 2016

import numpy as np
import measures


def build_dr_from_lists(data, proto, measure):
    # if unknown measure
    if measure not in measures.measure_to_function:
        raise ValueError('Unknown dissimilarity function.')

    len_d_first = len(data[0]) if data else None
    if not all(isinstance(d, list) for d in data) or not all(len(d) == len_d_first for d in data):
        raise ValueError('Data must be a list of lists of the same size')

    # we are dealing with a list of prototypes indexes from data
    if all(isinstance(i, int) for i in proto):
        # validating prototypes indexes
        if min(proto) < 0 or max(proto) >= len(data):
            raise ValueError('Invalid prototype indexes')

        # setting proto data
        proto_data = [data[idx] for idx in proto]
        proto = proto_data

    len_p_first = len(proto[0]) if proto else None
    if not all(isinstance(p, list) for p in proto) or not all(len(p) == len_p_first for p in proto):
        raise ValueError('Prototypes must be a list of lists of the same size')

    # validating data and prototypes altogether
    if len(data[0]) != len(proto[0]):
        raise ValueError('Data and prototypes must have the same size')

    # converting to ndarrays
    data_arr = np.array(data, float)
    proto_arr = np.array(proto, float)

    return build_dr_from_ndarrays(data_arr, proto_arr, measure)


def build_dr_from_ndarrays(data, proto, measure):
    # if unknown measure
    if measure not in measures.measure_to_function:
        raise ValueError('Unknown dissimilarity function.')

    # we are dealing with a list of prototypes indexes from data
    if all(isinstance(i, int) for i in proto):
        # validating prototypes indexes
        if min(proto) < 0 or max(proto) >= data.shape[0]:
            raise ValueError('Invalid prototype indexes')

        # setting proto data
        proto_data = data[proto]
        proto = proto_data

    # validating data and prototypes altogether
    if data.shape[1] != proto.shape[1]:
        raise ValueError('Data and prototypes must have the same size')

    # building resulting array representation
    dr = np.empty((data.shape[0], proto.shape[0]), float)

    # building dr
    d = measures.measure_to_function[measure]
    for i, p in enumerate(proto):
        # computing dissimilarity of each sample to i-th prototype
        x = np.apply_along_axis(lambda v: d(v, p), axis=1, arr=data)

        # setting i-th feature for each sample
        dr[:, i] = x[:]

    # returning the dissimilarity representation of the data by the prototypes
    return dr
