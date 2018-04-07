#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, February 2017

import pylab
from datasets.gc_mud import load_gc_mud

# ---------------------------------------------------------------


def plot_gc_mud_data_set():
    # loading the gc mud data set
    ds = load_gc_mud()

    ds.T.plot(legend=None)
    pylab.show()
