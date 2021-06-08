FROM python:3.6-slim

EXPOSE 8000

RUN apt update && apt install -y \
    gcc \
    g++ \
    hunspell \
    libhunspell-dev \
    git \
    wget \
&& rm -rf /var/lib/apt/lists/*

RUN pip install -U pip

RUN pip install \
    profanity-filter[deep-analysis,web]~=1.3.0 \
    git+https://github.com/rominf/hunspell_serializable@49c00fabf94cacf9e6a23a0cd666aac10cb1d491#egg=hunspell_serializable \
    git+https://github.com/rominf/pyffs@6c805fbfd7771727138b169b32484b53c0b0fad1#egg=pyffs

RUN python -m spacy download en

WORKDIR /usr/local/lib/python3.6/site-packages/profanity_filter/data/

RUN wget https://raw.githubusercontent.com/LibreOffice/dictionaries/master/en/en_US.aff
RUN wget https://raw.githubusercontent.com/LibreOffice/dictionaries/master/en/en_US.dic
RUN mv en_US.aff en.aff
RUN mv en_US.dic en.dic

CMD ["uvicorn", "profanity_filter.web:app", "--reload", "--host=0.0.0.0"]
