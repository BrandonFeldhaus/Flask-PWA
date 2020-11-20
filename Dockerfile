FROM python:3.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 65
ENTRYPOINT [ "python" ]
CMD ["app.py"]