# Metis Project 3 - What are the characteristics of the democratic electorate?

## Objective and Audience
The contrived audience for this project was a political pundits, operatives and campaigns invested in the Democratic Presidential Primary. As such, they would be interested in what the democratic electorate cared about and and if there were any differences between the supporters of various candidates.

## Data
I fetched six months worth of Reddit comments from the Push Shift API. I wanted to analyze posts and comments on social media and Reddit provided the most accessible data. I chose r/Democrats and r/PoliticalDiscussion because of their popularity and likelihood of having active democratic voters. I also scraped each subreddit for the leading presidential candidates.

## Scope
This was a two week, independent project using natural language processing and unsupervised learning techniques. Given these constraints, I focused on topic modeling the various subreddits, clustering the users, and then comparing which clusters were most active on which candidate's subreddit. This would allow me to find differences among each candidate's support.

## NLP and Unsupervised Techniques
After pre-processing using stop words, lemmitisation, and other techniques, I used non-negative matrix factorization to model topics on each of the various subreddits. I also used the VADER and the IBM Watson API to get sentiment and tonality of the comments. Using the prevelance of the topics and these features I clustered the users into four distinct groups using K-Means.

## Interpretation
The first and most obvious insight was that the moderate and progressive split that dominated much of the coverage on the presidential primary was reflected in the topics discussed on the subreddits. In addition, healthcare was a salient way to distinguish beetween the two groups.

However, this analysis had relatively limited usefulness in terms of targeting likely supporters through reddit. For instance, the users who spoke the most frequently about racial justice were most likely to be active on Pete Buttigieg's subreddit. Given the negative press Buttigieg's campaign received on the issue of race, this more likely an indication that the analysis needs to be much more granular and use parts of speech tagging to understand who is truly supportive of a candidate. Simply being active on a subreddit is likely and inadequate proxy for support.

One potential opportunity is the cluster of users who predominantly post negative comments about the impeachment proceedings but are not active on any campaign subreddit. These users that are engaged in Democratic politics at large could be targeted to engage with particular candidate's reddit community.

To view more specific results, please review my [slide deck](https://docs.google.com/presentation/d/1p3QZbj4DUJHJWmfpIw5MU_Qe5C66iX63aUDNr64zV7o/edit?usp=sharing).
