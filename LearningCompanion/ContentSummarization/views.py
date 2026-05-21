from django.views import View
from django.http import JsonResponse
from django.shortcuts import render
import json
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import google.generativeai as genai
import os

# Create your views here.

class GetDetails(View):
    #def get(self, request):
        #return HttpResponse(f"Welcome to the Content Summarization Section And today is {day}")
    #    data = json.loads(request.body)
    #    return JsonResponse(data)
    def get(self, request):
        return render(request, "ContentSummarization/index.html")

    def post(self, request):
        ytt_api = YouTubeTranscriptApi()
        
        data = json.loads(request.body)
        url = data['url']
        language = data['language']
        video_id = self.extract_video_id(url)
        

        #language = language_map[lan]
        '''
        if video_id != None:
            transcript = ytt_api.fetch(video_id, languages=[language])
            full_text = " ".join([item.text for item in transcript])
            #with open('youtube_' + video_id, 'w', encoding="utf-8") as file:
            
            file.close()
            summary = self.ai_summarise(video_id, language)'''
        if video_id != None:
            ytt_api = YouTubeTranscriptApi()

            # Get available transcripts
            transcript_list = ytt_api.list(video_id)

            try:

                transcript_list = ytt_api.list(video_id)

                try:
                    # Try English subtitles first
                    transcript = transcript_list.find_transcript(['en'])

                except:
                    # Otherwise use first available subtitle
                    transcript = next(iter(transcript_list), None)
                    print("trans ", transcript)

                # If no subtitles exist
                if transcript is None:
                    print(None)

                else:

                    # Fetch subtitles
                    fetched_transcript = transcript.fetch()

                    # Convert to text
                    transcript_text = " ".join(
                        [item.text for item in fetched_transcript]
                    )
                    # Create folder if it doesn't exist
                    folder_path = rf"C:\Users\sange\Projects\DB\Subtitle\{language}"
                    os.makedirs(folder_path, exist_ok=True)

                    file_path = rf"{folder_path}\{video_id}.txt"
                    with open(
                            file_path,
                            "w",
                            encoding="utf-8"
                        ) as file:

                            file.write(transcript_text)
                    print(transcript_text)
                summary = self.ai_summarise(video_id, language)
                return JsonResponse({
                    "message": "Video transcripted and summarised successfully.",
                    "summary": summary,
                })
            except Exception as e:
                return JsonResponse({"message": str(e)}, status=400)
            
        return JsonResponse({"message": "Enter a valid YouTube URL."}, status=400)

        

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
        #genai.configure(api_key=os.environ.get("AIzaSyA9PAbfL4ofIgfF1mlxEUtbaMJXjky4XNM"))
        genai.configure(api_key="AIzaSyA9PAbfL4ofIgfF1mlxEUtbaMJXjky4XNM")
        
        # Read transcript file
        with open(rf"C:\Users\sange\Projects\DB\Subtitle\{language}\{video_id}.txt", "r", encoding="utf-8") as file:
            transcript = file.read()

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



                
        
        
