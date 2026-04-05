from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .models import UploadedImage
from .forms import ImageUploadForm, ImageURLForm
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

system_instruction = """You are an advanced AI system specialized in universal crop health analysis using agricultural image recognition.
Your task is to analyze any uploaded plant or crop image and generate an accurate crop health report.
Tasks to Perform
Detect and classify the crop/plant type from the image.
Analyze leaf, stem, fruit, or visible plant regions.
Determine whether the crop is:
Healthy
Diseased
If diseased:
Identify the disease name.
Estimate infection severity (%) based on visible damage area.
Describe detected symptoms.
Suggest basic treatment or preventive action.
If no disease is detected:
Mark status as Healthy Crop.
Provide crop name confirmation.
Severity Estimation Rule
0–10% → Very Mild
11–30% → Mild
31–60% → Moderate
61–100% → Severe
Output Format (STRICT JSON)
{
  "crop_name": "",
  "health_status": "Healthy | Diseased",
  "disease_name": "None if healthy",
  "infection_percentage": "0-100%",
  "severity_level": "Very Mild | Mild | Moderate | Severe",
  "symptoms_detected": "",
  "recommendation": "",
  "confidence_score": 0.0
}
Important Guidelines
Must work for any crop image, including unseen crops.
Base predictions only on visible image patterns.
Never leave fields empty.
If unsure, return the most probable prediction with lower confidence.
Keep explanations short and agriculture-focused.
Avoid generic answers.
"""


def home(request):
    return render(request, 'detection/index.html')

def upload(request):
    return render(request, 'detection/upload.html')

def weather_view(request):
    return render(request, 'detection/weather.html')

def upload_image(request):
    if request.method == 'POST':
        upload_form = ImageUploadForm(request.POST, request.FILES)
        if upload_form.is_valid():
            upload_form.save()
            uploaded_image = upload_form.instance
            result = predict_image(uploaded_image.image.path)
            if 'error' in result:
                return render(request, 'detection/upload_image.html', {
                    'upload_form': upload_form,
                    'error': result['error']
                })
            else:
                return render(request, 'detection/result.html', {
                    'class_name': result['class_name'],
                    'confidence': result['confidence'],
                    'image_url': uploaded_image.image.url,
                    'crop_name': result['crop_name'],
                    'health_status': result['health_status'],
                    'infection_percentage': result['infection_percentage'],
                    'severity_level': result['severity_level'],
                    'symptoms_detected': result['symptoms_detected'],
                    'recommendation': result['recommendation'],
                })
        else:
            return render(request, 'detection/upload_image.html', {
                'upload_form': upload_form,
                'error': 'Invalid form submission. Please try again.'
            })
    else:
        upload_form = ImageUploadForm()

    return render(request, 'detection/upload_image.html', {
        'upload_form': upload_form,
    })


def enter_url(request):
    if request.method == 'POST':
        url_form = ImageURLForm(request.POST)
        if url_form.is_valid():
            image_url = url_form.cleaned_data['image_url']
            result = predict_image(image_url)
            if 'error' in result:
                return render(request, 'detection/enter_url.html', {
                    'url_form': url_form,
                    'error': result['error']
                })
            else:
                return render(request, 'detection/result.html', {
                    'class_name': result['class_name'],
                    'confidence': result['confidence'],
                    'image_url': image_url,
                    'crop_name': result['crop_name'],
                    'health_status': result['health_status'],
                    'infection_percentage': result['infection_percentage'],
                    'severity_level': result['severity_level'],
                    'symptoms_detected': result['symptoms_detected'],
                    'recommendation': result['recommendation'],
                })
    else:
        url_form = ImageURLForm()

    return render(request, 'detection/enter_url.html', {
        'url_form': url_form,
    })

def predict_image(image_path_or_url):
    try:
        if image_path_or_url.startswith('http'):
            # Handle the image as a URL
            response = requests.get(image_path_or_url)
            image = Image.open(BytesIO(response.content)).convert("RGB")
        else:
            # Handle the image as a file path
            image = Image.open(image_path_or_url).convert("RGB")

        # Use Gemini Model
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_instruction,
            generation_config={"response_mime_type": "application/json"}
        )

        response = model.generate_content([image])
        result_json = json.loads(response.text)

        # Convert confidence to percentage for backward compatibility or UI formatting
        confidence = result_json.get('confidence_score', 0)
        if isinstance(confidence, (int, float)) and confidence <= 1.0:
            confidence = confidence * 100

        return {
            'class_name': result_json.get('disease_name', 'Unknown'),
            'confidence': round(confidence, 2),
            # Gemini full structured output
            'crop_name': result_json.get('crop_name', 'Unknown'),
            'health_status': result_json.get('health_status', 'Unknown'),
            'infection_percentage': result_json.get('infection_percentage', '0%'),
            'severity_level': result_json.get('severity_level', 'Unknown'),
            'symptoms_detected': result_json.get('symptoms_detected', 'None'),
            'recommendation': result_json.get('recommendation', 'None'),
        }
    
    except (requests.exceptions.RequestException, UnidentifiedImageError, IOError, json.JSONDecodeError, Exception) as e:
        print(f"Error during prediction: {e}")
        # Return an error message if there was an issue with the URL or image
        return {'error': 'Invalid image or an issue occurred during prediction. Please try again with a different image.'}
