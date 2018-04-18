#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, January 2017

import measures

from datasets.uv_cannabis import load_uv_cannabis

from clustering.validation.demos import clustering_silhouette_analysis
from clustering.validation.demos import clustering_davies_bouldin_analysis

# ---------------------------------------------------------------


def silhouette_analysis_of_uv_cannabis_with_dshape():
    # loading the uv cannabis data set
    uv_can = load_uv_cannabis()

    # getting data as a list of lists
    uv_can_data = uv_can.iloc[:, :-1].values

    # getting the class labels
    classes = uv_can['class'].values

    # asserting amount of classes is the same as the amount of data
    assert len(uv_can_data) == len(classes)

    # performing clustering analysis on UV data with shape measure
    clustering_silhouette_analysis(uv_can_data, classes, measures.SHAPE_PY)


def davies_boulding_analysis_of_uv_cannabis_with_dshape():
    # loading the uv cannabis data set
    uv_can = load_uv_cannabis()

    # getting data as a list of lists
    uv_can_data = uv_can.iloc[:, :-1].values

    # getting the class labels
    classes = uv_can['class'].values

    # asserting amount of classes is the same as the amount of data
    assert len(uv_can_data) == len(classes)

    # performing clustering analysis on UV data with shape measure
    clustering_davies_bouldin_analysis(uv_can_data, classes, measures.SHAPE_PY)
