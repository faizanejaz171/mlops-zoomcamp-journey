# AWS Lambda ka official Python base image
FROM public.ecr.aws/lambda/python:3.9

# Apni Python script ko Lambda image ke andar copy karna
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Lambda ko batana ke konsa function run karna hai
CMD [ "lambda_function.lambda_handler" ]
