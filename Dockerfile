FROM python:3.10.6-slim
# Path: flask/Dockerfile

# set working directory
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirement.txt .

# update pip indexs
# RUN pip install --upgrade pip

# install app dependencies
RUN pip install -r requirement.txt

# copy the content of the local src directory to the working directory
COPY . /app

# install app dependencies
RUN pip install -r requirement.txt

# expose port
EXPOSE 5000

# start app
CMD ["python", "app.py"]