#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, May 2017

import os
import re
import shutil

# ---------------------------------------------------------------


def clear_folder(folder_path, exclude_patterns=list()):
    # building the exclusion regular expression
    exclude_regexes = [re.compile(p) for p in exclude_patterns]

    # for each item in the folder
    for item in os.listdir(folder_path):
        # creating a full path to the item
        item_path = os.path.join(folder_path, item)

        # skipping if current item matches any pattern from the exclusion pattern
        if any(rgx.match(item) for rgx in exclude_regexes):
            continue

        try:
            # removing item if it is a file
            if os.path.isfile(item_path):
                os.unlink(item_path)

            # removing the item if it is a dir
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)

        # case of an exception
        except Exception as e:
            print(e)
