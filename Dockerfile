FROM python:3
LABEL maintainer="ishanshrestha"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1 
WORKDIR /app

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app/
EXPOSE 8000