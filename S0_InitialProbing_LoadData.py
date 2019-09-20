import numpy as np
import pandas as pd

FilePath = 'C:\\Users\\diman\\OneDrive\\Work_temp\\Insight\\WineKaggleData\\'
LoadFileName = 'winemag-data-130k-v2.csv'
PyFileName = 'S1_InitialProbing_LoadData'

Data = pd.read_csv(FilePath+LoadFileName, index_col=0)


