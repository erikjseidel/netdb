FROM python:3.11
WORKDIR /netdb/app
COPY ./requirements.txt /netdb/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /netdb/requirements.txt
COPY ./netdb /netdb/app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
