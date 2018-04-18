#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, July 2017

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

import numpy as np

# ---------------------------------------------------------------

# common path for shared library
__shared_lib_path = "{}/cpp-dcomb/cmake-build-debug/".format(os.path.split(__file__)[0])
lib_name = 'lib_cpp_dcomb'

win32_lib_ext = '.dll'
posix_lib_ext = '.so'

# linux os support
if os.name == 'posix' and sys.platform.startswith('linux'):
    try:
        __dcomb_lib_path = "{}{}{}".format(__shared_lib_path, lib_name, posix_lib_ext)
        __dcomb_lib = cdll.LoadLibrary(__dcomb_lib_path)
    except:
        raise ImportError('Error while loading Dcomb shared library.')

# windows os support
elif os.name == 'nt':
    try:
        __dcomb_lib_path = "{}{}{}".format(__shared_lib_path, lib_name, win32_lib_ext)
        __dcomb_lib = cdll.LoadLibrary(__dcomb_lib_path)
    except:
        raise ImportError('Error while loading Dcomb shared library.')

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


# handle to 'dnom' function in the *.so library
__dnom = c_func(
    'dnom', __dcomb_lib, c_double,

    # 'x' vector
    ('x', c_double_p, 1),  # double* x

    # 'y' vector
    ('y', c_double_p, 1),  # double* y

    # vectors count
    ('count', c_int, 1),  # int count
)

# handle to 'dord' function in the *.so library
__dord = c_func(
    'dord', __dcomb_lib, c_double,

    # 'x' vector
    ('x', c_double_p, 1),  # double* x

    # 'y' vector
    ('y', c_double_p, 1),  # double* y

    # vectors count
    ('count', c_int, 1),  # int count
)

# ---------------------------------------------------------------

def dnom(x, y):
    if len(x) != len(y):
        raise ValueError('Vectors must have the same size.')

    # convert to list
    x = x.tolist() if isinstance(x, np.ndarray) else x
    y = y.tolist() if isinstance(y, np.ndarray) else y

    # building params
    count = len(x)
    x_arr = c_array(c_double, count, x)
    y_arr = c_array(c_double, count, y)

    # function call to 'dnom' in C
    d = __dnom(x_arr, y_arr, count)

    return d

def dord(x, y):
    if len(x) != len(y):
        raise ValueError('Vectors must have the same size.')

    # convert to list
    x = x.tolist() if isinstance(x, np.ndarray) else x
    y = y.tolist() if isinstance(y, np.ndarray) else y

    # building params
    count = len(x)
    x_arr = c_array(c_double, count, x)
    y_arr = c_array(c_double, count, y)

    # function call to 'dord' in C
    d = __dord(x_arr, y_arr, count)

    return d
