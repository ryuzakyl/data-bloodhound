#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, February 2017

"""Demos for clustering validation indexes

Todo:
    * Module TODOs here!!!
    * You have to also use ``sphinx.ext.todo`` extension

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import sklearn.metrics as skl_metrics
from sklearn import manifold
from sklearn import cluster

from measures import measure_to_function as d_to_f

from clustering.validation.davies_bouldin_index import davies_bouldin

# ----------------------------------------


def clustering_silhouette_analysis(X, y, measure):
    """Silhouette Analysis for clustering results.

    Args:
        X (np.ndarray): The data array.
        y (np.ndarray): The data labels.
        measure (int): The type of dissimilarity to use as metric (see 'measures' module).

    Note:
        Idea taken from:
        http://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html#sphx-glr-auto-examples-cluster-plot-kmeans-silhouette-analysis-py

        Silhouette analysis can be used to study the separation distance
        between the resulting clusters. The silhouette plot displays a
        measure of how close each point in one cluster is to points in the
        neighboring clusters and thus provides a way to assess parameters
        like number of clusters visually. This measure has a range of
        [-1, 1].

        Silhouette coefficients (as these values are referred to as) near
        +1 indicate that the sample is far away from the neighboring
        clusters. A value of 0 indicates that the sample is on or very
        close to the decision boundary between two neighboring clusters
        and negative values indicate that those samples might have been
        assigned to the wrong cluster.

    """

    # validating 'data' and 'labels'
    if not isinstance(X, np.ndarray) or not isinstance(y, np.ndarray):
        raise ValueError('Verify data and labels.')

    # validating consistency between samples and labels
    if X.shape[0] != y.shape[0]:
        raise ValueError('Amount of samples must be the same as the amount of labels.')

    # the specified metric must be one of the implemented measures
    if measure not in d_to_f:
        raise ValueError('Unknown dissimilarity measure.')

    # getting the metric function
    d = d_to_f[measure]

    # computing the silhouette scores for each sample
    sil_per_sample = skl_metrics.silhouette_samples(X, y, metric=d)

    # average of silhouette score of all samples
    sil_avg = sil_per_sample.mean()

    # getting amount of clusters
    y_set = sorted(set(y))
    n_clusters = len(y_set)

    # configuring drawing parameters
    fig, (ax1, ax2) = plt.subplots(1, 2)     # create a subplot with 1 row and 2 columns
    fig.set_size_inches(18, 7)

    # The 1st subplot is the silhouette plot
    # The silhouette coefficient can range from -1, 1 but in this example all
    # lie within [-0.1, 1]
    ax1.set_xlim([-1, 1])
    # The (n_clusters+1)*10 is for inserting blank space between silhouette
    # plots of individual clusters, to demarcate them clearly.
    ax1.set_ylim([0, len(X) + (n_clusters + 1) * 10])

    y_lower = 10

    # for each cluster
    for i in y_set:
        # getting silhouette score from samples belonging to cluster i
        sil_per_cluster = sil_per_sample[y == i]

        # sorting silhouette score values
        sil_per_cluster.sort()

        cluster_size = sil_per_cluster.shape[0]
        y_upper = y_lower + cluster_size

        color = cm.spectral(float(i) / n_clusters)
        ax1.fill_betweenx(np.arange(y_lower, y_upper),
                          0, sil_per_cluster,
                          facecolor=color, edgecolor=color, alpha=0.7)

        # Label the silhouette plots with their cluster numbers at the middle
        ax1.text(-0.05, y_lower + 0.5 * cluster_size, str(i))

        # Compute the new y_lower for next plot
        y_lower = y_upper + 10  # 10 for the 0 samples

    ax1.set_title("The silhouette plot for the various clusters.")
    ax1.set_xlabel("The silhouette coefficient values")
    ax1.set_ylabel("Cluster label")

    # The vertical line for average silhouette score of all the values
    ax1.axvline(x=sil_avg, color="red", linestyle="--")

    ax1.set_yticks([])  # Clear the yaxis labels / ticks
    ax1.set_xticks([-1, -0.8, -0.5, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1])

    # 2nd Plot showing the actual clusters formed
    colors = cm.spectral(y.astype(float) / n_clusters)

    # t-SNE embedding in 2-dimensional space
    tsne = manifold.TSNE(n_components=2, init='pca', random_state=0)
    tsne_data = tsne.fit_transform(X)

    # scatter plot of data in underlying 2-dimensional space
    ax2.scatter(tsne_data[:, 0], tsne_data[:, 1], marker='.', s=30, lw=0, alpha=0.7, c=colors)

    # getting centroids of clusters
    centers_list = [
        np.mean(tsne_data[y == label], axis=0)
        for label in y_set
    ]
    centers = np.array(centers_list)

    # draw white circles at cluster centers
    ax2.scatter(centers[:, 0], centers[:, 1], marker='o', c="white", alpha=1, s=200)

    for i, c in zip(y_set, centers):
        ax2.scatter(c[0], c[1], marker='$%d$' % i, alpha=1, s=50)

    ax2.set_title('Clustered data visualization')
    ax2.set_xlabel('1st feature (t-SNE embedded space)')
    ax2.set_ylabel('2nd feature (t-SNE embedded space)')

    plt.suptitle(("Silhouette analysis for clustered data "
                  "with n_clusters = %d" % n_clusters),
                 fontsize=14, fontweight='bold')

    # showing the plot
    plt.show()


def clustering_davies_bouldin_analysis(X, y, measure):
    # validating 'data' and 'labels'
    if not isinstance(X, np.ndarray) or not isinstance(y, np.ndarray):
        raise ValueError('Verify data and labels.')

    # validating consistency between samples and labels
    if X.shape[0] != y.shape[0]:
        raise ValueError('Amount of samples must be the same as the amount of labels.')

    # the specified metric must be one of the implemented measures
    if measure not in d_to_f:
        raise ValueError('Unknown dissimilarity measure.')

    # list of davies bouldin indexes
    db_values = []

    # clustering with k-means for several k values
    k_potential = int(X.shape[0] / 4)
    k_max = 10 if k_potential > 10 else k_potential
    x_data = range(2, k_max)
    for k in x_data:
        kmeans = cluster.KMeans(n_clusters=k).fit(X)
        k_labels = kmeans.labels_

        print('Performed clustering with k={} clusters'.format(k))

        # adding the currently computed davies bouldin index
        db_values += [davies_bouldin(X, k_labels, measure)]

    # plotting the results
    db_values_arr = np.array(db_values)
    db_mean = np.mean(db_values_arr)
    x_data_arr = np.array(x_data)

    # applying red color mask
    r_mask = db_values_arr <= db_mean
    plt.bar(x_data_arr[r_mask], db_values_arr[r_mask], color='red')

    # applying green color mask
    g_mask = db_values_arr > db_mean
    plt.bar(x_data_arr[g_mask], db_values_arr[g_mask], color='green')

    # plotting davies bouldin mean value
    plt.axhline(db_mean, color='b', linestyle='dashed', linewidth=2)

    plt.title('The Davies Boulding index plot for several partitions')
    plt.xlabel('Cluster count')
    plt.ylabel('The Davies Boulding index value')

    print('Mean Davis-Bouldin value is: {}'.format(db_mean))

    plt.show()
