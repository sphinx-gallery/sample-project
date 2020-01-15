"""
Data download example
=====================

This example shows one way of dealing with large data files required for your
examples.

Data is downloaded, by default to the folder ``~/sg_data``, and the location
is stored in a config file under the key 'data_path'. You can now use the data
again in a different example without downloading the data again.

Note that examples in the gallery are ordered according to their filenames,
thus the number after 'plot\_' dictates the order the example appears in the
gallery.
"""

import SampleModule.data_download as dd
import pandas as pd


data_file = dd.download_data(
    url='http://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data',\
    data_file_name='iris.csv')

iris = pd.read_csv(data_file, header=None)
iris.head()






