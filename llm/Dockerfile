#Using python
FROM python:3.9-slim
# Using Layered approach for the installation of requirements
RUN python -m pip install --upgrade pip

COPY ./app /app
# ENV PYTHONPATH "${PYTHONPATH}:/app/"
WORKDIR /app
#RUN pip install dash dash-bootstrap-components gunicorn #-r requirements.txt
#Copy files to your container
#COPY . ./
#Running your APP and doing some PORT Forwarding /home/shtabari/Documents/GitPage/dashapps/llm/app/requirements.txt
RUN pip install -r requirements.txt 
# RUN pip install google-api-core google-cloud-core grpcio grpcio-tools


EXPOSE 8080

CMD ["python", "app.py"]

