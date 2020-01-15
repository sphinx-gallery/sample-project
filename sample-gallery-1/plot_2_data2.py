"""
Data download example 2
=======================

Once you have downloaded the required data, you can obtain the location of the
data directory using ``get_config()`` and the key 'data_path'.
"""

import SampleModule.data_download as dd
import os
import pandas as pd

data_path = dd.get_config('data_path')
data_file = os.path.join(data_path, 'iris.csv')

iris = pd.read_csv(data_file, header=None)
iris.head()