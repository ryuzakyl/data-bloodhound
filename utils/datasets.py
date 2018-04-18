#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, July 2017

import os
import re

import pandas as pd

# importing decorator to be used in all data set loading utilities
from .decorators import load_data_from_pickle

# ------------------------------------------------------------------------

# For more info on parsing numbers in scientific notation see:
#   . http://stackoverflow.com/questions/638565/parsing-scientific-notation-sensibly

# regular expression to get only data from files
# JASCO_DATA_REGEX = r'^([-+]?\d*\.\d+|\d+)\s+([+-]?\d+.?\d*(?:[Ee]-\d+)?)'
JASCO_DATA_REGEX = r'^([-+]?\d*\.\d+|\d+)\s+([+\-]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+)?)'

# condition that indicates that the content matched is not of interest
JASCO_NOT_MATCH_COND = lambda match: len(match) != 1 or len(match[0]) != 2


def parse_jasco_file(jasco_file_path, file_encoding):
    with open(jasco_file_path, mode='r', encoding=file_encoding) as f:
        return parse_jasco_content(f)


def parse_jasco_content(jasco_file_content):
    # for each line in file
    raw_data = list()   # raw data extracted from file
    for line in jasco_file_content:
        # performing pattern matching to the current line
        match = re.findall(JASCO_DATA_REGEX, line)

        # skipping pattern if not what we want
        if JASCO_NOT_MATCH_COND(match):
            continue

        # appending pattern to list
        label, data = match[0]
        raw_data.append((float(label), float(data)))

    return raw_data


def check_jasco_format(jasco_file_path, file_encoding):
    with open(jasco_file_path, mode='r', encoding=file_encoding) as f:
        return check_jasco_content(f)


def check_jasco_content(jasco_file_content):
    # first line starts with 'TITLE'
    if not jasco_file_content.readline().startswith('TITLE'):
        print("Error in Line 1: 'TITLE' attribute error")
        return False

    if not jasco_file_content.readline().startswith('DATA TYPE'):
        print("Error in Line 2: 'DATA TYPE' attribute error")
        return False

    if not jasco_file_content.readline().startswith('ORIGIN'):
        print("Error in Line 3: 'ORIGIN' attribute error")
        return False

    if not jasco_file_content.readline().startswith('OWNER'):
        print("Error in Line 4: 'OWNER' attribute error")
        return False

    if not jasco_file_content.readline().startswith('DATE'):
        print("Error in Line 5: 'DATE' attribute error")
        return False

    if not jasco_file_content.readline().startswith('TIME'):
        print("Error in Line 6: 'TIME' attribute error")
        return False

    if not jasco_file_content.readline().startswith('SPECTROMETER'):
        print("Error in Line 7: 'TIME' attribute error")
        return False

    if not jasco_file_content.readline().startswith('RESOLUTION'):
        print("Error in Line 8: 'RESOLUTION' attribute error")
        return False

    if not jasco_file_content.readline().startswith('DELTAX'):
        print("Error in Line 9: 'DELTAX' attribute error")
        return False

    if not jasco_file_content.readline().startswith('XUNITS'):
        print("Error in Line 10: 'XUNITS' attribute error")
        return False

    if not jasco_file_content.readline().startswith('YUNITS'):
        print("Error in Line 11: 'YUNITS' attribute error")
        return False

    if not jasco_file_content.readline().startswith('FIRSTX'):
        print("Error in Line 12: 'FIRSTX' attribute error")
        return False

    if not jasco_file_content.readline().startswith('LASTX'):
        print("Error in Line 13: 'LASTX' attribute error")
        return False

    npoints_line = jasco_file_content.readline().strip()
    npoints = int(npoints_line.split(' ')[-1])
    if not npoints_line.startswith('NPOINTS') or npoints <= 0:
        print("Error in Line 14: 'NPOINTS' attribute error")
        return False

    if not jasco_file_content.readline().startswith('FIRSTY'):
        print("Error in Line 15: 'FIRSTY' attribute error")
        return False

    if not jasco_file_content.readline().startswith('MAXY'):
        print("Error in Line 16: 'MAXY' attribute error")
        return False

    if not jasco_file_content.readline().startswith('MINY'):
        print("Error in Line 17: 'MINY' attribute error")
        return False

    if not jasco_file_content.readline().startswith('XYDATA'):
        print("Error in Line 18: 'XYDATA' attribute error")
        return False

    # parsing jasco file
    raw_data = parse_jasco_content(jasco_file_content)

    return len(raw_data) == npoints

# ------------------------------------------------------------------------

# regular expression to get only data from files
SCAN_DATA_REGEX = r'([+-]?\d+.?\d*),\s*([+-]?\d+.?\d*(?:[Ee]-\d+)?)'

# condition that indicates that the content matched is not of interest
SCAN_NOT_MATCH_COND = lambda match: len(match) != 1 or len(match[0]) != 2


def check_scan_format(scan_file_path, file_encoding):
    with open(scan_file_path, mode='r', encoding=file_encoding) as f:
        return check_scan_content(f)


def check_scan_content(scan_file_content):
    # first line ends with '.scan'
    if not scan_file_content.readline().endswith('.scan'):
        print("Error in Line 1: '.scan' extension missing")
        return False

    # second line should be 'Wavelength,Reading'
    if not scan_file_content.readline().startswith('Wavelength,Reading'):
        print("Error in Line 2: 'Wavelength,Reading' expected")
        return False

    # parsing scan file
    raw_data = parse_scan_content(scan_file_content)

    # nothing additional to check
    return raw_data


def parse_scan_file(scan_file_path, file_encoding):
    with open(scan_file_path, mode='r', encoding=file_encoding) as f:
        return parse_scan_content(f)


def parse_scan_content(scan_file_content):
    # for each line in file
    raw_data = list()   # raw data extracted from file
    for line in scan_file_content:
        # performing pattern matching to the current line
        match = re.findall(SCAN_DATA_REGEX, line)

        # skipping pattern if not what we want
        if SCAN_NOT_MATCH_COND(match):
            continue

        # appending pattern to list
        label, data = match[0]
        raw_data.append((float(label), float(data)))

    return raw_data

# ------------------------------------------------------------------------


def check_list_format(list_file_path, file_encoding):
    with open(list_file_path, mode='r', encoding=file_encoding) as f:
        return check_list_content(f)


def check_list_content(list_file_content):
    # parsing scan file
    raw_data = parse_list_content(list_file_content)

    # nothing additional to check
    return len(raw_data) > 0


def parse_list_file(list_file_path, file_encoding):
    with open(list_file_path, mode='r', encoding=file_encoding) as f:
        return parse_list_content(f)


def parse_list_content(list_file_content):
    # for each line in file
    raw_data = list()   # raw data extracted from file
    for i, line in enumerate(list_file_content):
        # skipping line if not what we want
        if not is_number(line):
            continue

        # appending pattern to list
        label, data = i + 1, line
        raw_data.append((label, float(data)))

    return raw_data

# ------------------------------------------------------------------------


def build_data_set(data, samples_labels, features_labels, extra_cols=None):
    """Builds a data set from raw data information.

    Args:
        data: The samples data (vector of features).
        samples_labels: The samples names or labels.
        features_labels: Labels for every feature in the feature vector.
        extra_cols: Extra columns for the data set (e.g. classes, properties, etc.)

    Returns:
        DataFrame: A Pandas DataFrame with the data set (samples as rows and features as columns).

    """
    # validating features labels
    features_count = len(features_labels)
    if features_count <= 0:
        raise ValueError('The amount of features must be positive.')

    # validating data
    if len(data) <= 0 or not all(len(li) == features_count for li in data):
        raise ValueError('All samples must have the same amount of features.')

    # creating the data frame
    df = pd.DataFrame(data, index=samples_labels, columns=features_labels)

    # checking for extra_cols param
    if extra_cols is None:
        return df

    # validating extra columns
    cols = extra_cols.values()
    if len(extra_cols) < 1 or not all(len(x) == len(list(cols)[0]) for x in cols):
        raise ValueError('Invalid extra columns.')

    # appending extra columns to data frame
    for c_new in extra_cols.keys():
        df[c_new] = pd.Series(extra_cols[c_new], index=df.index)

    # returning the built data set
    return df


def load_files_from_folder(folder_path, parser_type, file_encoding):
    # validating folder
    if not os.path.exists(folder_path):
        raise ValueError('Invalid folder path.')

    # validating parser type (any of the 2 dictionaries would suffice)
    if parser_type not in file_parsers_dict:
        raise ValueError('Unknown parser type.')

    # getting file parser function
    parser = file_parsers_dict[parser_type]

    data = []
    for file_name in sorted(os.listdir(folder_path)):
        # parsing data files only
        file_path = "{}/{}".format(folder_path, file_name)
        if os.path.isdir(file_path) or file_name.endswith('.db') or file_name.endswith('.ini'):
            continue

        # adding parsed content to data
        parsed_info = parser(file_path, file_encoding)
        data.append((file_name, parsed_info))

    return data

# ------------------------------------------------------------------------


def build_clusters_from_data_set(data_set, class_col_name='class'):
    # validating the data set
    if data_set is None or not isinstance(data_set, pd.DataFrame):
        raise ValueError('Invalid data set provided.')

    # validating that column associated with class is present
    if class_col_name not in list(data_set.columns.values):
        raise ValueError('Unknown group by column specified.')

    # the clusters dictionary
    clusters = dict()

    # grouping by the specified column
    partition = data_set.groupby(class_col_name)

    # for each group found
    for label, g in partition:
        # removing the class column
        g = g.drop(class_col_name, 1)

        # adding cluster
        clusters[label] = [(index, list(row.values)) for index, row in g.iterrows()]

    return clusters


# ------------------------------------------------------------------------

# dictionary with all implemented file types parsers
file_parsers_dict = {
    'jasco':    parse_jasco_file,
    'scan':     parse_scan_file,
    'list':     parse_list_file,
}

# dictionary with all implemented content types parsers
content_parsers_dict = {
    'jasco':    parse_jasco_content,
    'scan':     parse_scan_content,
    'list':     parse_list_content,
}

# ------------------------------------------------------------------------

# list of valid cannabis samples for all 3 analytical techniques (UV, TLC, GC) used for this substance
cannabis_white_list = [
    'J016R', 'F014R', 'J005R', 'F002R', 'F010R', 'A001R', 'J001R', 'F006R', 'J009R', 'M003R',
    'J010R', 'J014R', 'J007R', 'J012R', 'L004S', 'M008R', 'C008X', 'J021R', 'M006R', 'C004X',
    'C002X', 'F004R', 'F008R', 'J020R', 'J002R', 'F003R', 'F007R', 'F011R', 'A002R', 'F001R',
    'M002R', 'J013R', 'L002S', 'J008R', 'M004R', 'J011R', 'J004R', 'J015R', 'J006R', 'K002R',
    'F009R', 'L001S', 'C007X', 'C005X', 'F005R', 'C009X', 'M005R', 'C003X', 'K001R', 'L003R',
]


def get_cannabis_sample_id(s):
    return s[0:5]


def build_classes_dictionary(classes_path):
    with open(classes_path, 'r') as f:
        labels_dict = dict()
        for line in f:
            line_splitted = line.split(',')
            labels_dict[line_splitted[0][:-4]] = int(line_splitted[1].strip())

    return labels_dict

# ------------------------------------------------------------------------


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
