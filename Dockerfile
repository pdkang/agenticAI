FROM public.ecr.aws/amazonlinux/amazonlinux:latest
RUN yum install python3 pip -y && yum update -y
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
CMD ["python3", "financial_agent.py"]
EXPOSE 8080