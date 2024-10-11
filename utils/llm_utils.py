"""Module of all LLM functions"""

import torch
from transformers import (AutoModelForSequenceClassification, AutoTokenizer)


def classify_text_with_huggingface(text, which_data):
    """
    takes text and returns cap_code with huggingface's 
    """
    # load correct model
    if which_data == 'bill':
        model_name = "poltextlab/xlm-roberta-large-english-legislative-cap-v3"
    elif which_data == 'news':
        model_name = "poltextlab/xlm-roberta-large-english-media-cap-v3"

    else:
        print("Article type mismatch.")
        return -1 # never a cap code

    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    # tokenize
    # both models use the same tokenizer
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

    return label_crossmap(label)


def label_crossmap(label):
    """
    https://www.comparativeagendas.net/pages/master-codebook
    """

    crossmap= {
        'LABEL_0':'Macroeconomics',
        'LABEL_1':'Civil Rights',
        'LABEL_2':'Health',
        'LABEL_3':'Agriculture',
        'LABEL_4':'Labor',
        'LABEL_5':'Education',
        'LABEL_6':'Environment',
        'LABEL_7':'Energy',
        'LABEL_8':'Immigration',
        'LABEL_9':'Transportation',
        'LABEL_10':'Law and Crime',
        'LABEL_11':'Social Welfare',
        'LABEL_12':'Housing',
        'LABEL_13':'Domestic Commerce',
        'LABEL_14':'Defense',
        'LABEL_15':'Technology',
        'LABEL_16':'Foreign Trade',
        'LABEL_17':'International Affairs',
        'LABEL_18':'Government Operations',
        'LABEL_19':'Public Lands',
        'LABEL_20':'Culture',
        'LABEL_21':'None Available'
    }

    return crossmap[label]
