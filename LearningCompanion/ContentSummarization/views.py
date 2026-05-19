from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
import json
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import google.generativeai as genai

# Create your views here.

class GetDetails(View):
    #def get(self, request):
        #return HttpResponse(f"Welcome to the Content Summarization Section And today is {day}")
    #    data = json.loads(request.body)
    #    return JsonResponse(data)
    def get(self, request):
        ytt_api = YouTubeTranscriptApi()
        
        data = json.loads(request.body)
        url = data['url']
        lan = data['language']
        video_id = self.extract_video_id(url)
        
        print(video_id)
        language_map = {
            "Tamil": "ta",
            "English": "en",
            "Hindi": "hi",
            "French": "fr"
        }
        language = language_map[lan]
        '''if video_id != None:
            transcript = ytt_api.fetch(video_id, languages=[language])
            full_text = " ".join([item.text for item in transcript])
            #with open('youtube_' + video_id, 'w', encoding="utf-8") as file:
            with open (rf"C:Projects\DB\Subtitle\{video_id}.txt", "w", encoding="utf-8" ) as file:   
                file.write(full_text)
            file.close()
            summary = self.ai_summarise(video_id, language)'''
        if video_id != None:
            # Get available transcripts
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

            # Fetch first available transcript
            transcript = next(iter(transcript_list))

            fetched_transcript = transcript.fetch()

            # Convert transcript list into text
            transcript_text = " ".join(
                [item.text for item in fetched_transcript]
            )

            # Save transcript
            with open(
                rf"C:Projects\DB\Subtitle\{video_id}.txt",
                "w",
                encoding="utf-8"
            ) as file:

                file.write(transcript_text)

            return JsonResponse({"message" : "Video Transcripted and Summarised. File Successfully Downloaded"})
        return JsonResponse({"message" : "Enter a Valid Url"})

        

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

    def ai_summarise(self, video_id, language):
        genai.configure(api_key="YOUR_API_KEY")

        # Read transcript file
        with open(rf"C:Projects\DB\Subtitle\{video_id}.txt", "r", encoding="utf-8") as file:
            transcript = file.read()
        #for model in genai.list_models():
        #    print(model.name)
        # Load model
        model = genai.GenerativeModel("gemini-2.5-flash")

        
        # Generate summary
        response = model.generate_content(
            f"Summarize this transcript simply in points as per the mentioned language{language}:\n\n{transcript}"
        )
        summary = response.text
        # Print summary
        with open(rf"C:Projects\DB\Summary\{video_id}.txt", "w", encoding="utf-8") as file:
            file.write(summary)

        #print(response.text)


                
        
        