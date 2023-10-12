FROM python:3.10.12
ENV PYTHONUNBUFFERED=1
#RUN pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN mkdir /app
COPY . /app
WORKDIR /app
EXPOSE 8000
CMD sh ./run.sh
