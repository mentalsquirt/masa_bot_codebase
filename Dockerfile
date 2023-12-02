FROM python:3.11
WORKDIR /app
ADD . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80
CMD ["python", "main.py"]

# docker build -t masa_bot .
# docker run -p 4000:80 --name masa -e TOKEN="**your_token**" -e REDIS_URL="redis://**your-redis-url**" masa_bot