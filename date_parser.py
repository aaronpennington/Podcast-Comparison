import pandas as pd
import plotly.graph_objects as go
import datetime
import numpy as np
import feedparser
from collections import Counter

# RSS LINKS:
# http://nodumbqs.libsyn.com/rss
# http://www.hellointernet.fm/podcast?format=rss

podcast_urls = ["http://www.hellointernet.fm/podcast?format=rss", "http://nodumbqs.libsyn.com/rss", "https://www.unmade.fm/episodes?format=rss"]

ndq_url = "http://nodumbqs.libsyn.com/rss"
hi_url = "http://www.hellointernet.fm/podcast?format=rss"
up_url = "https://www.unmade.fm/episodes?format=rss"


def get_release_dates(url):
    # open url and get xml doc
    response = feedparser.parse(url)

    #get release dates from the xml
    dates = []
    for post in response.entries:
        timedate = pd.to_datetime(post.published)
        dates.append(timedate.date())

    return dates


def get_podcast_title(url_list):
    title_list = []
    for url in url_list:
        response = feedparser.parse(url)
        title_list.append(response.feed.title)
    return title_list


def generate_heatmap():
    # Plot a heatmap of release dates
    np.random.seed(1)

    # Y AXIS (Podcast Titles)
    podcasts = get_podcast_title(podcast_urls)

    # Get the release date for episode 1
    hi_dates = get_release_dates(podcast_urls[0])
    ndq_dates = get_release_dates(podcast_urls[1])
    up_dates = get_release_dates(podcast_urls[2])
    start = hi_dates[len(hi_dates)-1]

    # Get the number of days between the first episode and today
    end = datetime.datetime.today().date()
    date_diff = (end-start).days

    print("START DATE: " + str(start))
    print("TODAY DATE: " + str(end))
    print("DATE DIFF = " + str(date_diff))

    # pandas date range
    dates = pd.date_range(start, end, freq='D')

    # counter for date we need counted
    hi_counts = Counter(pd.to_datetime(hi_dates))
    ndq_counts = Counter(pd.to_datetime(ndq_dates))
    up_counts = Counter(pd.to_datetime(up_dates))

    # build a list using a list comprehension of counts at all dates in range
    hi_date_freq = []
    ndq_date_freq = []
    up_date_freq = []
    for d in dates:
        hi_date_freq.append(hi_counts[d])
        ndq_date_freq.append(ndq_counts[d])
        up_date_freq.append(up_counts[d])

    z = [hi_date_freq, ndq_date_freq, up_date_freq]

    # Create the heatmap figure
    fig = go.Figure(data=go.Heatmap(
            z=z,
            x=dates,
            y=podcasts,
            colorscale='Portland'))
    # Colorscale may be any from a list of the following: Greys,YlGnBu,Greens,YlOrRd,Bluered,RdBu,Reds,Blues,Picnic,
    # Rainbow,Portland,Jet,Hot,Blackbody,Earth,Electric,Viridis,Cividis

    fig.update_layout(
        title='Episode Release Dates',
        xaxis_nticks=3)

    fig.show()


if __name__ == "__main__":
    generate_heatmap()
