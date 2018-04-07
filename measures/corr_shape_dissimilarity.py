#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, June 2017

from math import ceil, floor
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d as scipy_gauss1d
from scipy.spatial.distance import correlation

def derfilter(data, sigma=2.0):
    # computing x boundaries
    x_lb = int(floor(-3 * sigma))
    x_ub = int(ceil(3 * sigma)) + 1   # accounting for the upper exclusive boundary in python

    # computing x and g
    x = np.arange(x_lb, x_ub)
    g = np.exp(-0.5 * (x ** 2) / sigma ** 2)    # parenthesis only for clarity

    # computing kernel
    dg = -x * g / sigma ** 2
    kernel = dg

    # computing data and sizes
    sc, fc = data.shape
    kernel_length = kernel.shape[0]
    kc = kernel_length + 10    # amount of columns of kernel

    # output data
    out = np.zeros(data.shape)

    # extend the data by mirroring the tails
    data2 = np.hstack([np.fliplr(data[:, 0:kc]), data, np.fliplr(data[:, -kc:])])

    # size of the convolution output
    outc = fc + 2*kc + kernel_length - 1

    # ind = kc+ceil(length(kernel)/2):outc-kc-floor(length(kernel)/2);
    ind = slice(kc + int(ceil(kernel_length / 2)), outc - kc - int(floor(kernel_length / 2)) + 1)   # +1 because Python excludes upper bound while MATLAB does not

    # TODO: Optimization here!: 1-list comprehension, 2-out=np.vstack(list_comprehension)
    for i in range(sc):
        t = np.convolve(data2[i, :], kernel)
        out[i, :] = t[ind]

    # data convolved with a gaussian kernel
    return out


def corr_dshape(x, y, sigma=2.0):
    # creating a data array from the two samples
    data = np.array([x, y])

    # computing the dissimilarity representation via shape measure
    dr_data = corr_dspec_shape(data, data, sigma)

    # dr_data should have shape (2, 2) and dshape(x, y) = dr_data[0, 1] = dr_data[1, 0]
    return dr_data[0, 1]


def corr_dspec_shape(data, proto, sigma=2.0):
    # validating feature sizes
    if data.shape[1] != proto.shape[1]:
        raise Exception('Both "data" and "prototypes" must have the same feature sizes.')

    # getting samples and prototypes count
    sc = data.shape[0]
    pc = proto.shape[0]

    # resulting dissimilarity representation
    d = np.zeros((sc, pc))

    # derivative filter for both data and prototypes
    data2 = derfilter(data, sigma)
    proto2 = derfilter(proto, sigma)

    # normalizing each row by its maximum value
    data2 = np.apply_along_axis(lambda row: row / row.max(), 1, data2)
    proto2 = np.apply_along_axis(lambda row: row / row.max(), 1, proto2)

    # change here!!!!!!
    # TODO: Optimization here!: 1-list comprehension, 2-out=np.vstack(list_comprehension)
    for i in range(pc):
        t = np.apply_along_axis(lambda row: correlation(row, proto2[i, :]), 1, data2)
        d[:, i] = t

    # the dissimilarity representation
    return d


def corr_shape_measure(x, y, sigma=2.0):
    """Computes the shape dissimilarity value.

    Args:
        x (list): The first vector.
        y (list): The second vector.
        sigma (float): The smoothing parameter

    Returns:
        float: The shape dissimilarity value between vectors x and y.

    """

    # getting the length of the vectors
    x_length = len(x)
    y_length = len(y)

    # validating parameters
    if x_length != y_length:
        raise Exception('Vectors with different sizes')

    # TODO: Here it is assumed that x and y are lists. Analyze the possibility for them to be tuples or numpy arrays

    # converting x and y to numpy arrays
    x_arr = np.array(x, np.float32)
    y_arr = np.array(y, np.float32)

    # applying a first gaussian derivative filter to both
    x_gauss = scipy_gauss1d(x_arr, sigma, order=1)
    y_gauss = scipy_gauss1d(y_arr, sigma, order=1)

    # computing the shape dissimilarity
    return correlation(x_gauss, y_gauss)
