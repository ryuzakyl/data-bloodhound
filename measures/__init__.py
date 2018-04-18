#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, August 2016

from .euclidean_distance import euclidean
from .manhattan_distance import manhattan
from .minkowski_distance import minkowski

from .shape_dissimilarity import dshape as shape_hy
from .shape_dissimilarity import shape_measure as shape_py

from .correlation_coefficient import probabilistic_correlation as prob_correlation
from .correlation_coefficient import dis_correlation_scipy
from .pearson_coefficient import probabilistic_pearsonr as prob_pearson
from .pearson_coefficient import dis_pearsonr as dis_pearson
from .spearman_coefficient import probabilistic_spearmanr as prob_spearman
from .spearman_coefficient import dis_spearmanr as dis_spearman

from .cosine_distance import cosine
from .spectral_angle_mapper import sam
from .pearson_coefficient import dissimilarity_pcc as pcc

from .kolmogorov_smirnov import dkolmogorov as kolmogorov
from .bray_curtis import dis_bray_curtis as bray_curtis
from .chi_squared import X2

from .andrew_curves import dis_andrews_curves
from .corr_shape_dissimilarity import corr_dshape as corr_shape_hy
from .corr_shape_dissimilarity import corr_shape_measure as corr_shape_py
from .dcomb import dnom, dord

# ------------------------------------------------------

# minkowski family
EUCLIDEAN = 0
MANHATTAN = 1
MINKOWSKI = 2

# shape measures
SHAPE_HY = 3
SHAPE_PY = 4

# correlation based measures
CORRELATION = 5
PEARSON = 6
SPEARMAN = 7

# angle based measures
PCC = 8
COSINE = 9
SAM = 10

# probability distribution based dissimilarities
KOLMOGOROV = 11
BRAY_CURTIS = 12
CHI_SQUARED = 13

# other measures
ANDREW_CURVES = 14
CORR_SHAPE_HY = 15
CORR_SHAPE_PY = 16
DNOM = 17
DORD = 18

# ---------------

# list of measures implemented
measures_list = [
    # distances for vector spaces
    EUCLIDEAN,
    MANHATTAN,
    MINKOWSKI,

    # shape measures
    SHAPE_HY,
    SHAPE_PY,

    # correlation based measures
    CORRELATION,
    PEARSON,
    SPEARMAN,

    # angle based measures
    PCC,
    COSINE,
    SAM,

    # probability distribution based dissimilarities
    KOLMOGOROV,
    BRAY_CURTIS,
    CHI_SQUARED,

    # other measures
    ANDREW_CURVES,
    CORR_SHAPE_HY,
    CORR_SHAPE_PY,
    DNOM,
    DORD,
]

# ---------------

# map of measure id and the corresponding callable
measure_to_function = {
    EUCLIDEAN:      euclidean,
    SHAPE_HY:       shape_hy,
    SHAPE_PY:       shape_py,
    MANHATTAN:      manhattan,
    CORRELATION:    dis_correlation_scipy,
    COSINE:         cosine,
    PEARSON:        dis_pearson,
    PCC:            pcc,
    SPEARMAN:       dis_spearman,
    SAM:            sam,
    MINKOWSKI:      minkowski,
    KOLMOGOROV:     kolmogorov,
    BRAY_CURTIS:    bray_curtis,
    CHI_SQUARED:    X2,
    ANDREW_CURVES:  lambda x, y: dis_andrews_curves(x, y, SHAPE_PY),
    CORR_SHAPE_HY:  corr_shape_hy,
    CORR_SHAPE_PY:  corr_shape_py,
    DNOM:           dnom,
    DORD:           dord,
}

# ---------------

# map of measure id and measure name
measures_names = {
    EUCLIDEAN:      'Euc',
    SHAPE_HY:       'SHy',
    SHAPE_PY:       'SPy',
    MANHATTAN:      'Man',
    CORRELATION:    'Cor',
    COSINE:         'Cos',
    PEARSON:        'Pea',
    PCC:            'PCC',
    SPEARMAN:       'Spe',
    SAM:            'SAM',
    MINKOWSKI:      'Min',
    KOLMOGOROV:     'Kol',
    BRAY_CURTIS:    'Bra',
    CHI_SQUARED:    'Chi',
    ANDREW_CURVES:  'And',
    CORR_SHAPE_HY:  'CSH',
    CORR_SHAPE_PY:  'CSP',
    DNOM:           'DNM',
    DORD:           'DOR',
}
