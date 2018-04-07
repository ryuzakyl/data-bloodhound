#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, February 2017

import pylab
from datasets.ir_wines import load_ir_wines

# ---------------------------------------------------------------


def plot_ir_wines_data_set():
    # loading the 'ir_wines' data set
    ds = load_ir_wines()

    # excluding class labels
    ds_reduced = ds.iloc[:, :-1]

    ds_reduced.T.plot(legend=None)
    pylab.show()


def plot_ir_wines_of_origin_argentina():
    # loading the 'ir_wines' data set
    ds = load_ir_wines()

    # getting samples taken in Argentina
    ds_argentina = ds.loc[ds['origin'] == 1]

    # excluding class labels
    ds_argentina_data = ds_argentina.iloc[:, :-1]

    ds_argentina_data.T.plot()
    pylab.show()
