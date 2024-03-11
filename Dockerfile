FROM python:3.12.0-slim

RUN mkdir /Lottery

WORKDIR /Lottery

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/Lottery/app"
ENV PYTHONPATH "${PYTHONPATH}:/Lottery/BOT"


COPY . .

#RUN chmod a+x /Lottery/docker/*.sh

CMD ["uvicorn", "app.main:app", "--reload", "--workers", "1", "--host", "0.0.0.0", "--port", "8000"]

