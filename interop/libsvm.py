#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, July 2017

import numpy as np

# ---------------------------------------------------------------


def dataframe_to_libsvm_data(file_path, df, class_column):
    """Dunn-index for clustering validation in a dissimilarity space.

    Args:
        file_path (string): File to save train data in.
        df (pd.DataFrame): Dataframe with training information.
        class_column (object): Column with class label information.

    Returns:
        Saves data to train SVM classifier via ``libsvm`` `svm-train` tool to the file specified

    Notes:
        * Use for interacting with the ``libsvm`` `svm-train` tool.

    Examples:
        >>> import os
        >>> from datasets.meb_explosives import load_meb_explosives
        >>> df = load_meb_explosives()

        # saving training data to specified file
        >>> dataframe_to_libsvm_data(os.path.abspath('./output/svm_train_data'), df, 'class')

    """

    # making a copy of the data frame
    df_cpy = df.copy()

    # getting class labels
    y = df_cpy[class_column]
    y_unique = np.unique(y)
    y_map = {c: i for i, c in enumerate(y_unique)}

    # getting data
    del df_cpy[class_column]
    X = df_cpy.values

    # building lines to write to file
    lines = [
        '{} {}\n'.format(y_map[c], ' '.join(['{}:{}'.format(i + 1, x) for i, x in enumerate(row)]))
        for c, row in zip(y, X)
    ]

    # writing data to file
    with open(file_path, 'w') as f:
        f.writelines(lines)
