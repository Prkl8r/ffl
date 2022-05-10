# For more information, please refer to https://aka.ms/vscode-docker-python
FROM alpine:3.15

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN apk add --update py3-pip
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
#RUN adduser -u 5678 --disabled-password --gecos "" -D appuser
RUN adduser -D appuser
#COPY --chown=appuser:appuser . /app
RUN chown -R appuser:appuser /app
RUN chmod -R 755 .
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi"]

