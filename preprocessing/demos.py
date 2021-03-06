#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, March 2017

import pylab

import pandas as pd

from datasets.raman_tablets import load_raman_tablets
from datasets.nir_tablets import load_nir_tablets
from datasets.nmr_onion import load_nmr_onion

from preprocessing.snv import snv_norm
from preprocessing.savitzky_golay import savitsky_golay_smoothing as sav_gol
from preprocessing.moving_average import mov_avg_2d
from preprocessing.msc import mscorr
from preprocessing.msc import mscorr_linreg

# ---------------------------------------------------------------


def plot_raman_tablets_data_after_snv():
    # loading the raman tablets data set
    ds = load_raman_tablets()

    # removing columns associated with classes and properties
    ds = ds.iloc[:, :-2]

    # creating the figure and adding subplots
    n_rows, n_cols = 1, 2
    fig, axes = pylab.subplots(nrows=n_rows, ncols=n_cols)

    axes[0].set_title('Raman Tablets')
    ds.T.plot(ax=axes[0], legend=None)

    axes[1].set_title('Raman Tablets (SNV)')
    ds_prep = pd.DataFrame(snv_norm(ds.values), index=ds.index, columns=ds.columns)
    ds_prep.T.plot(ax=axes[1], legend=None)

    pylab.show()


def plot_nir_tablets_data_after_savitsky_golay():
    # loading the nir tablets data set
    ds = load_nir_tablets()

    # removing columns associated with classes and properties
    ds = ds.iloc[:, :-2]

    # creating the figure and adding subplots
    n_rows, n_cols = 1, 2
    fig, axes = pylab.subplots(nrows=n_rows, ncols=n_cols)

    axes[0].set_title('NIR Tablets')
    ds.T.plot(ax=axes[0], legend=None)

    axes[1].set_title('NIR Tablets (Savitsky-Golay)')
    ds_prep = pd.DataFrame(sav_gol(ds.values, width=7, order=5, deriv=0), index=ds.index, columns=ds.columns)
    ds_prep.T.plot(ax=axes[1], legend=None)

    pylab.show()


def plot_nmr_onion_data_after_moving_average():
    # loading the nmr onion data set
    ds = load_nmr_onion()

    # removing columns associated with classes and properties
    ds = ds.iloc[:, :-1]

    # creating the figure and adding subplots
    n_rows, n_cols = 1, 2
    fig, axes = pylab.subplots(nrows=n_rows, ncols=n_cols)

    axes[0].set_title('NMR Onion')
    ds.T.plot(ax=axes[0], legend=None)

    axes[1].set_title('NMR Onion (Moving Average)')
    ds_prep = pd.DataFrame(mov_avg_2d(ds.values, window_len=51), index=ds.index, columns=ds.columns)


    ds_prep.T.plot(ax=axes[1], legend=None)

    pylab.show()


def plot_nir_tablets_data_after_msc():
    # loading the nir tablets data set
    ds = load_nir_tablets()

    # removing columns associated with classes and properties
    ds = ds.iloc[:, :-3]

    # creating the figure and adding subplots
    n_rows, n_cols = 1, 2
    fig, axes = pylab.subplots(nrows=n_rows, ncols=n_cols)

    axes[0].set_title('NIR Tablets')
    ds.T.plot(ax=axes[0], legend=None)

    axes[1].set_title('NIR Tablets (MSC)')
    # ds_prep = pd.DataFrame(mscorr_linreg(ds.values, 'bestcorr'), index=ds.index, columns=ds.columns)
    ds_prep = pd.DataFrame(mscorr(ds.values, 'mean'), index=ds.index, columns=ds.columns)
    ds_prep.T.plot(ax=axes[1], legend=None)

    pylab.show()


def plot_nir_tablets_data_after_msc_linreg():
    # loading the nir tablets data set
    ds = load_nir_tablets()

    # removing columns associated with classes and properties
    ds = ds.iloc[:, :-3]

    # creating the figure and adding subplots
    n_rows, n_cols = 1, 2
    fig, axes = pylab.subplots(nrows=n_rows, ncols=n_cols)

    axes[0].set_title('NIR Tablets')
    ds.T.plot(ax=axes[0], legend=None)

    axes[1].set_title('NIR Tablets (MSC)')
    # ds_prep = pd.DataFrame(mscorr_linreg(ds.values, 'bestcorr'), index=ds.index, columns=ds.columns)
    ds_prep = pd.DataFrame(mscorr_linreg(ds.values, 'mean'), index=ds.index, columns=ds.columns)
    ds_prep.T.plot(ax=axes[1], legend=None)

    pylab.show()
