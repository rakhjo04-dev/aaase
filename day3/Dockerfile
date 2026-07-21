FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir langchain-openai langgraph python-dotenv fastapi uvicorn

EXPOSE 8000

CMD ["python", "lab_prototype_to_enterprise.py", "serve"]