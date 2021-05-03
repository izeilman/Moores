import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import os
os.chdir(os.path.realpath(__file__)[:-(len(os.path.basename(__file__)))])

# Read html data into pandas
# table = pd.read_html('https://en.wikipedia.org/wiki/Transistor_count')

# Save it through pickle
# pickle.dump(table, open("html_data", "wb" ))

# load the data into a pandas data frame
table = pickle.load(open("html_data", "rb" ))
df = pd.DataFrame(table[1]) # using the data from table at index 1

# print(df.columns)
# prints:
# Index(['Processor', 'MOS transistor count', 'Date ofintroduction', 'Designer',
# 'MOS process(nm)', 'Area (mm2)'],
# dtype='object')

# function to clean up the numbers in the data frame
def sanitize_num(x):
    d = ""
    for i in x:
        if i == ",":
            pass
        elif i in [str(x) for x in range(10)]:
            d += i
        else:
            break
    try:
        return int(d)
    except:
        pass


# drop unused data
df = df.drop(columns = ['Processor', 'Designer', 'Area (mm2)'])

# clean up the naming
df = df.rename(columns = {'MOS transistor count': 'transistor count',
                          'MOS process(nm)': 'size(nm)',
                          'Date ofintroduction' : 'year'})

# apply sanitize_num to the data frame
df = df.applymap(lambda x: sanitize_num(x))

# set the index to the year
df = df.set_index("year")

# check to see if everything looks good
# print(df.head)

# store in csv
df.to_csv("MooresData.csv")

# display the colomns as scatter plots
fig, axes = plt.subplots(df.columns.size, 1)
for c, i in enumerate(df.columns):
    axes[c].set_title(i)
    axes[c].ticklabel_format(style='plain')
    axes[c].scatter(df[i].index.tolist(), df[i].values.tolist(), s = 8)
plt.tight_layout()
plt.show()

# Show the transistor scatter plot with the ngram results for distributed processing and multiprocessing
# ngram data pulled into csv using tool from econpy https://github.com/econpy/google-ngrams pull #18
ts = pd.read_csv('distributedprocessing_multiprocessing-eng_2012-1970-2019-3-caseSensitive.csv',index_col=0,parse_dates=True)
fig, axes = plt.subplots(2, 1)
axes[0].scatter(df['transistor count'].index.tolist(), df['transistor count'].values.tolist(), s = 8)
axes[0].set_title("Transistor count")
axes[1].plot(ts)
axes[1].legend(["Distributed Processing", "Multiprocessing"])
plt.show()
