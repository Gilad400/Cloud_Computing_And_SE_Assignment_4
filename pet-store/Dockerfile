FROM python:alpine3.17

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY pet-store.py .

ARG STORE_ID
ENV STORE_ID=${STORE_ID}
ENV NINJA_API_KEY=SraBF/za+qf7A4j4VCS3Tg==QVrQZLNr9qnIDVId

EXPOSE 8000

CMD ["python", "pet-store.py"]