FROM python:3.9.5-slim

  #Environment variable
  ENV APP_HOME /app
  ENV APP_PORT 5000

  #Create workdir
  WORKDIR $APP_HOME
  COPY . ./

  #Install librareies
  RUN pip install --upgrade pip && pip install  -r requirements.txt \
    && rm -rf requirements.txt


  #Run app
  EXPOSE $APP_PORT
  CMD ["streamlit", "run", "app.py", "--server.port", "${APP_PORT}"]
