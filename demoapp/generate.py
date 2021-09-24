import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import transformers
transformers.logging.set_verbosity_error()

import torch
import spacy
from transformers import pipeline, set_seed
import re
import tensorflow as tf
import tensorflow.keras as keras
import numpy as np

from .utils import get_db, get_collection


# text = "Post: The cyclone has hit hard at the west coast of California. Comment:"
# text = "Mr. Anderson has reached New York safely. He will be giving the keynote speech at 10 am sharp."

# Initiate the Named Entity Recognition model
nlp = spacy.load('en_core_web_sm')

# Category detection
# Albert tokenizer
albert_tokenizer = transformers.AutoTokenizer.from_pretrained('./detect_category/albert_base_v2/')
# Albert base v2 model
albert_model = transformers.AlbertModel.from_pretrained('./detect_category/albert_base_v2/')
# Pretrained neural network for category detection
nn = keras.models.load_model('./detect_category/category_model.h5')

target_encoding = {'NATION':0, 'BUSINESS':1, 'TECHNOLOGY':2, 'SPORTS':3, 'ENTERTAINMENT':4, 'WORLD':5, 'HEALTH':6, 'SCIENCE':7}
target_decoding = {v:k for k,v in target_encoding.items()}

# Inititate the text-generation pipeline
gpt_tokenizer = transformers.AutoTokenizer.from_pretrained('./gpt2_medium/')
generator = pipeline('text-generation', model='./gpt2_medium/')
set_seed(42)

# Get the database
db, client = get_db(db_name = 'generated_comment_db')
# Get the collection
coll = get_collection(db, 'comments')

def ner(text):
    # Extract the entitites
    doc = nlp(text)
    
    ner_dict = {tok.text:tok.label_ for tok in doc.ents}
    return ner_dict 

def detect_category(text):

    # Get albert's last layer embeddings for the text 
    albert_output = albert_model(albert_tokenizer(text, return_tensors='pt')['input_ids'])
    # Feed the 768 dimensional embedding to the pretrained neural network
    x = np.array(albert_output[0].tolist()[0][0]).reshape(1,-1)
    y = nn.predict(x).tolist()[0]
    y = np.argmax(y)
    prediction = target_decoding[y]
    
    return prediction

# Generate a comment and check if unique
def generate_comment(text):
    raw_text = text
    text = 'Post: '+text+ ' Comment:'
    length = len(gpt_tokenizer(text)['input_ids'])

    for num in range(1,11):
        outputs = generator(text, max_length=length+50, num_return_sequences=num)

        for gen in outputs:
            comment = gen['generated_text'].split('Comment:')[1]
            comment = postprocess_comment(comment)

            old = store(raw_text, comment)
            if old==False:
                break

        if old==False:
            # print(comment)
            break

    return comment

# Store the post and the comment in 'generated_comment_db' database under the 'comments' collection
# Also check if the comments are unique
# Returns the flag old=False if the comment is new
def store(post: str, comment:str):
    data = {'post': post, 'comment': comment}

    if list(coll.find(data))==[]:
        print('new entry')
        coll.insert_one(data)
        old = False
        
    else:
        old = True
        print('already in database')

    return old 

def postprocess_comment(comm):

    end_index =-1

    for i in range(-1, -len(comm), -1):
        if comm[i] in ['.', '!', '?']:
            end_index = i+1
            break

    comm = comm[:end_index]
    return comm

