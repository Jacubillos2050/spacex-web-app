import lambda_function

event = {}  # Simula una invocación manual
context = None
response = lambda_function.lambda_handler(event, context)
print(response)