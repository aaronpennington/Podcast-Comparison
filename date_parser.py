import xml.etree.ElementTree as ET
import pandas as pd
import plotly.graph_objects as go
import datetime
import numpy as np

# Initialize 2 lists of dates for the podcasts
hi_dates = []
ndq_dates = []

# PARSE NDQ FEED
tree = ET.parse('ndq_feed.xml')
root = tree.getroot()

for child in root:
    for item in child:
        for ep in item:
            if (ep.tag == "pubDate"):
                #print(ep.tag, ep.text)
                timedate = pd.to_datetime(ep.text)
                ndq_dates.append(timedate.date())

print("*************************")

# PARSE HI FEED
tree2 = ET.parse('hi_feed.xml')
root2 = tree2.getroot()

for child in root2:
    for item in child:
        for ep in item:
            if (ep.tag == "pubDate"):
                #print(ep.tag, ep.text)
                timedate = pd.to_datetime(ep.text)
                hi_dates.append(timedate.date())

ndq_file = open("ndq_dates.txt", "a")
hi_file = open("hi_dates.txt", "a")

# Write release dates for each episode of both podcasts to seperate files.
# print("NDQ: ")
for date in ndq_dates:
    # print(date)
    ndq_file.write(str(date))
# print("HI: ")
for date in hi_dates:
    # print(date)
    hi_file.write(str(date))

# Plot a heatmap of release dates
np.random.seed(1)

# Y AXIS
podcasts = ['Hello Internet', 'No Dumb Questions']

# Get the release date for episode 1
start = hi_dates[len(hi_dates)-1]

# Get the number of days between the first episode and today
end = datetime.datetime.today().date()
date_diff = (end-start).days

print("START DATE: " + str(start))
print("TODAY DATE: " + str(end))
print("DATE DIFF = " + str(date_diff))

# Plot those dates on the x-axis
dates = start + np.arange(date_diff) * datetime.timedelta(days=1)

# Distribute the frequencies of each day
# z = np.random.poisson(size=(len(podcasts), len(dates)))


from collections import Counter

# pandas date range
dates = pd.date_range(start, end, freq='D')

# counter for date we need counted
hi_counts = Counter(pd.to_datetime(hi_dates))
ndq_counts = Counter(pd.to_datetime(ndq_dates))
print("HI COUNTS: " + str(hi_counts))

# build a list using a list comprehension of counts at all dates in range
hi_date_freq = []
ndq_date_freq = []
for d in dates:
    hi_date_freq.append(hi_counts[d])
    ndq_date_freq.append(ndq_counts[d])

print(hi_date_freq)
z = [hi_date_freq, ndq_date_freq]

# Create the heatmap figure
fig = go.Figure(data=go.Heatmap(
        z=z,
        x=dates,
        y=podcasts,
        colorscale='Portland'))
# Colorscale may be any from a list of the following: Greys,YlGnBu,Greens,YlOrRd,Bluered,RdBu,Reds,Blues,Picnic,
# Rainbow,Portland,Jet,Hot,Blackbody,Earth,Electric,Viridis,Cividis

fig.update_layout(
    title='Episode Releases',
    xaxis_nticks=3)

fig.show()
