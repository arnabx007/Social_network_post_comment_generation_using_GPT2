# Social Network Comment Generation using GPT2
This is a demo project that generates comment for a social network post. It has following features:
* Detects the entities in the given post such as location, company, person, date etc.
* Detects the category of the post. It can detect up to 8 categories: technology, business, entertainment, sports, world, health, nation & science.
* Generates unique comments everytime you generate a comment. 
* The web app also has a REST api for retrieving and putting new entries.

![alt text](https://github.com/arnabx007/Social_network_post_comment_generation_using_GPT2/blob/master/sample.gif "")

### Underneath the hood:
* OpenAI's pretrained NLG model **GPT2-Medium** (345M parameters)has been used for comment generation. Read the paper [here](https://github.com/openai/gpt-2). Huggingface's transformer library has been used to load the model and generate texts.
* An **ALBERT** model fine-tuned on category detection detects the category of the post. [albert-base-v2](https://huggingface.co/albert-base-v2) model is has been fine-tuned on this [Topic Labeled News Dataset](https://www.kaggle.com/kotartemiy/topic-labeled-news-dataset) from Kaggle.
* The **en_core_web_sm**, multi-task CNN [model](https://github.com/explosion/spacy-models/releases/tag/en_core_web_sm-3.1.0) trained on OntoNotes, with GloVe vectors trained on Common Crawl, does the entity extraction task.
* The web app automatically stores the post and the generated comment in a MongoDB database and checks for uniquness of the generated comment.
* The web app is built using Django framework. 
* The REST api is built using Django-REST framework. 


## Running locally 

### Option 1 - Using a virtual environment

1. Clone the repository.

2. Create a virtual environment with Python 3.8.6.

3. Install the requirements files `pip install -r requirements.txt`

4. Download the gpt2 medium sized model from the following link, rename it to 'pytorch_model.bin' (transformers library expects the model in this name):
https://s3.amazonaws.com/models.huggingface.co/bert/gpt2-pytorch_model.bin

5. Place the model it in the **gpt2_medium** folder:

6. Run 'python -m spacy download en_core_web_sm' command to download spacy's entity extraction model.

7. Download and install MongoDB Enterprise Edition from https://www.mongodb.com/try/download/enterprise

6. Run the web app locally by executing `python manage.py runserver`. The default development URL is `https://127.0.0.1:8000/` (Django's default URL)

### Option 2 - Using Docker

1. Change the `DOCKER_USERNAME` in the Dockerfile. 

2. Build the Docker image: `docker build -t comment_gen` .

3. Run the image: `docker run -d comment_gen`. The URL will be `https://127.0.0.1:8000/`.

## Testing

Run `python -m unittest test.py` for running the test code for comment generation. 
The testcase is built on top of python's `unittest` module and runs test for unique comment generation. Change the `post` variable and it will run test cases for 2 generated comments not to be the same. 

## Future Features
* A Social media like web interface where unique comments will be generated and shown simultaneously. 
* Making use of the larger GPT2 model (1.5 Billion parameters), or the new and the largest NLG model GPT3 API.
* Having a swagger.
