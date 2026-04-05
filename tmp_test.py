import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crop_disease.settings')
django.setup()

try:
    import detection.views
except Exception as e:
    print(f"Failed to import views: {e}")
