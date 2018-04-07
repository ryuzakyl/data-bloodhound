#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, May 2017

import pickle
import functools

import pandas as pd

# ---------------------------------------------------------------

MEAS_IDX = 0
CLUS_IDX = 1
CLAS_IDX = 2

DIST_IDX = 0
DF_IDX = 1

# ---------------------------------------------------------------

def merge_data_frames(df_to, df_from):
    # updating any existing columns
    df_to_idxs_set = set(df_to.index)
    df_from_idxs_set = set(df_from.index)

    # updating necessary rows
    idxs_to_update = df_from_idxs_set & df_to_idxs_set
    df_to.loc[idxs_to_update, :] = df_from.loc[idxs_to_update, :]

    # adding new rows
    idxs_to_add = df_from_idxs_set - df_to_idxs_set
    df_final = pd.concat([df_to, df_from.loc[idxs_to_add, :]])

    # returning the merged data frame
    return df_final


def load_data_from_pickle(pickle_file_path):
    # the actual decorator
    def load_from_pickle_decorator(load_function):
        # the wrapper function
        @functools.wraps(load_function)
        def wrapper(*args, **kwargs):
            data_set = None
            try:
                # loading pickled data set
                with open(pickle_file_path, 'rb') as f:
                    data_set = pickle.load(f)
            except IOError:
                # doing nothing
                pass

            # if the data set was not loaded from pickle
            if data_set is None:
                data_set = load_function(*args, **kwargs)

                # pickling/caching the data set
                with open(pickle_file_path, 'wb') as f:
                    pickle.dump(data_set, f, -1)

            # returning the data set
            return data_set

        # returning the wrapper function of the 'decorated' function
        return wrapper

    # returning the actual decorator
    return load_from_pickle_decorator


def update_data_from_pickle(pickle_file_path, do_update=False):
    # the actual decorator
    def update_from_pickle_decorator(load_function):
        # the wrapper function
        @functools.wraps(load_function)
        def wrapper(*args, **kwargs):
            try:
                # loading pickled data set
                with open(pickle_file_path, 'rb') as f:
                    pickle_ds = pickle.load(f)
            except IOError:
                pickle_ds = None

            # if an update was forced
            if do_update:
                # setting cached_ds
                cached_ds = pickle_ds

                # computing some additions to the already cached data set
                update_ds = load_function(*args, **kwargs)

                # if no data has been cached for now
                if cached_ds is None:
                    pickle_ds = update_ds

                # some data was cached previously
                else:
                    # no need to update
                    if update_ds is None:
                        pass

                    # updating previously cached data set
                    else:
                        # getting measures related information
                        cached_measures = cached_ds[MEAS_IDX]
                        update_measures = update_ds[MEAS_IDX]

                        # getting measures intra-inter distributions
                        cached_intra_inter = cached_measures[DIST_IDX]
                        update_intra_inter = update_measures[DIST_IDX]

                        # updating/adding newly computed intra-inter distributions
                        for m in update_intra_inter:
                            cached_intra_inter[m] = update_intra_inter[m]

                        # merging measures data frames
                        df_measures = merge_data_frames(cached_measures[DF_IDX], update_measures[DF_IDX])

                        # getting measures info ready for caching
                        measures_info = cached_intra_inter, df_measures

                        # -------------

                        clustering_info = merge_data_frames(cached_ds[CLUS_IDX], update_ds[CLUS_IDX])

                        # -------------

                        classification_info = merge_data_frames(cached_ds[CLAS_IDX], update_ds[CLAS_IDX])

                        # -------------

                        # building newly pickled data set
                        pickle_ds = measures_info, clustering_info, classification_info

                # pickling/caching the data set
                with open(pickle_file_path, 'wb') as f:
                    pickle.dump(pickle_ds, f, -1)

            # returning the data set
            return pickle_ds

        # returning the wrapper function of the 'decorated' function
        return wrapper

    # returning the actual decorator
    return update_from_pickle_decorator
