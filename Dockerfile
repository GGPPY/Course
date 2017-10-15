FROM python:2.7-slim
WORKDIR /app
ADD . /app
RUN pip install -r requirement.txt -i https://pypi.douban.com/simple
EXPOSE 80 5000
ENV NAME World
CMD ["python", "manage.py", "runserver", "-h", "0.0.0.0", "-p" , "80"]