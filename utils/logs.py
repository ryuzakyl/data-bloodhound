#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, May 2017

import os
import sys
import logging

from .io import clear_folder

# ---------------------------------------------------------------


def configure_logger(file_path):
    # http://stackoverflow.com/questions/9321741/printing-to-screen-and-writing-to-a-file-at-the-same-time

    # creating 'file_path' containing folder if it does not exists
    folder_path = os.path.split(file_path)[0]

    # creating folder
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    else:
        clear_folder(folder_path, [r".+\.pickle$"])

    # clearing handlers of root logger
    root_logger = logging.getLogger('')
    root_logger.handlers = []

    # file logger configuration
    logging.basicConfig(
        filename=file_path,                 # the path  of the log file
        filemode='w',                       # destroys the file and creates it from scratch
        level=logging.INFO,                 # logging only 'INFO' logs
        format='%(asctime)s %(message)s'    # format in which logs will be written
    )

    # console (STDOUT) logger configuration
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(message)s')
    console.setFormatter(formatter)

    # adding the console logger to the root logger
    root_logger.addHandler(console)
