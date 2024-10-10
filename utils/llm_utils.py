from openai import OpenAI
import time
import article_objects
import torch
import pandas as pd
from transformers import (AutoModelForSequenceClassification, AutoTokenizer, 
                          Trainer, TrainingArguments)
from datasets import Dataset

from db_utils import PostGreManager
import constants

"""
LLM functions. If more functions are needed, or if we want to use different models, keep them here
"""

def send_to_open_ai(news_article: article_objects.News):
    """
    function to query open_ai llm models 
    in this case, perplexity is piggybacking off of openAi's library
    if llm is needed for tasks other than labeling news articles, then a refactor is needed
    """

    title = news_article.get_title()
    description = news_article.get_description()

    chat_news_text = title + '.' + description
    chat_request_text = f'text:{chat_news_text}.\n Possible categories: macroeconomics, civil rights, health, agriculture, labor, education, \
        environment, energy, immigration, transportation, law and crime, social welfare, housing, domestic commerce, defense, \
        technology, foreign trade, international affairs, government operations, public lands, culture. \n Select a single category.'

    message = [
        {
            'role': 'system',
            'content': (
                'You are to catalog political headlines into exactly one of a number of categories. Please identify the best category for each headline and respond with only that. If no category is appropriate, say "0" and nothing else.'
            ),
        },
        {
            'role': 'user',
            'content': ( chat_request_text ),
        },
    ]

    llm_api_key = constants.LLM_API_KEY
    llm_base_url = constants.LLM_URL
    llm_model = constants.MODEL

    time.sleep(2)

    client = OpenAI(api_key=llm_api_key, base_url=llm_base_url)

    response = client.chat.completions.create(
        model = llm_model,
        messages=message
    )

    ## perplexity's response structure. update this is using a model with a different structure
    return response['choices']['0']['message']['content']


def send_bill_to_hugging_face(bill_article: article_objects.Bill):
    
    """
    llm function to send a BILL through a huggingface model to get CAP coded. 
    More information on the model here:
    https://figshare.com/s/8e3e9d1ae22c07869d6d
    https://huggingface.co/poltextlab
    https://capbabel.poltextlab.com/
    """

    



    
    pass


def send_news_to_hugging_face(news_article: article_objects.Bill):

    pass


def batch_news_to_hugging_face():

    
    query = "SELECT article_id, description, cap_code FROM news WHERE cap_code = -1;"
    
    db = pgm(constants.db_config)
    df = pd.read_sql(query, db.connect())
    hg_data = Dataset.from_pandas(df)

    #tokenized dataset
    dataset = hg_data.map(lambda df: AutoTokenizer.from_pretrained("xlm-roberta-large")(df['description'], max_length=MAXLEN, truncation=True, padding='max_length'), batched=True, remove_columns=hg_data.column_names)

    model = AutoModelForSequenceClassification.from_pretrained("poltextlab/xlm-roberta-large-english-media-cap-v3",
                                                               num_labels=num_labels,
                                                               problem_type="multi_label_classification",
                                                               ignore_mismatched_sizes=True
                                                               )
    
    #figure out how to actually get predictions
    #figure out how to add predictions to database

def batch_bills_to_hugging_face():

    """
    When first querying bills, there's no guarantee that we will have a description of the text/that the body of the bill 
    has already been transcripted. we're making do with what we have (title, policy area) if we decide to use this
    """

    query = "SELECT number, title, policy_area FROM bills WHERE cap_code = -1;" # is -1 actually used?

    db = pg(constants.db_config)
    df = pd.read_sql(query, db.connect())
    df['text'] = df['title'] + df['policy_area']

    hg_data = Dataset.from_pandas(df)

    #tokenized dataset
    dataset = hg_data.map(lambda df: AutoTokenizer.from_pretrained("xlm-roberta-large")(df['text'], max_length=MAXLEN, truncation=True, padding='max_length'), batched=True, remove_columns=hg_data.column_names)

    model = AutoModelForSequenceClassification.from_pretrained("poltextlab/xlm-roberta-large-english-legislative-cap-v3",
                                                                num_labels=num_labels,
                                                                problem_type="multi_label_classification",
                                                                ignore_mismatched_sizes=True
                                                                )
    
    #figure out how to actually get predictions
    #figure out how to add predictions to database