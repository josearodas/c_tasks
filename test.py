import pandas as pd
import matplotlib.pylab as plt
import numpy as np

data = pd.read_csv('nback_system')

subdata = pd.DataFrame(data.Date,data.n_level)

print data.index