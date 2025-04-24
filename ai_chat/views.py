import os
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from dotenv import load_dotenv
import cohere

# Load .env
load_dotenv()

# Cohere setup
co = cohere.Client(os.getenv("COHERE_API_KEY"))

def get_cohere_response(query):
    try:
        response = co.generate(
            prompt=query,
            model="command",
            max_tokens=100,
            temperature=0.7
        )
        return response.generations[0].text.strip()
    except Exception as e:
        print(f"Error in Cohere API: {e}")
        return f"⚠️ Error: {str(e)}"

def chat_view(request):
    response = ""
    detected_labels = ""
    uploaded_image_url = ""
    query = ""

    if request.method == "POST":
        query = request.POST.get("query", "").strip()

        # Case 1: Text (manual or speech-to-text) is given
        if query:
            response = get_cohere_response(query)

        # Case 2: Image is uploaded (but without YOLO processing)
        elif request.FILES.get("image"):
            image = request.FILES["image"]
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            uploaded_image_url = fs.url(filename)
            print(f"Image uploaded: {uploaded_image_url}")  # Debugging image URL
            
            # You can remove YOLO-related code and the detection logic here.

            # No detection is happening now, you can add some default response or further processing if needed.
            response = "Image uploaded successfully, but no object detection is applied."

    return render(request, "ai_chat/chat.html", {
        "query": query,
        "detected_labels": detected_labels,
        "response": response,
        "image_response": response,  # Just passing the default image response
        "image_url": uploaded_image_url
    })
