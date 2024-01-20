FROM python:3.9-slim-buster

# Create a virtual environment
RUN python3 -m venv venv --python=python3.9

# Activate the virtual environment
ENV PATH="/venv/bin:$PATH"

# Copy the application files
COPY app.py /app

# Install the application dependencies
RUN pip install -r /app/config/requirements.txt

# Set the entrypoint
ENTRYPOINT ["streamlit run", "/app/app.py"]
