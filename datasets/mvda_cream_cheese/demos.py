#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, January 2017

import pylab

from datasets.mvda_cream_cheese import load_mvda_cream_cheese

# ---------------------------------------------------------------


def plot_mvda_cream_cheese_data_set():
    # loading the mvda cream cheese data set
    ds = load_mvda_cream_cheese()

    # removing columns associated with properties properties
    ds = ds.iloc[:, 6:]

    # plotting the data set
    ds.T.plot(legend=None)
    pylab.show()


def plot_mvda_cream_cheese_p_aroma():
    # loading the mvda cream cheese data set
    ds = load_mvda_cream_cheese()

    product_name = 'P+Aroma'
    product_df = None

    # removing columns associated with properties properties
    for (p_id, df) in ds.groupby('Product name'):
        if p_id == product_name:
            product_df = df
            break

    product_df = product_df.iloc[:, 6:]

    # plotting the data set
    product_df.T.plot()
    pylab.show()
