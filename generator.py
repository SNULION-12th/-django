# importing the function from utils
from django.core.management.utils import get_random_secret_key

# generating and printing the SECRET_KEY
secret_key = get_random_secret_key()

print(secret_key)