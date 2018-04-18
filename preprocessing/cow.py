#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, March 2017

import os
import sys
from ctypes import (
    cdll,

    # c/c++ types declarations
    POINTER,
    c_int,
    c_double,

    # c/c++ functions declarations
    CFUNCTYPE,
)
import logging as log

import numpy as np

from utils import preprocessing as prep_utils

# ---------------------------------------------------------------

# common path for shared library
__shared_lib_path = "{}/cpp-cow/cmake-build-debug/".format(os.path.split(__file__)[0])
lib_name = 'lib_cpp_cow'

win32_lib_ext = '.dll'
posix_lib_ext = '.so'

# linux os support
if os.name == 'posix' and sys.platform.startswith('linux'):
    try:
        __cow_lib_path = "{}{}{}".format(__shared_lib_path, lib_name, posix_lib_ext)
        __cow_lib = cdll.LoadLibrary(__cow_lib_path)
    except:
        raise ImportError('Error while loading COW shared library.')

# windows os support
elif os.name == 'nt':
    try:
        __cow_lib_path = "{}{}{}".format(__shared_lib_path, lib_name, win32_lib_ext)
        __cow_lib = cdll.LoadLibrary(__cow_lib_path)
    except:
        raise ImportError('Error while loading COW shared library.')

# os not supported
else:
    raise NotImplemented()

# ---------------------------------------------------------------

# additional type declarations
c_int_p = POINTER(c_int)            # c/c++ int* data type
c_double_p = POINTER(c_double)      # c/c++ double* data type


# creates a c_array of type 'c_type' and size 'n' (if l is provided, then it copies the values of l)
def c_array(c_type, n, l=None):
    return (c_type * n)(*l) if l else (c_type * n)()


# allowing c/c++ function prototypes declarations a bit easier
def c_func(lib_func_name, lib_handle, ret_type, *args):
    # types and flags declarations
    a_types = []
    a_flags = []

    # for each argument
    for arg in args:
        a_types.append(arg[1])
        a_flags.append((arg[2], arg[0]) + arg[3:])

    return CFUNCTYPE(ret_type, *a_types)((lib_func_name, lib_handle), tuple(a_flags))


# handle to 'cow_align' function in the *.so library
__c_cow_align = c_func(
    'cow_align', __cow_lib, None,

    # 'v' spectrum related params
    ('v', c_double_p, 1),  # double* v
    ('v_len', c_int, 1),  # int v_len

    # 'v' segments related params
    ('v_segments', c_int_p, 1),  # int* v_segments
    ('v_segs_len', c_int, 1),  # int v_segs_len

    # 'ref' spectrum params
    ('ref', c_double_p, 1),  # double* ref
    ('ref_len', c_int, 1),  # int ref_len

    # 'ref' segments related params
    ('ref_segments', c_int_p, 1),  # int* ref_segments
    ('ref_segs_len', c_int, 1),  # int ref_segs_len

    # slack param
    ('slack', c_int, 1),  # int slack

    # result param
    ('result', c_double_p, 1),  # double* v
)

# ---------------------------------------------------------------


def cow_align_single_auto(v, ref, segs_count, slack):
    # cow manual alignment with:
    # . v_segs=[0] and
    # . ref_segs=[segs_count] (automatic segments of size `segs_count`)
    return cow_align_single_manual(v, [0], ref, [segs_count], slack)


def cow_align_single_manual(v, v_segs, ref, ref_segs, slack):
    """COW alignment of a spectrum and a reference.

    Args:
        v (list, np.ndarray): The spectrum to align.
        v_segs (list, np.ndarray): The segments on the spectrum to align.
        ref (list, np.ndarray): The reference spectrum.
        ref_segs (list, np.ndarray): The segments on the reference spectrum.
        slack (int): Flexibility or tolerance.

    Returns:
        (list, np.ndarray): The spectrum COW aligned.

    Notes:
        * It depends primarly on the reference spectrum and defined segments.

    """

    # converting params to list (if needed)
    v = v.tolist() if isinstance(v, np.ndarray) else v
    v_segs = v_segs.tolist() if isinstance(v_segs, np.ndarray) else v_segs
    ref = ref.tolist() if isinstance(ref, np.ndarray) else ref
    ref_segs = ref_segs.tolist() if isinstance(ref_segs, np.ndarray) else ref_segs

    # size of spectrum and reference must be the same
    if len(v) != len(ref):
        raise ValueError('The vector "v" and the reference "ref" must have the same size.')

    # validating the slack
    if slack <= 1:
        raise ValueError("The slack must be greater than one.")

    # # there must be at least 2 segments (start and end)
    # if len(ref_segs) < 2:
    #     raise ValueError("There must be at least 2 segments (start and end).")

    # segment sizes must match
    if len(v_segs) != len(ref_segs):
        raise ValueError("The same amount of points must be chosen for the reference and the sample.")

    # building 'v' related params
    v_len = len(v)
    v_arr = c_array(c_double, v_len, v)

    # building 'v_segs' related params
    v_segs_len = len(v_segs)
    v_segs_arr = c_array(c_int, v_segs_len, v_segs)

    # building 'ref' related params
    ref_len = len(ref)
    ref_arr = c_array(c_double, ref_len, ref)

    # building 'ref_segs' related params
    ref_segs_len = len(ref_segs)
    ref_segs_arr = c_array(c_int, ref_segs_len, ref_segs)

    # building result param
    result = c_array(c_double, v_len, [0.0] * v_len)

    # function call to 'cow_align' in C
    __c_cow_align(
        # 'v' spectrum params
        v_arr,
        v_len,

        # 'v' segments params
        v_segs_arr,
        v_segs_len,

        # 'ref' spectrum params
        ref_arr,
        ref_len,

        # 'ref' segments related params
        ref_segs_arr,
        ref_segs_len,

        # slack param
        slack,

        # result param
        result,
    )

    # c++ cow implementation failed to align
    if all(x == 0 for x in result):
        log.warning("C++ COW failed to align!!! Returning same spectrum.")
        return v

    # transforming ctypes array into a python list
    v_cow = [result[i] for i in range(v_len)]

    # returning the spectrum v cow aligned
    return v_cow


def cow_align_auto(X, ref, segs_size, slack):
    # 'ref' spectrum has to be determined
    if isinstance(ref, str):
        y = prep_utils.select_ref(ref, X)

    # 'ref' spectrum is provided, either as a 'list' or a 'np.ndarray'
    elif isinstance(ref, np.ndarray) or isinstance(ref, list):
        # converting 'ref' specrtum to ndarray
        y = ref.copy() if isinstance(ref, np.ndarray) else np.array(ref)

        # 'ref' spectrum must have the same size of data
        if y.shape[0] != X.shape[1]:
            raise ValueError('Reference spectrum must have the same dimensions.')

    # invalid 'ref' spectrum provided
    else:
        raise ValueError('Invalid reference spectrum.')

    # automatic alignment of single spectrum for each row of X
    return np.apply_along_axis(
        lambda v: cow_align_single_auto(v, y, segs_size, slack),
        arr = X, axis = 1)
