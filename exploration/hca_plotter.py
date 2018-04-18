# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, July 2016

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.cluster.hierarchy as hca
from PyQt4 import QtGui
from matplotlib.widgets import Button, RadioButtons, CheckButtons
from .mpl_vertical_slider import VertSlider

import measures


class HcaPlotter(object):
    # the dataset to use in the clustering process
    data = None
    ext = ".txt"

    # labels of the samples in the dataset
    x_labels = None

    # data of the samples in the dataset
    x_data = None

    # the background color for the axes
    ax_back_color = 'lightgoldenrodyellow'

    # the threshold slider subplot
    ax_thres = None

    # last threshold line drawn
    last_thres_line = None

    # the dendrogram subplot
    ax_dendrogram = None

    # the 'methods' RadioButtons control
    ax_methods = None

    # available methods
    methods_dict = {
        'single':       'single',
        'complete':     'complete',
        'average':      'average',
        'weighted':     'weighted',
        # 'ward':         'ward',
    }

    # the selected method (the key)
    selected_method = None

    # the 'metrics' RadioButtons control
    ax_metrics = None

    metrics_dict = {
        measures.measures_names[measures.EUCLIDEAN]: measures.measure_to_function[measures.EUCLIDEAN],
        measures.measures_names[measures.CORRELATION]: measures.measure_to_function[measures.CORRELATION],
        measures.measures_names[measures.SAM]: measures.measure_to_function[measures.SAM],
        measures.measures_names[measures.SHAPE_HY]: measures.measure_to_function[measures.SHAPE_HY],
    }

    # the selected metric (the key)
    selected_metric = None

    # available options
    options_dict = {
        'Show labels':  False,
        'Show annotations': False
    }

    # button that invokes the clustering functionality
    ax_go_button = None

    # represents the result of the last linkage invoked
    last_linkage = None

    # button to save clustering results
    ax_save_button = None

    def __init__(self, df, metrics=None):
        # storing and parsing the dataset
        self.process_dataset(df)

        # setting the dendrogram subplot
        self.ax_dendrogram = plt.subplot(111)
        plt.subplots_adjust(left=0.1, right=0.95, bottom=0.25, top=0.95)

        # setting the 'threshold' slider control
        ax_thres = plt.axes([0.02, 0.25, 0.03, 0.7], axisbg=self.ax_back_color)
        self.ax_thres = VertSlider(ax_thres, 'Thres', 0.0, 1.0, valinit=0.5)
        self.ax_thres.valtext.set_visible(False)
        self.ax_thres.on_changed(self.on_ax_thres_changed)

        # setting the 'methods' radio control
        ax_methods = plt.axes([0.1, 0.01, 0.15, 0.15], axisbg=self.ax_back_color, zorder=5)
        methods_options = tuple(sorted(self.methods_dict.keys()))
        self.ax_methods = RadioButtons(ax_methods, methods_options, active=0)
        self.selected_method = list(self.methods_dict)[0]
        self.ax_methods.on_clicked(self.on_ax_methods_clicked)

        # setting the 'metrics' radio control
        if metrics is not None:
            self.metrics_dict = {}

            # for each metric supplied
            for m in metrics:
                if m not in measures.measures_list:
                    raise ValueError('Unknown metric')

                # dynamically adding metrics
                self.metrics_dict[measures.measures_names[m]] = measures.measure_to_function[m]

        ax_metrics = plt.axes([0.3, 0.01, 0.16, 0.15], axisbg=self.ax_back_color, zorder=4)
        metrics_options = tuple(sorted(self.metrics_dict.keys()))
        self.ax_metrics = RadioButtons(ax_metrics, metrics_options, active=0, activecolor='blue')
        self.selected_metric = list(self.metrics_dict)[0]
        self.ax_metrics.on_clicked(self.on_ax_metrics_clicked)

        # adding visualization options
        ax_options = plt.axes([0.51, 0.01, 0.26, 0.15], axisbg=self.ax_back_color)
        opt_labels = ('Show labels', 'Show annotations')
        opt_vals = (False,) * len(opt_labels)
        self.ax_options = CheckButtons(ax_options, opt_labels, opt_vals)
        self.ax_options.on_clicked(self.on_ax_options_clicked)

        # adding the button that actually performs clustering
        btn_width = 0.14
        ax_go_button = plt.axes([0.95 - btn_width, 0.09, btn_width, 0.5 * btn_width])
        self.ax_go_button = Button(ax_go_button, 'Go!!!', color=self.ax_back_color, hovercolor='0.911')
        self.ax_go_button.on_clicked(self.on_ax_go_button_clicked)

        # adding the button that saves the results
        ax_save_button = plt.axes([0.95 - btn_width, 0.01, btn_width, 0.5 * btn_width])
        self.ax_save_button = Button(ax_save_button, 'Save!!!', color=self.ax_back_color, hovercolor='0.911')
        self.ax_save_button.on_clicked(self.on_ax_save_button_clicked)

    def __get_dataset(self):
        return self.data

    def __set_dataset(self, value):
        self.process_dataset(value)

    dataset = property(fget=__get_dataset, fset=__set_dataset, doc='''The dataset to process by means of HCA''')

    def on_ax_thres_changed(self, value):
        # if we haven't made a first attempt on clustering, we exit
        if self.last_linkage is None:
            return

        # removing last threshold line drawn
        if self.last_thres_line is not None:
            self.last_thres_line.remove()

        # re-drawing the whole dendrogram for this threshold value
        self.draw_dendrogram(self.last_linkage, self.options_dict)

    def on_ax_methods_clicked(self, label):
        # changing selected method
        self.selected_method = label

    def on_ax_metrics_clicked(self, label):
        # changing selected metric
        self.selected_metric = label

    def on_ax_options_clicked(self, label):
        # updating the selected options
        self.options_dict[label] = not self.options_dict[label]

        # if we haven't made a first attempt on clustering, we exit
        if self.last_linkage is None:
            return

        # re-drawing the whole dendrogram for the new options
        self.draw_dendrogram(self.last_linkage, self.options_dict)

    def on_ax_go_button_clicked(self, event):
        try:
            # attempting to do hierarchical clustering
            self.do_clustering(self.selected_method, self.selected_metric, self.options_dict)

            # showing success message
            QtGui.QMessageBox.information(None, 'Information', 'Hierarchical clustering was a success.')

        # case of exception
        except Exception as e:
            # showing error message
            QtGui.QMessageBox.critical(None, 'Error', '{}'.format(str(e)))

    def on_ax_save_button_clicked(self, event):
        try:
            # if we haven't made a first attempt on clustering, we exit
            if self.last_linkage is None:
                # showing success message
                QtGui.QMessageBox.warning(None, "Warning", "You should perform hierarchical clustering first.")
                return

            # opening a save file dialog
            file_path = QtGui.QFileDialog.getSaveFileName(None, 'Save File', './', 'txt files (*.txt)\nAll files (*.*)')

            # getting the partition
            partition = self.get_partition(include_labels=True, include_data=True)

            # building the lines to write to file
            lines = ['{},{}\n'.format(x_label, c_label) for x_label, c_label, _ in partition]

            # writing lines to selected file
            with open(file_path, 'w') as f:
                f.writelines(lines)

            # showing success message
            QtGui.QMessageBox.information(None, 'Information', 'Results saved successfully.', 'OK')

        except Exception as e:
            QtGui.QMessageBox.critical(None, 'Error', 'Failed to save results.', 'OK')
            raise e

    # --------------------------------------------------

    def process_dataset(self, df):
        self.data = df
        self.x_labels = df.index.tolist()
        self.x_data = df.values

    def do_clustering(self, method, metric, options):
        # creating the pandas data frame (df.index.values -> for labels, df.values -> for data)
        df = pd.DataFrame(np.array(self.x_data), index=self.x_labels)

        # getting 'method' and 'metric'
        link_method = self.methods_dict[method]
        link_metric = self.metrics_dict[metric]

        # actually performing hierarchical cluster analysis
        self.last_linkage = hca.linkage(df, method=link_method, metric=link_metric)

        self.last_linkage = np.clip(self.last_linkage, 0.0, None)

        # drawing the dendrogram
        self.draw_dendrogram(self.last_linkage, options)

    def get_partition(self, thres=None, include_labels=False, include_data=False):
        # if we haven't made a first attempt on clustering, we return None
        if self.last_linkage is None:
            return None

        if thres is None:
            # getting the threshold from the vertical slider
            lb, ub = self.last_linkage[0][2], self.last_linkage[-1][2]
            thres = lb + self.ax_thres.val * (ub - lb)

        # actually getting the partition with the distance criterion
        partition = hca.fcluster(self.last_linkage, t=thres, criterion='distance')

        # if samples are not required, simply return the partition
        if not include_labels:
            return partition

        if len(self.x_labels) != len(partition):
            raise Exception("The amount of samples doesn't match with the partition size.")

        if not include_data:
            return [(self.x_labels[i], partition[i]) for i in range(len(self.x_labels))]

        if len(self.x_data) != len(partition):
            raise Exception("The amount of samples doesn't match with the partition size.")

        return [
            (self.x_labels[i], partition[i], self.x_data[i])
            for i in range(len(self.x_labels))
        ]

    def draw_dendrogram(self, linkage, options):
        # 'changing the focus' to the dendrogram axis
        plt.sca(self.ax_dendrogram)

        # clearing all the content of the dendrogram axis
        plt.cla()

        # getting 'options'
        named_args = dict()
        named_args['no_labels'] = False if options['Show labels'] else True
        named_args['annotate'] = True if options['Show annotations'] else False

        # computing 'cutoff' threshold value
        y_min, y_max = self.last_linkage[0][2], self.last_linkage[-1][2]
        thres = y_min + self.ax_thres.val * (y_max - y_min)
        named_args['color_threshold'] = thres

        # passing the dataset labels
        named_args['labels'] = self.x_labels
        named_args['leaf_font_size'] = 8.

        # actually plotting the dendrogram
        _ = self.dendrogram_with_annotation(linkage, **named_args)

        # rotating x labels
        plt.xticks(rotation=90)

        # drawing the new threshold line
        x_min, x_max = self.ax_dendrogram.get_xlim()
        self.last_thres_line = self.ax_dendrogram.axhline(y=thres, xmin=x_min, xmax=x_max, c="blue", linewidth=1.0, zorder=1000)

        # re-drawing the control
        plt.draw()

    def dendrogram_with_annotation(*args, **kwargs):
        # removing the first HcaPlotter instance object
        args = args[1:]

        # checking for my keyword 'annotate'
        if 'annotate' not in kwargs:
            annotate_dendrogram = False
        else:
            # getting the value of 'annotate' from 'kwargs'
            annotate_dendrogram = kwargs['annotate']

            # removing the value from 'kwargs'
            kwargs.pop('annotate')

        # calling the original dendrogram function
        dend_data = hca.dendrogram(*args, **kwargs)

        # annotating dendrogram if requested
        if annotate_dendrogram:
            for i, d in zip(dend_data['icoord'], dend_data['dcoord']):
                x = 0.5 * sum(i[1:3])
                y = d[1]
                plt.plot(x, y, 'ro')
                plt.annotate("%.3g" % y, (x, y), xytext=(0, -8), textcoords='offset points', va='top', ha='center')

        # returning the data usually returned by the dendrogram function
        return dend_data

    def show(self):
        plt.show()

def build_features(features):
    # building the content of the 'samples_features' file
    f = lambda nf: "{}".format(nf)
    sf_data = [
        "%s\n" % ",".join(map(f, s_data))
        for s_data in features
    ]
    return sf_data