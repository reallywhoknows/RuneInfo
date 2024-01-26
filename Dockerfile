FROM Python:3.9

WORKDIR /
COPY requirements.txt .
COPY . .

RUN python3 -m pip install requirements.txt
CMD ["python", "./app.py"]