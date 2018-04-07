=========
Data sets
=========

A data set (or dataset) is a collection of data. The term data set may also
be used more loosely, to refer to the data in a collection corresponding to
a particular experiment or event. Keep reading for discovering all the data
sets available in this toolbox.

:UC:
    Unsupervised Classification (Data set is suitable for **Unsupervised Classification**).

:SC:
    Supervised Classification (Data set is suitable for **Supervised Classification**).

:RC:
    Regression/Calibration (Data set is suitable for **Regression/Calibration**).

:DE:
    Data Exploration (Data set is suitable for **Data Exploration**-PCA, etc.-).

:MW:
    Multi-Way (Data set is-or can be transformed into- a **multi-way** data set).

.. |yes| image:: _images/summary-table/yes.png
   :scale: 7%
   :align: middle

.. |no| image:: _images/summary-table/no.png
   :scale: 4%
   :align: middle

=================================================  ========= ====================== ===== ===== ===== ===== =====
Data set                                           Data Size Features Size          UC    SC    RC    DE    MW
=================================================  ========= ====================== ===== ===== ===== ===== =====
:doc:`GC Mud <gc-mud>`                             77        527                    |yes| |no|  |no|  |yes| |no|
:doc:`GC Wines <gc-wines>`                         44        2700 (+1)()            |yes| |yes| |no|  |yes| |no|
:doc:`HPLC Oil <hplc-oil>`                         120       4001 (+2)()            |yes| |yes| |no|  |yes| |no|
:doc:`IR Wines <ir-wines>`                         44        843 (+1)()             |yes| |yes| |no|  |yes| |no|
:doc:`MS Cola <ms-cola>`                           44        106 (+1)()             |yes| |yes| |no|  |yes| |no|
:doc:`MS Diesel <ms-diesel>`                       44        202 (+1)(+1)           |yes| |yes| |yes| |yes| |no|
:doc:`MS Glycol <ms-glycol>`                       162       253 ()(+1)             |yes| |no|  |yes| |yes| |no|
:doc:`MS Olive Oil <ms-olive-oil>`                 40        101 (+1)()             |yes| |yes| |no|  |yes| |no|
:doc:`MS Wines <ms-wines>`                         44        200 (+1)()             |yes| |yes| |no|  |yes| |no|
:doc:`MVDA Alcohol <mvda-alcohol>`                 65        53 (+1)()              |yes| |yes| |no|  |yes| |no|
:doc:`MVDA Archeology <mvda-arch>`                 63 (+12)  10 (+1)()              |yes| |yes| |no|  |yes| |no|
:doc:`MVDA Cream Cheese <mvda-cream-cheese>`       240       23 (+6)()              |yes| |yes| |no|  |yes| |yes|
:doc:`MVDA Peas Raw <mvda-peas-raw>`               1200      15 (+3)()              |yes| |yes| |no|  |yes| |yes|
:doc:`MVDA Soil <mvda-soil>`                       66 (+15)  7 (+1)()               |yes| |yes| |no|  |yes| |no|
:doc:`MVDA Sucos <mvda-sucos>`                     42        9 (+1)()               |yes| |yes| |no|  |yes| |no|
:doc:`MVDA Tea <mvda-tea>`                         31        6 (+2)()               |yes| |yes| |no|  |yes| |no|
:doc:`MW GC-MS/FT-IR Wines <mw-gc-ms-wines>`       44        (2700x200x843)(+1)()   |yes| |yes| |no|  |yes| |yes|
:doc:`NIR Alcohol <nir-alcohol>`                   67        101 ()(+3)             |yes| |no|  |yes| |yes| |no|
:doc:`NIR Corn <nir-corn>`                         80x3      700 ()(+4)             |yes| |no|  |yes| |yes| |no|
:doc:`NIR Fuel <nir-fuel>`                         784       401 ()(+7)             |yes| |no|  |yes| |yes| |no|
:doc:`NIR Sugarcane <nir-sugarcane>`               1797      745 (+3)(+2)           |yes| |yes| |yes| |yes| |no|
:doc:`NIR Tablets <nir-tablets>`                   310       404 (+2)(+1)           |yes| |yes| |yes| |yes| |no|
:doc:`NIR Tecator <nir-tecator>`                   240       100 (+1)(+1)           |yes| |yes| |yes| |yes| |no|
:doc:`NMR Onion <nmr-onion>`                       31        29001 ()(+1)           |yes| |no|  |yes| |yes| |no|
:doc:`NMR Wine <nmr-wine>`                         40        8712 ()(+17)           |yes| |no|  |yes| |yes| |no|
:doc:`Raman Porkfat <raman-porkfat>`               105       5667 (+3)(+19)         |yes| |yes| |yes| |yes| |no|
:doc:`Raman Tablets <raman-tablets>`               120       3401 (+1)(+1)          |yes| |yes| |yes| |yes| |no|
=================================================  ========= ====================== ===== ===== ===== ===== =====

.. toctree::
   :hidden:

   gc-mud
   gc-wines
   hplc-oil
   ir-wines
   ms-cola
   ms-diesel
   ms-glycol
   ms-olive-oil
   ms-wines
   mvda-alcohol
   mvda-arch
   mvda-cream-cheese
   mvda-peas-raw
   mvda-soil
   mvda-sucos
   mvda-tea
   mw-gc-ms-wines
   nir-alcohol
   nir-corn
   nir-fuel
   nir-sugarcane
   nir-tablets
   nir-tecator
   nmr-onion
   nmr-wine
   raman-porkfat
   raman-tablets
