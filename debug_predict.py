import os
import django
from dotenv import load_dotenv

# Setup Django if needed or just load dotenv
load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crop_disease.settings')
django.setup()

from detection.views import predict_image
import traceback

try:
    print("Testing with API Key present:", bool(os.getenv("GEMINI_API_KEY")))
    result = predict_image('images/PD.jpg')
    print("Result:", result)
except Exception as e:
    traceback.print_exc()
