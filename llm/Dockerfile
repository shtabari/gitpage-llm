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

#CMD gunicorn -b 0.0.0.0:80 app:server gcloud artifacts repositories describe gitpage --project=github-page-413420 --location=us-central1

# gcloud artifacts docker images list us-central1-docker.pkg.dev/github-page-413420/gitpage/dashapp-test [--include-tags] 
# docker run -p 4500:8080 --name frst-dash my-app
# docker tag dashapp-test us-central1-docker.pkg.dev/github-page-413420/gitpage/dashapp-test:latest

# gcloud artifacts repositories describe gitpage --project=github-page-413420 --location=us-central1

#  1624  rbenv local 3.0.6
#  1625  bundle exec jekyll serve
#  1626  bundle exec jekyll liveserve
#  1627  bundle exec jekyll serve -l