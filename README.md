## Political Coding

Is there a difference in what senators and representatives are discussing in congress and what is being discussed in the news? The best way to answer that is by collecting immense amounts of data from both sources, classifying topics, and comparing the overall landscape of what each group is discussing.

This is a project to ingest congressional data from the [Library of Congress's API]([https://api.data.gov/docs/developer-manual/]) and political news from ~~Perignon's News API~~. a Google News rss feed and to classify topics with ~~Perplexity's LLM~~ a [pretrained Huggingface model](https://huggingface.co/poltextlab/xlm-roberta-large-english-legislative-cap-v3). We use [Airflow](https://airflow.apache.org/) to load data into a PostGreSQL database daily, which will then be connected to a [Superset](https://superset.apache.org/) instance for analysis.

~~EDIT: Because my Perignon trial expired, this project is on hold.~~

Currently using an ad hoc Google News RSS to scrape political media data. After establishing a MVP, I'll work to scrape multiple rss feeds directly from each news source.

TODO:
- [ ] enum everywhere

- [ ] package libraries properly

- [ ] Write unit tests

- [ ] Document PostGre queries and screenshots of visualizations
