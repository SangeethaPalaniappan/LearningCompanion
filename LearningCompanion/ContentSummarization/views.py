from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import FormView
from django.http import JsonResponse
from django.shortcuts import render
import json
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import google.generativeai as genai
from .forms import SignUpForm
from .models import Users, VideoSubtitle
import os

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    load_dotenv = None

# Create your views here.

class SignUpView(FormView):
    template_name = "registration/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("get")

    def form_valid(self, form):
        user = form.save()
        Users.objects.create(
            user_name=user.username,
            mail_id=form.cleaned_data["email"],
            password=user.password,
        )
        login(self.request, user)
        messages.success(self.request, "Account created successfully.")
        return super().form_valid(form)


class GetDetails(LoginRequiredMixin, View):
    #def get(self, request):
        #return HttpResponse(f"Welcome to the Content Summarization Section And today is {day}")
    #    data = json.loads(request.body)
    #    return JsonResponse(data)
    def get(self, request):
        return render(request, "ContentSummarization/index.html")

    def post(self, request):
        data = json.loads(request.body)
        url = data['url']
        language = data['language']
        video_id = self.extract_video_id(url)

        if video_id is None:
            return JsonResponse({"message": "Enter a valid YouTube URL."}, status=400)

        try:
            subtitle_record = VideoSubtitle.objects.filter(video_id=video_id).first()

            if subtitle_record:
                transcript_text = subtitle_record.subtitle
                message = "Subtitle found in database and summarised successfully."
            else:
                transcript_text = self.fetch_transcript(video_id)
                VideoSubtitle.objects.create(video_id=video_id, subtitle=transcript_text)
                message = "Subtitle fetched, saved to database, and summarised successfully."

            summary = self.ai_summarise(video_id, language, transcript_text)
            return JsonResponse({
                "message": message,
                "summary": summary,
            })
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)

    def fetch_transcript(self, video_id):
        ytt_api = YouTubeTranscriptApi()
        transcript_list = ytt_api.list(video_id)

        try:
            transcript = transcript_list.find_transcript(['en'])
        except Exception:
            transcript = next(iter(transcript_list), None)

        if transcript is None:
            raise ValueError("No subtitles are available for this video.")

        fetched_transcript = transcript.fetch()
        return " ".join([item.text for item in fetched_transcript])

    def extract_video_id(self, url):

        parsed_url = urlparse(url)

        # youtu.be links
        if "youtu.be" in url:
            return parsed_url.path.lstrip("/")

        # shorts links
        elif "/shorts/" in url:
            return parsed_url.path.split("/shorts/")[1].split("/")[0]

        # normal watch links
        elif "watch" in url:
            return parse_qs(parsed_url.query).get("v", [None])[0]
            
        # embed links    
        elif "/embed/" in url:
            return parsed_url.path.split("/embed/")[1]

        return None

    def ai_summarise(self, video_id, language, transcript):
         
        if load_dotenv:
            load_dotenv("api_key.env")
        api_key = os.getenv("API_KEY") 
        
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set.")

        genai.configure(api_key=api_key)

        # Load model
        model = genai.GenerativeModel("gemini-2.5-flash")

        
        # Generate summary
        response = model.generate_content(
            f"Summarize this transcript simply in points as per the mentioned language{language}:\n\n{transcript}"
        )
        summary = response.text
        #summary = transcript
        # Print summary
        # Create folder if it doesn't exist
        folder_path = rf"C:\Users\sange\Projects\DB\Summary\{language}"
        os.makedirs(folder_path, exist_ok=True)

        file_path = rf"{folder_path}\{video_id}.txt"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(summary)

        return summary



                
        
        
