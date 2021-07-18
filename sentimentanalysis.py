
import json
import pandas as pd
from datetime import datetime
from datetime import timedelta
import time
import requests
from matplotlib import  pyplot as plt
import numpy as np
import tensorflow as tf
from nltk.tokenize import sent_tokenize
from random import randint
import matplotlib.pyplot as plt
import csv
import sys
import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import transformers


class InputExample(object):
    def __init__(self, guid, text, label=None, agree=None):
        self.guid = guid
        self.text = text
        self.label = label
        self.agree = agree


class InputFeatures(object):
    def __init__(self, input_ids, attention_mask, token_type_ids, label_id, agree=None):
        self.input_ids = input_ids
        self.attention_mask = attention_mask
        self.token_type_ids = token_type_ids
        self.label_id = label_id
        self.agree = agree


def convert_examples_to_features(examples, label_list, max_seq_length, tokenizer, mode='classification'):
    if mode == 'classification':
        label_map = {label: i for i, label in enumerate(label_list)}
        label_map[None] = 9090

    features = []
    for (ex_index, example) in enumerate(examples):
        tokens = tokenizer.tokenize(example.text)

        if len(tokens) > max_seq_length - 2:
            tokens = tokens[:(max_seq_length // 4) - 1] + tokens[
                                                          len(tokens) - (3 * max_seq_length // 4) + 1:]

        tokens = ["[CLS]"] + tokens + ["[SEP]"]

        token_type_ids = [0] * len(tokens)

        input_ids = tokenizer.convert_tokens_to_ids(tokens)

        attention_mask = [1] * len(input_ids)

        padding = [0] * (max_seq_length - len(input_ids))
        input_ids += padding
        attention_mask += padding


        token_type_ids += padding

        assert len(input_ids) == max_seq_length
        assert len(attention_mask) == max_seq_length
        assert len(token_type_ids) == max_seq_length
        label_id = label_map[example.label]
        agree = example.agree
        mapagree = {'0.5': 1, '0.66': 2, '0.75': 3, '1.0': 4}
        try:
            agree = mapagree[agree]
        except:
            agree = 0
        features.append(
            InputFeatures(input_ids=input_ids,
                          attention_mask=attention_mask,
                          token_type_ids=token_type_ids,
                          label_id=label_id,
                          agree=agree))
    return features
def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]
def softmax(x, axis=1):
    e_x = np.exp(x - np.max(x, axis=axis)[:, None])
    return e_x / np.sum(e_x, axis=axis)[:, None]
def merge_sentences_of_opinion(result, number_of_posts):
    text = ""
    #newResult = pd.DataFrame()
    for sentence in result['sentence']:
        text+=sentence
        text+=". "
    score_mean = result['sentiment_score'].mean()
    prediction = result['prediction'].mode().any()
    logit_means = [sum([sum(r) for r in result['logit']])]
    newResult = {
        'sentence':[text],'sentiment_score':[score_mean],
        'currency':[result['currency'][0]],'time':[result['time'][0]],
        'prediction':[prediction],'logit': logit_means,'number_of_posts':[number_of_posts]
    }
    newResult['prediction'] = result[result['sentiment_score']==result['sentiment_score'].max()]['prediction']
    #print(newResult)
    return pd.DataFrame(newResult)

def predict(text_and_postsn_lst, data,time,currency,dictionary,prev_result,model, tokenizer=None, write_to_csv=False, path=None):
    model.eval()
    sentences = sent_tokenize(text_and_postsn_lst[0])

    label_list = ['positive', 'negative', 'neutral']
    label_dict = {0: 'positive', 1: 'negative', 2: 'neutral'}
    result = pd.DataFrame(columns=['sentence', 'logit', 'prediction', 'sentiment_score'])
    for batch in chunks(sentences, 5):
        examples = [InputExample(str(i), sentence) for i, sentence in enumerate(batch)]

        features = convert_examples_to_features(examples, label_list, 64, tokenizer)

        all_input_ids = torch.tensor([f.input_ids for f in features], dtype=torch.long)
        all_attention_mask = torch.tensor([f.attention_mask for f in features], dtype=torch.long)
        all_token_type_ids = torch.tensor([f.token_type_ids for f in features], dtype=torch.long)

        with torch.no_grad():
            logits = model(all_input_ids, all_attention_mask, all_token_type_ids)[0]
            logits = softmax(np.array(logits))
            sentiment_score = pd.Series(logits[:, 0] - logits[:, 1])
            predictions = np.squeeze(np.argmax(logits, axis=1))

            batch_result = {'time': time,
                            'currency': currency,
                            'sentence': batch,
                            'logit': list(logits),
                            'prediction': predictions,
                            'sentiment_score': sentiment_score}

            batch_result = pd.DataFrame(batch_result)
            result = pd.concat([result, batch_result], ignore_index=True)
    result['prediction'] = result.prediction.apply(lambda x: label_dict[x])
    #print("============DICTIONARY==================================================")
    #print(dictionary)
    #print("============END_OF_DICTIONARY==================================================")
    #print("============RESULT==================================================")
    #print("============BEFORE==================================================")
    #print(result)
    result = merge_sentences_of_opinion(result, text_and_postsn_lst[1])
    #print("============AFTER==================================================")
    #print(result)
    #print("============END_OF_RESULT==================================================")

    if write_to_csv:
        result.to_csv(path, sep=',', index=False)
    else:
        dictionary[time][currency]['prediction']=list(result['prediction'])
        dictionary[time][currency]['sentiment_score']=list(result['sentiment_score'])
        dictionary[time][currency]['logit']=result['logit']
    if prev_result is not None:
        result.append(prev_result)
    #print(dictionary)
    return result
def predict_and_save(time,currency,data, dictionary,  result,model, tokenizer):
  output = "predictions{}{}.csv".format(time,currency)
  prediction = result
  for opinion in data:
    #print("PREDICTING {}".format(opinion))
    prediction = predict(opinion,data,time,currency,dictionary,result,model,tokenizer=tokenizer,write_to_csv=False,path=os.path.join("/content/sample_data",output))
  return prediction

def backTest(sentiments):
    for hour in sentiments:
        d = hour.split(" ")[0]

def downloadNewPostsFromSubreddit(subreddits, filename):
    posts = {}
    url="https://api.pushshift.io/reddit/search/submission/?subreddit={}&sort=desc&sort_type=created_utc&after={}&before={}&size=1000"
    now= datetime.now()
    then = now - timedelta(days=100)
    unixtimeFrom = time.mktime(then.timetuple())
    while then<=now:
        then = then + timedelta(hours=1)
        unixtimeTo = time.mktime(now.timetuple())
        fromKey = then.strftime("%m/%d/%Y, %H:%M:%S")
        print(fromKey)
        posts[fromKey] = {}
        for symbol in subreddits:
            try:
                print("Arguments {} {} {}".format(symbol,unixtimeFrom,unixtimeTo))
                data = requests.get(url.format(symbol,int(unixtimeFrom), int(unixtimeTo))).json()['data']
                print(symbol)
                posts[fromKey][symbol] = []
                for post in data:
                    if 'selftext' in post:
                        if post['selftext'] is not None and len(post['selftext'])!=0:
                            posts[fromKey][symbol].append([post['selftext'],post['num_comments']]) 
            except Exception as e:
                print(e)
                time.sleep(5)
        unixtimeFrom = unixtimeTo
        print(fromKey)
        with open(filename,'w') as f:
            json.dump(posts,f)
if __name__ =='__main__':
    #downloadNewPostsFromSubreddit(["Bitcoin","Dogecoin"],"Scraped-Posts3.json")
    with open("Scraped-Posts2.json",'r') as f:
        dataset = json.load(f)
    #print(dataset.keys(), len(dataset.keys()))    
    i=0
    dictionary = {}
    size = len(dataset)
    result = None
    i=0
    for hour in dataset:
        dictionary[hour] = {}

    transformers.logging.set_verbosity_error()
    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
    results=pd.DataFrame([])
    for hour in dataset:
        i+=1
        for currency in dataset[hour]:
            dictionary[hour][currency]= {}
            dictionary[hour][currency]['posts'] = dataset[hour][currency]
            result=predict_and_save(hour,currency,dataset[hour][currency], dictionary, result, model, tokenizer)
            results =pd.concat([results,result])
        print("SAVE RESULT {}".format(results))
        results.to_csv("sentiment2.csv", encoding='utf-8', index=False)