#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, February 2017

import pylab

from datasets.nir_corn import load_nir_corn

# ---------------------------------------------------------------


def plot_nir_corn_m5spec_data_set():
    # loading the nir corn data set
    ds = load_nir_corn()['m5_spec']

    # plotting the data set
    ds.T.plot(legend=None)
    pylab.show()
