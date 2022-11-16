# Configuración para levantar el FastAPI desde ubuntu

# FROM ubuntu

# ENV DEBIAN_FRONTEND=noninteractive

# WORKDIR /code

# RUN apt-get update

# RUN apt-get install -y p7zip wget make gcc

# RUN wget https://www.python.org/ftp/python/3.9.6/Python-3.9.6.tgz
# RUN tar xzvf Python-3.9.6.tgz
# RUN cd Python-3.9.6 \
#     && ./configure \
#     && make \
#     && make install
# RUN apt-get install python3-pip

# RUN cd /usr/local/bin \
#     && ln -s /usr/bin/python3.9.6 python \  
#     && pip3 --no-cache-dir install --upgrade pip \
#     && rm -rf /var/lib/apt/lists/*

# COPY ./requirements.txt /code/requirements.txt

# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# RUN 7za x Citas_RN.zip.001

# COPY ./ /code
 
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

# Configuración para levantar el FastAPI directamente con Python 3.9.6
FROM python:3.9.6

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

ENV PYHTONUNBUFFERED=1

RUN python -m pip install --upgrade pip

#RUN pip install -U --no-cache-dir -r /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./ /code

RUN python -m decompress Citas_RN.zip /code/Citas_RN.h5

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]