
# coding: utf-8

# # AIRDOS AmPuCf Clibration (256 ch. version)

# In[5]:

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from IPython.display import Image as ImageDisp
from pandas import DataFrame
import string
import os
import matplotlib.pyplot as plt


# In[6]:

get_ipython().magic(u'pylab inline --no-import-all')


# ## Read Logfile

# In[7]:

fto = './data/DATALOG.TXT' #  File to Open
l=[]
l.extend(range(0,520))
df = pd.read_table(fto, sep=',', header=None, names=l, comment='*',engine='python' )

#
''' DEBUG
df = df.reset_index(drop=True)
df.drop(df[df.index > 100].index, inplace=True)
'''#'''

df.drop(df[df[0]=='$GPTXT'].index, inplace=True)
#df.drop(r[r[0]=='$GPRMC'].index, inplace=True)
df.drop(df[df[0]=='$GPVTG'].index, inplace=True)
df.drop(df[df[0]=='$GPGLL'].index, inplace=True)
df.drop(df[df[0]=='$GPGSA'].index, inplace=True)
df.drop(df[df[0]=='$GPGSV'].index, inplace=True)
#df.drop(df[df[0]=='$CANDY'].index, inplace=True)


# # Spectrum Interactive

# In[15]:

get_ipython().magic(u'matplotlib qt')
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from IPython.display import Image as ImageDisp
from pandas import DataFrame
import string
import os
import matplotlib.pyplot as plt

fto = './data/DATALOG.TXT' #  File to Open
l=[]
l.extend(range(0,520))
df = pd.read_table(fto, sep=',', header=None, names=l, comment='*')

#
''' DEBUG
df = df.reset_index(drop=True)
df.drop(df[df.index > 100].index, inplace=True)
'''#'''

df.drop(df[df[0]=='$GPTXT'].index, inplace=True)
#df.drop(r[r[0]=='$GPRMC'].index, inplace=True)
df.drop(df[df[0]=='$GPVTG'].index, inplace=True)
df.drop(df[df[0]=='$GPGLL'].index, inplace=True)
df.drop(df[df[0]=='$GPGSA'].index, inplace=True)
df.drop(df[df[0]=='$GPGSV'].index, inplace=True)
#df.drop(df[df[0]=='$CANDY'].index, inplace=True)


matplotlib.rcParams.update({'font.size': 20})

rc = df.loc[df[0]=='$CANDY']
rc.reset_index(drop=True, inplace=True)

rc = rc.apply(pd.to_numeric, errors='coerce')

rc['sum'] = rc[range(270,513)].sum(axis=1)

plt.figure(figsize=(20,5))
plt.yscale('log')

rc.ix[:,'sum'].plot(c='black')

plt.title('Select 6 points: begin Am - end Am, begin Pu - end Pu, begin Cf - end Cf.')
plt.xlabel('Measurement No.')
plt.ylabel('Flux [counts per 10 s]')

#----------- Select Measurements in Flux diagram -----------------------------
points=plt.ginput(6)

e1 = [points[0][0],points[1][0]]
e2 = [points[2][0],points[3][0]]
e3 = [points[4][0],points[5][0]]

rc.ix[e1[0]:e1[1],'sum'].plot(c='b')
rc.ix[e2[0]:e2[1],'sum'].plot(c='orange')
rc.ix[e3[0]:e3[1],'sum'].plot(c='g')

plt.title('AIRDOS')
plt.xlabel('measurement No.')
plt.ylabel('Flux [counts per 10 s]')

#----------- Plot Spectrum -----------------------------
LOW_ENERGY = 256

ener1 = rc.ix[e1[0]:e1[1],LOW_ENERGY:513].sum()
ener2 = rc.ix[e2[0]:e2[1],LOW_ENERGY:513].sum()
ener3 = rc.ix[e3[0]:e3[1],LOW_ENERGY:513].sum()
 
plt.figure(figsize=(15,10))
plt.yscale('log')

plt.plot(ener1, label='Am-241 5.49 MeV (85 %) / 5.44 MeV (13 %)', drawstyle='steps-pre', c='blue')
plt.plot(ener2, label='Pu-239 5.16 MeV (73 %) / 5.14 (15 %) / 5.11 (12 %)', drawstyle='steps-pre', c='orange')
plt.plot(ener3, label='Cf-252 6.12 MeV (84 %) / 6.08 MeV (16 %)', drawstyle='steps-pre', c='green')
#plt.ylim([0,20000])
#plt.xlim([600,750])
plt.legend()
plt.title('AIRDOS Alpha Spectrum')
plt.xlabel('Channel')
plt.ylabel('Counts')
#plt.xticks(range(500,1030,10))
plt.xticks(rotation=90)
plt.grid()


# ## Save Histogram Data

# In[11]:

ener1.to_csv('Am.csv')
ener2.to_csv('Pu.csv')
ener3.to_csv('Cf.csv')


# In[ ]:



