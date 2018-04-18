#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, February 2017

import measures

from measures.validation.decidability_index import decidability_index_in_dis_space as di_in_dis_space
from measures.validation.kl_divergence import kl_divergence as kl_div
from measures.validation.kl_divergence import kl_divergence_in_dis_space as kl_div_in_dis

from measures.validation.classes_ratio import intra_inter_class_separation_in_dis_space as intra_inter_ratio_in_dis
from measures.validation.silhouette import silhouette_score_from_data

from measures.validation.utils import intra_inter_class_dissimilarities as intra_inter_diss

from datasets.uv_cannabis import load_uv_cannabis

# ---------------------------------------------------------------


def compute_kl_divergence():
    a = {0.2: 10, 0.3: 30, 0.4: 10, 0.5: 10}
    b = {0.5: 10, 0.6: 30, 0.7: 10}

    print(kl_div(a, b))

# ---------------------------------------------------------------


def euclidean_distance_behavior_on_uv_cannabis_data_set():
    # loading the uv cannabis data set
    uv_can = load_uv_cannabis()

    # getting data as a list of lists
    uv_can_data = uv_can.iloc[:, :-1].values

    # getting the class labels
    labels = uv_can['class'].values

    # asserting amount of classes is the same as the amount of data
    assert len(uv_can_data) == len(labels)

    # computing 'intra' e 'inter' class distances
    intra_dists, inter_dists = intra_inter_diss(uv_can_data, labels, measures.EUCLIDEAN)

    print('Euclidean Distance on UV Cannabis data set behavior.')
    print()
    print("Intra-class distances {} comparisons:\r\n{}".format(len(intra_dists), intra_dists))
    print()
    print("Inter-class distances {} comparisons:\r\n{}".format(len(inter_dists), inter_dists))

    import matplotlib.pyplot as plt

    # plotting the histograms
    plt.hist(intra_dists, bins=150, normed=True, color='g', label='Intra-class')
    plt.hist(inter_dists, bins=150, normed=True, color='b', alpha=0.3, label='Inter-class')

    # plot configuration
    plt.title('Euclidean distance on the UV Cannabis data set')
    plt.xlabel('Euclidean distance')
    plt.ylabel('Frequency')
    plt.legend()

    # showing plot
    plt.show()

# ---------------------------------------------------------------


def decidability_index_of_euclidean_distance_on_uv_cannabis():
    # loading the uv cannabis data set
    uv_can = load_uv_cannabis()

    # getting data as a list of lists
    uv_can_data = uv_can.iloc[:, :-1].values

    # getting the class labels
    labels = uv_can['class'].values

    # asserting amount of classes is the same as the amount of data
    assert len(uv_can_data) == len(labels)

    print('Decidability index of Euclidean Distance on UV Cannabis data set:')
    print("d = {}".format(di_in_dis_space(uv_can_data, labels, measures.EUCLIDEAN)))

# ---------------------------------------------------------------


def kl_divergence_of_dshape_on_uv_cannabis():
    # loading the uv cannabis data set
    uv_can = load_uv_cannabis()

    # getting data as a list of lists
    uv_can_data = uv_can.iloc[:, :-1].values

    # getting the class labels
    labels = uv_can['class'].values

    # asserting amount of classes is the same as the amount of data
    assert len(uv_can_data) == len(labels)

    print('KL divergence of DShape Dissimilarity on UV Cannabis data set:')
    print("kl = {}".format(kl_div_in_dis(uv_can_data, labels, measures.SHAPE_PY)))

# ---------------------------------------------------------------


def intra_inter_class_ratio_of_dshape_on_uv_cannabis():
    # loading the uv cannabis data set
    uv_can = load_uv_cannabis()

    # getting data as a list of lists
    uv_can_data = uv_can.iloc[:, :-1].values

    # getting the class labels
    labels = uv_can['class'].values

    # asserting amount of classes is the same as the amount of data
    assert len(uv_can_data) == len(labels)

    print('Intra-inter class ratio of DShape on UV Cannabis data set:')
    print("intra/inter ratio = {}".format(intra_inter_ratio_in_dis(uv_can_data, labels, measures.SHAPE_PY)))

# ---------------------------------------------------------------


def silhouette_with_euclidean_distance_on_uv_cannabis():
    # loading the uv cannabis data set
    uv_can = load_uv_cannabis()

    # getting data as a list of lists
    uv_can_data = uv_can.iloc[:, :-1].values

    # getting the class labels
    classes = uv_can['class'].values

    # asserting amount of classes is the same as the amount of data
    assert len(uv_can_data) == len(classes)

    print('Silhouette score with Euclidean Distance on UV Cannabis data set:')
    print(silhouette_score_from_data(uv_can_data, classes, measures.EUCLIDEAN))
