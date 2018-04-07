#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, May 2017

import numpy as np
from scipy.spatial.distance import pdist, squareform

from measures.similarity import to_similarity as to_sim

from prototypes.entropy.sort_by_entropy import sort_by_entropy

# ---------------------------------------------------------------

LEFT_VERTEX_SELECTION = 0
LOCAL_MAXIMUM_SELECTION = 1
ONE_SHOT_POSITIVES_SELECTION = 2
ONE_SHOT_THRESHOLD_SELECTION = 3
BEST_25_PERCENT = 4
BEST_50_PERCENT = 5
BEST_75_PERCENT = 6

selection_strategy_to_function = {
    LEFT_VERTEX_SELECTION:          lambda s: left_from_vertex_selection(s),
    LOCAL_MAXIMUM_SELECTION:        lambda s: local_maximum_selection(s),
    ONE_SHOT_POSITIVES_SELECTION:   lambda s: one_shot_selection(s),
    ONE_SHOT_THRESHOLD_SELECTION:   lambda s: one_shot_selection(s, thres=0.1),
    BEST_25_PERCENT:                   lambda s: best_percent(s, perc=25),
    BEST_50_PERCENT:                   lambda s: best_percent(s, perc=50),
    BEST_75_PERCENT:                   lambda s: best_percent(s, perc=75),
}

# ---------------

# map of strategy id and strategy name
selection_strategies_names = {
    LEFT_VERTEX_SELECTION:          'LFT_VTX',
    LOCAL_MAXIMUM_SELECTION:        'LOC_MAX',
    ONE_SHOT_POSITIVES_SELECTION:   'OSH_POS',
    ONE_SHOT_THRESHOLD_SELECTION:   'OSH_THR',
    BEST_25_PERCENT:                'BST_25P',
    BEST_50_PERCENT:                'BST_50P',
    BEST_75_PERCENT:                'BST_75P',
}

# ---------------------------------------------------------------


def order_templates(gk, s):
    """Orders templates in a gallery using entropy value as a criterion

    Args:
        gk (ndarray): The similarity matrix of the gallery.
        s (callable): Similarity function to compare samples in gallery

    Returns:
        (idx, entropy) Sample index and entropy value from more important to less important

    Examples:
        >>> import measures
        >>> from measures.similarity import to_similarity as to_sim
        >>> s = to_sim(measures.EUCLIDEAN)
        >>> gk = np.arange(1, 51).reshape((5, 10))
        >>> order_templates(gk, s)
        [(0, 0.15915271770635764), (1, 0.08551326768452594), (2, 0.70773126312284951), (3, 0.0)]
        >>> s = to_sim(measures.MANHATTAN)
        >>> gk = np.arange(1, 10).reshape((3, 3))
        >>> order_templates(gk, s)
        [(0, 0.96840510364912347), (1, 0.0)]

    """

    # validating 'comparisons' and 'labels'
    if not isinstance(gk, np.ndarray):
        raise ValueError('Verify comparisons and labels.')

    # computing a similarity matrix
    dm = squareform(pdist(gk, metric=s))

    # sorting gallery samples by entropy value
    pivots, entropy_values = sort_by_entropy(dm, 0)

    return list(zip(pivots, entropy_values))

# ---------------------------------------------------------------


def ent_sel_from_df(df, labels_col, measure, percent):
    # selected templates given an entropy criterion
    idxs_sel = list()

    # getting a similarity function from the given dissimilarity
    sim = to_sim(measure)

    # performing entropy-based template selection for each group
    for gid, g in df.groupby(labels_col):
        # ordering templates
        g_ordered = [(0, 0.0)] if len(g) < 2 else order_templates(g.values[:, :-1], s=sim)

        # getting selected templates
        selection = best_percent(g_ordered, percent)

        # taking at least two instances
        if not len(selection):
            idxs = [0, 1]

        # adding another instance
        elif len(selection) == 1:
            # selecting also template to the right (in a circular manner)
            idxs = [selection[0], (selection[0] + 1) % g.shape[0]]

        else:
            idxs = [idx for idx in selection]

        # adding selected samples in this group
        idxs_sel += g.index[idxs].tolist()

    # returning the selected indexes
    return idxs_sel


def cluster_template_selection(cluster_id, cluster_dict, sim_type, sel_type):
    # getting the cluster samples
    cluster_dataset = cluster_dict[cluster_id]

    # applying template selection by means of entropy
    sim = to_sim(sim_type)
    data = [t[1] for t in cluster_dataset]
    ordered = order_templates(data, s=sim)

    # # showing parable
    # f_values = [v for _, v in ordered]
    # plot_entropy_and_parable(f_values, y_min=0, y_max=1)

    # getting selected templates
    selection_strategy = selection_strategy_to_function[sel_type]
    selection = selection_strategy(ordered)
    # idxs_selection = [t[0] for t in selection] if len(selection) else [0]
    idxs_selection = [idx for idx in selection] if len(selection) else [0]

    # returning the sample if selected
    return [(x[0], cluster_id, x[1]) for i, x in enumerate(cluster_dataset) if i in idxs_selection]


def perform_template_selection(cluster_dict, sim_type, sel_type):
    # selections for each cluster
    result = list()

    # template selection for each cluster
    for cluster_id in cluster_dict.keys():
        result += cluster_template_selection(cluster_id, cluster_dict, sim_type, sel_type)

    # returning the result
    return result


def left_from_vertex_selection(selection):
    # getting the data for fitting
    x = [i + 1 for i in range(len(selection))]
    y = [f_value for _, f_value in selection]

    # fitting a second order polynomial (i.e. parable)
    a, b, c = fit_parable_1d(np.array(x), np.array(y))

    # computing the 'abscissa' of the fitted parable vertex
    x_vertex = -1.0 * b / (2 * a)

    # choosing templates on the left side of parable vertex (i + 1 because data starts at 1 and not 0)
    return [i for i, _ in enumerate(selection) if i + 1 <= x_vertex]


def local_maximum_selection(selection):
    # declaring the resulting list
    result = []

    # whether the elements line is growing or not
    growing = True

    # for each template in the given order
    for i in range(1, len(selection)):
        # an abate was detected (there is a max at index i-1)
        if selection[i][1] < selection[i-1][1]:
            if growing:
                result.append(i-1)

            # curve not growing anymore
            growing = False

        # a growth was detected
        else:
            # curve is growing
            growing = True

    # returning the local maximum points
    return result


def one_shot_selection(selection, thres=0.0):
    # adding an initial fake element
    sel = [selection[0]] + selection

    # declaring the list for the new fitness
    new_fit = [(i - 1, sel[i][1] - sel[i-1][1]) for i in range(1, len(sel))]

    # keeping values with fitness value greater than thres
    fit_gt_thres = filter(lambda t: t[1] > thres, new_fit)

    # returning simply the selected indexes
    return [idx for idx, _ in fit_gt_thres]


def best_percent(selection, perc=50):
    # validating percent
    if perc < 0 or perc > 100:
        raise ValueError('Invalid percent value.')

    # computing upper bound index
    ub_idx = int((perc / 100.0) * len(selection))
    ub_idx = max(1, ub_idx)

    # adding an initial fake element
    sel = [selection[0]] + selection

    # declaring the list for the new fitness
    new_fit = [(i - 1, sel[i][1] - sel[i - 1][1]) for i in range(1, len(sel))]

    # sorting by new fitness
    new_fit.sort(key=lambda x: x[1], reverse=True)

    fit_gt_idx = new_fit[0: ub_idx]

    # returning simply the selected indexes
    return [idx for idx, _ in fit_gt_idx]

# -----------------------------------------------------


def fit_parable_1d_array(x, y):
    # x and y must be ndarrays
    if not isinstance(x, np.ndarray) or not isinstance(y, np.ndarray):
        raise Exception('Both parameters must be n-dimensional arrays')

    # x and y must have shape (n,)
    if len(x.shape) != 1 or len(y.shape) != 1:
        raise Exception('Both parameters must have a single dimension')

    # x and y must have the same shape
    if x.shape != y.shape:
        raise Exception('Both parameters must have the same dimension')

    # fitting a parable (degree 2)
    return np.polyfit(x, y, 2)


def fit_parable_1d(x, y):
    # fitting the parable and getting the ndarray of coefficients
    coefs = fit_parable_1d_array(x, y)

    # returning the fitted coefficients a, b and c
    return coefs[0], coefs[1], coefs[2]
