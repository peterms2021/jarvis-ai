FROM python:3.10-slim-bullseye

# Set the working directory
WORKDIR /app

# Copy the project files to the container
COPY . .

# Install the package using setup.py
RUN pip install -e .

# Install dependencies
RUN pip install pip -U && \
    pip install --no-cache-dir -r requirements.txt

# Set the environment variable
ARG OPENAI_API_KEY
ARG OPENAI_API_PROVIDER
ARG OPENAI_API_BASE
ARG OPENAI_API_ENGINE
ARG OPENAI_API_VERSION

ENV OPENAI_API_KEY=$OPENAI_API_KEY
ENV OPENAI_API_PROVIDER=$OPENAI_API_PROVIDER
ENV OPENAI_API_BASE=$OPENAI_API_BASE
ENV OPENAI_API_ENGINE=$OPENAI_API_ENGINE
ENV OPENAI_API_VERSION=$OPENAI_API_VERSION


# Expose the necessary ports
EXPOSE 8000

# Run the application
CMD ["uvicorn", "agents.main:app", "--host", "0.0.0.0", "--port", "8000"]
