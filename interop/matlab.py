#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, August 20

import datetime
import numpy as np
import scipy.io as sio


def to_matlab_matrix(file_path, arr, matrix_name='m'):
    # attempting to save the numpy array as a MATLAB matrix
    try:
        # appending .mat extension if needed
        file_path = file_path if file_path.endswith('.mat') else '{}.mat'.format(file_path)

        # data dictionary
        d = {
            matrix_name: arr,
            '__version__': '1.0',
            '__header__': 'MATLAB 5.0 MAT-file, Platform: PCWIN64, Created on: {}'.format(datetime.datetime.now()),
            '__globals__': []
        }

        # saving as MATLAB file
        sio.savemat(file_path, d)

        # all good
        return True

    # case of io exception
    except IOError:
        # error saving the file
        return False


def from_matlab_matrix(file_path):
    # loading .mat file
    mat_contents = sio.loadmat(file_path)

    # for each key data in matlab matrix
    for k in mat_contents.keys():
        # not interested in private matlab generated attributes
        if k.startswith('__'):
            continue

        # returning numpy array
        if isinstance(mat_contents[k], np.ndarray):
            return mat_contents[k].astype(str)

    return None


def generate_data_for_matlab_cross_validation(folder_path, selection_data):
    # getting the samples names and writing them to file
    s_names = [name for name, _, _ in selection_data]
    names_arr = np.array(s_names)
    to_matlab_matrix('{}/names.mat'.format(folder_path), names_arr, matrix_name='names')

    # getting the samples classes and writing them to file
    s_classes = [c for _, c, _ in selection_data]
    classes_arr = np.array(s_classes)
    to_matlab_matrix('{}/classes.mat'.format(folder_path), classes_arr, matrix_name='classes')

    # getting the samples data and writing them to file
    s_data = [data for _, _, data in selection_data]
    data_arr = np.array(s_data)
    to_matlab_matrix('{}/data.mat'.format(folder_path), data_arr, matrix_name='data')
