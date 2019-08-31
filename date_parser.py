import pandas as pd
import plotly.graph_objects as go
import datetime
import numpy as np
import feedparser
from collections import Counter

# RSS LINKS:
# http://nodumbqs.libsyn.com/rss
# http://www.hellointernet.fm/podcast?format=rss

# Initialize 2 lists of dates for the podcasts
hi_dates = []
ndq_dates = []

ndq_url = "http://nodumbqs.libsyn.com/rss"
hi_url = "http://www.hellointernet.fm/podcast?format=rss"

ndq_response = feedparser.parse(ndq_url)
hi_response = feedparser.parse(hi_url)

# PARSE NDQ FEED
for post in ndq_response.entries:
    # print(post)
    timedate = pd.to_datetime(post.published)
    ndq_dates.append(timedate.date())

print("*************************")

# PARSE HI FEED
for post in hi_response.entries:
    # print(post)
    timedate = pd.to_datetime(post.published)
    hi_dates.append(timedate.date())

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
