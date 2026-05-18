from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
import json
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

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
        video_id = self.extract_video_id(url)
        print(video_id)
        if video_id != None:
            transcript = ytt_api.fetch(video_id, languages=['ta'])
            full_text = " ".join([item.text for item in transcript])
            with open('youtube_' + video_id, 'w', encoding="utf-8") as file:
                file.write(full_text)
            file.close()
            return JsonResponse({"message" : "Video Transcripted and File Successfully Downloaded"})
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

                
        
        