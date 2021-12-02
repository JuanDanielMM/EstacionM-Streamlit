FROM python:3.7
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8093
COPY . /app
ENTRYPOINT ["streamlit", "run"]
CMD ["EMGraficasTuneado.py"]
