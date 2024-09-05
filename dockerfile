FROM python:3.12 

COPY requirements.txt /src/
RUN pip install --no-cache-dir -r /src/requirements.txt --break-system-packages

WORKDIR /app    

COPY /src /app

EXPOSE 8000

#CMD ["sh", "-c", "while true; do sleep 3600; done"]
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]