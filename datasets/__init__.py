#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, August 2016

# gc data sets
from .gc_mud import load_gc_mud
from .gc_wines import load_gc_wines

# hplc data sets
from .hplc_oil import load_hplc_oil

# ir data sets
from .ir_wines import load_ir_wines

# ms data sets
from .ms_cola import load_ms_cola
from .ms_diesel import load_ms_diesel
from .ms_glycol import load_ms_glycol
from .ms_olive_oil import load_ms_olive_oil
from .ms_wines import load_ms_wines

# mvda data sets
from .mvda_alcohol import load_mvda_alcohol
from .mvda_archeology import load_mvda_archeology
from .mvda_cream_cheese import load_mvda_cream_cheese
from .mvda_peas_raw import load_mvda_peas_raw
from .mvda_sucos import load_mvda_sucos
from .mvda_tea import load_mvda_tea
from .mvda_soil import load_mvda_soil

# multi-way data sets
from .mw_gc_ms_wines import load_mw_gc_ms_wines

# nir data sets
from .nir_alcohol import load_nir_alcohol
from .nir_corn import load_nir_corn
from .nir_fuel import load_nir_fuel
from .nir_sugarcane import load_nir_sugarcane
from .nir_tablets import load_nir_tablets
from .nir_tecator import load_nir_tecator

# nmr data sets
from .nmr_onion import load_nmr_onion
from .nmr_wine import load_nmr_wines

# raman data sets
from .raman_tablets import load_raman_tablets
from .raman_porkfat import load_raman_porkfat

# ---------------------------------------------------------------

GC_MUD = 2
GC_WINES = 4

HPLC_OIL = 5

IR_WINES = 9

MS_COLA = 11
MS_DIESEL = 12
MS_GLYCOL = 13
MS_OLIVE_OIL = 14
MS_WINES = 15

MVDA_ALCOHOL = 16
MVDA_ARCHEOLOGY = 17
MVDA_CREAM_CHEESE = 18
MVDA_PEAS_RAW = 19
MVDA_SOIL = 20
MVDA_SUCOS = 21
MVDA_TEA = 22

MW_GC_MS_WINES = 24

NIR_ALCOHOL = 25
NIR_CORN = 26
NIR_FUEL = 27
NIR_SUGARCANE = 28
NIR_TABLETS = 29
NIR_TECATOR = 30

NMR_ONION = 31
NMR_WINES = 32

RAMAN_PORKFAT = 33
RAMAN_TABLETS = 34

# ---------------

# list of all data sets included in the toolbox
datasets_list = [
    GC_MUD,
    GC_WINES,

    HPLC_OIL,

    IR_WINES,

    MS_COLA,
    MS_DIESEL,
    MS_GLYCOL,
    MS_OLIVE_OIL,
    MS_WINES,

    MVDA_ALCOHOL,
    MVDA_ARCHEOLOGY,
    MVDA_CREAM_CHEESE,
    MVDA_PEAS_RAW,
    MVDA_SOIL,
    MVDA_SUCOS,
    MVDA_TEA,

    MW_GC_MS_WINES,

    NIR_ALCOHOL,
    NIR_CORN,
    NIR_FUEL,
    NIR_SUGARCANE,
    NIR_TABLETS,
    NIR_TECATOR,

    NMR_ONION,
    NMR_WINES,

    RAMAN_PORKFAT,
    RAMAN_TABLETS,
]

# ---------------

# data sets load functions
dataset_id_load_func = {
    GC_MUD:             load_gc_mud,
    GC_WINES:           load_gc_wines,

    HPLC_OIL:           load_hplc_oil,

    IR_WINES:           load_ir_wines,

    MS_DIESEL:          load_ms_diesel,
    MS_GLYCOL:          load_ms_glycol,
    MS_OLIVE_OIL:       load_ms_olive_oil,
    MS_WINES:           load_ms_wines,

    MVDA_ALCOHOL:       load_mvda_alcohol,
    MVDA_ARCHEOLOGY:    load_mvda_archeology,
    MVDA_CREAM_CHEESE:  load_mvda_cream_cheese,
    MVDA_PEAS_RAW:      load_mvda_peas_raw,
    MVDA_SOIL:          load_mvda_soil,
    MVDA_SUCOS:         load_mvda_sucos,
    MVDA_TEA:           load_mvda_tea,

    MW_GC_MS_WINES:     load_mw_gc_ms_wines,

    NIR_ALCOHOL:        load_nir_alcohol,
    NIR_CORN:           load_nir_corn,
    NIR_FUEL:           load_nir_fuel,
    NIR_SUGARCANE:      load_nir_sugarcane,
    NIR_TABLETS:        load_nir_tablets,
    NIR_TECATOR:        load_nir_tecator,

    NMR_ONION:          load_nmr_onion,
    NMR_WINES:          load_nmr_wines,

    RAMAN_PORKFAT:      load_raman_porkfat,
    RAMAN_TABLETS:      load_raman_tablets,
}

# ---------------

# data sets names
dataset_names = {
    GC_MUD:             'gc_mud',
    GC_WINES:           'gc_wines',

    HPLC_OIL:           'hplc_oil',

    IR_WINES:           'ir_wines',

    MS_COLA:            'ms_cola',
    MS_DIESEL:          'ms_diesel',
    MS_GLYCOL:          'ms_glycol',
    MS_OLIVE_OIL:       'ms_olive_oil',
    MS_WINES:           'ms_wines',

    MVDA_ALCOHOL:       'mvda_alcohol',
    MVDA_ARCHEOLOGY:    'mvda_archeology',
    MVDA_CREAM_CHEESE:  'mvda_cream_cheese',
    MVDA_PEAS_RAW:      'mvda_peas_raw',
    MVDA_SOIL:          'mvda_soil',
    MVDA_SUCOS:         'mvda_sucos',
    MVDA_TEA:           'mvda_tea',

    MW_GC_MS_WINES:     'mw_gc_ms_wines',

    NIR_ALCOHOL:        'nir_alcohol',
    NIR_CORN:           'nir_corn',
    NIR_FUEL:           'nir_fuel',
    NIR_SUGARCANE:      'nir_sugarcane',
    NIR_TABLETS:        'nir_tablets',
    NIR_TECATOR:        'nir_tecator',

    NMR_ONION:          'nmr_onion',
    NMR_WINES:          'nmr_wines',

    RAMAN_PORKFAT:      'raman_porkfat',
    RAMAN_TABLETS:      'raman_tablets',
}

# ---------------

def load_dataset_by_id(dataset_id):
    # validating the id provided
    if dataset_id not in dataset_id_load_func:
        raise ValueError('Unknown data set id')

    # getting the load function
    load_data_set_function = dataset_id_load_func[dataset_id]

    # actually loading the data set
    return load_data_set_function()
