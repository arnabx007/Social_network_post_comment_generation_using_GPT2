FROM python:3
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Download MongoDB via Docker
RUN export MONGODB_VERSION=4.0
RUN curl -O --remote-name-all https://raw.githubusercontent.com/docker-library/mongo/master/$MONGODB_VERSION/{Dockerfile,docker-entrypoint.sh}

RUN export DOCKER_USERNAME=username
RUN chmod 755 ./docker-entrypoint.sh
RUN docker build --build-arg MONGO_PACKAGE=mongodb-enterprise --build-arg MONGO_REPO=repo.mongodb.com -t $DOCKER_USERNAME/mongo-enterprise:$MONGODB_VERSION .


# Download the gpt2 pytorch model and place it in the gpt2_medium folder
RUN curl --output pytorch_model.bin https://s3.amazonaws.com/models.huggingface.co/bert/gpt2-pytorch_model.bin && mv pytorch_model.bin $app/gpt2_medium

# Download the entity extraction model
RUN python -m spacy download en_core_web_sm

CMD [ "python", "manage.py", "runserver"]