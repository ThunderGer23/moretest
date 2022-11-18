# Configuración para levantar el FastAPI desde tensorflow
FROM ubuntu:18.04
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /code

RUN apt-get update
RUN apt-get install -y wget make gcc gnupg2 gnupg gnupg1
RUN apt-key del 7fa2af80
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-keyring_1.0-1_all.deb
RUN dpkg -i cuda-keyring_1.0-1_all.deb
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub

RUN apt-get update \
  && apt-get install -y python3 python3-distutils python3-pip \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 --no-cache-dir install --upgrade pip \
  && rm -rf /var/lib/apt/lists/* 

RUN pip3 --no-cache-dir install --upgrade pip \
    && rm -rf /var/lib/apt/lists/*
RUN export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/cuda/lib64

COPY ./ /code

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
#RUN 7za x Citas_RN.zip.001
RUN python -m decompress Citas_RN.zip /code/Citas_RN.h5
 
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

# Configuración para levantar el FastAPI directamente con Python 3.9.6
# FROM python:3.9.6

# WORKDIR /code
# RUN apt-get update \
#     && apt-get install cudatoolkit cudnn tensorflow tensorflow-gpu


# COPY ./requirements.txt /code/requirements.txt

# ENV PYHTONUNBUFFERED=1

# RUN python -m pip install --upgrade pip

# #RUN pip install -U --no-cache-dir -r /code/requirements.txt

# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# COPY ./ /code

# RUN python -m decompress Citas_RN.zip /code/Citas_RN.h5
# RUN export LD_LIBRARY_PATH=/usr/local/cuda-10.1/compat/:$LD_LIBRARY_PATH

# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]