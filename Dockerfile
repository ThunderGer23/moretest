FROM python:3.9.6

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

ENV PYHTONUNBUFFERED=1

RUN python -m pip install --upgrade pip

RUN pip install -U --no-cache-dir -r /code/requirements.txt

COPY ./ /code

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]