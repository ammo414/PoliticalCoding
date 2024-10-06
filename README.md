## Political Coding

A project to ingest congressional data from the Library of Congress's API and political news from Perignon's News API. The intent is to then contrast the topics of interest for these two groups to find descrepancies.

Uses Airflow to load data daily into a PostGreSQL database (SQL connection is still a to-do).

~~EDIT: Because my Perignon trial expired, this project is on hold.~~

Currently using an ad hoc Google News RSS to scrape political media data. After establishing a MVP, I'll work to scrape multiple rss feeds directly from each news source.

TODO:
- [ ] Complete HuggingFace integration for classifying data

- [ ] Add HuggingFace function into airflow

- [ ] Write unit tests
