import constants
from openai import OpenAI
import time
import article_objects
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch



"""
LLM functions. If more functions are needed, or if we want to use different models, keep them here
"""

def send_to_open_ai(news_article: article_objects.News):
    """
    function to query open_ai llm models 
    in this case, perplexity is piggybacking off of openAi's library
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

    llm_api_key = constants.OPEN_AI_API_KEY
    llm_base_url = constants.OPEN_AI_URL
    llm_model = constants.OPEN_AI_MODEL

    time.sleep(2)

    client = OpenAI(api_key=llm_api_key, base_url=llm_base_url)

    response = client.chat.completions.create(
        model = llm_model,
        messages=message
    )

    ## perplexity's response structure. update this is using a model with a different structure
    return response['choices']['0']['message']['content']

def classify_text_with_huggingface(text, which_data):
    """
    takes text and returns cap_code 
    """
    # load correct model
    if which_data == 'bill':
        model_name = "poltextlab/xlm-roberta-large-english-legislative-cap-v3"
    elif which_data == 'news':
        model_name = "poltextlab/xlm-roberta-large-english-medica-cap-v3"

    else:
        print("Article type mismatch.")
        return -1 # never a cap code
    model = AutoModelForSequenceClassification()

    # tokenize
    # it looks like both models use the same tokenizer
    tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-large")

    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding=True)

    #infer
    with torch.no_grad():
        outputs = model(**inputs)
        # model is where the two models differ, surprisingly enough

    # get prediction as class
    predicted_class = torch.argmax(outputs.logits, dim=1).item()

    # convert from class to label
    label = model.config.id2label[predicted_class]

    return label

