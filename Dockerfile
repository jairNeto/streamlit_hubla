FROM python:3.9-slim

COPY ./requirements.txt /requirements.txt

RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir --upgrade pip setuptools && \
    pip3 install --no-cache-dir -r /requirements.txt

COPY ./srcs /srcs

ENTRYPOINT ["streamlit", "run"]

CMD ["/srcs/app.py"]

EXPOSE 8501