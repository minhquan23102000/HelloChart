FROM python:3.9.5-slim

  #Create workdir
  WORKDIR /app
  COPY . ./

  #Install librareies
  RUN pip install --upgrade pip && pip install  --no-cache-dir -r requirements.txt \
    && rm -rf requirements.txt

  #Run app
  CMD ["streamlit", "run", "app.py"]
