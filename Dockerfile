FROM ubuntu
MAINTAINER david.hieber@uni-tuebingen.de
# update python version and replace python with python 3
RUN apt -y update && apt-get -y install software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && apt -y update && apt -y install git && \
    apt-get install -y python3.9 && apt install python-is-python3 && apt install -y python3-pip && \
    rm -rf /var/lib/apt/lists && \
    pip install pipenv

# install packages for train router

WORKDIR /opt/pht-email-service/

COPY Pipfile /opt/pht-email-service/Pipfile
COPY Pipfile.lock /opt/pht-email-service/Pipfile.lock

RUN pipenv install --system --deploy --ignore-pipfile && \
    pip install git+https://github.com/PHT-Medic/train-container-library.git

COPY src /opt/pht-email-service/src

CMD ["python", "-u", "/opt/pht-email-service/src/MessageConsumer.py"]
