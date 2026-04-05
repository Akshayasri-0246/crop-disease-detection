# crop-disease-detection
🌾 Crop Disease Detection using Deep Learning.

 📌 Overview
Crop Disease Detection is a web-based application designed to identify plant diseases using deep learning and computer vision techniques. Built with Django and powered by a TensorFlow Lite model, this system enables users to upload crop images or provide image URLs to receive accurate disease predictions along with confidence scores.

The project leverages transfer learning with a lightweight convolutional neural network (MobileNet), ensuring efficient performance and fast inference. It supports multiple crops such as Corn, Potato, Tomato, Rice, and Wheat, each with various disease and healthy classes.

🚀 Key Features
- Image-based crop disease detection  
- URL-based image prediction support  
- Fast inference using TensorFlow Lite  
- High accuracy with MobileNet transfer learning  
- Clean and responsive Django web interface  
- Scalable structure for adding new crops and diseases  

🧠 Model Details
- Framework: TensorFlow / Keras  
- Architecture: MobileNet (Transfer Learning)  
- Output: Multi-class classification  
- Deployment: TensorFlow Lite (.tflite)  

📂 Project Structure

Crop_Disease_Detection/

│── crop_disease/
│── detection/
│── images/
│── models/
│── train.py
│── manage.py
│── requirements.txt


⚙️ Setup Instructions

  1. Clone Repository

git clone https://github.com/Akshayasri-0246/crop-disease-detection.git

cd Crop_Disease_Detection


  2. Create Virtual Environment

py -3.11 -m venv venv
venv\Scripts\activate


 3. Install Dependencies

pip install -r requirements.txt


 4. Run Project

python manage.py runserver


 5. Open in Browser

http://127.0.0.1:8000/





📌 Summary
This project demonstrates how deep learning can be effectively applied in agriculture to detect crop diseases quickly and accurately, combining AI with a user-friendly web interface.
