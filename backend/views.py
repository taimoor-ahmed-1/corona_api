from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import sox
from django.core import serializers as json_serializer
import json 
import time
from datetime import date, datetime
from django.http import HttpResponse
from .models import *
#from .serializers import *
from .utilities import Utilities
from rest_framework import generics
from rest_framework import status
#from .pagination import *
from django.contrib.auth import authenticate,login,logout
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FileUploadParser
from django.core.files.storage import FileSystemStorage
from rest_framework.permissions import AllowAny
from django.conf import settings
import requests
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

class Speech(APIView):
    parser_class = (FileUploadParser,)
    #authentication_classes = (TokenAuthentication,SessionAuthentication)
    #permission_classes = (IsAuthenticated,)
    
    def post(self, request, *args, **kwargs):
        play_files = {}
        play_files['خداحافظ'] = 'khudahafiz16.wav'

        play_files['شکریہ'] = 'shukria16.wav'

        play_files['آپ اس وقت کدھر ہیں؟'] = 'kidhr16.wav'

        play_files['وعلیکم اسلام'] = 'walaikum16.wav'

        play_files['معاف کیجیے۔ سمجھ نہیں آیا۔'] = 'maaf16.wav'

        play_files['کیا آپ کو کھانسی بھی ہے'] = 'khansi16.wav'

        play_files['آپ کو بخار محسوس ہو رہا ہے؟'] = 'bukhar16.wav'

        play_files['آپ نے بیرون ملک سفر کیا ہے انقریب؟'] = 'safar16.wav'

        play_files['ایمبولینس آرہی ہے'] = 'amb16.wav'

        play_files['آپ گھر میں ہی احتیاط کریں'] = 'ghar16.wav'

        play_files['ہادثہ کی نوعیت کیا ہے'] = 'noyat16.wav'

        play_files['کتنے افراد متاثر ہیں'] = 'kitne16.wav'

        play_files['براے مہربانی  معلومات مکمل کیجے'] = 'meherbani16.wav'

        play_files['آپ کو جسم میں درد ہے'] = 'dard16.wav'

        play_files['کیا ان الامات کو دن سے زیادہ کا ٹاءم ہوگیا ہے'] = 'A2din16.wav'

        play_files['کیا آپ کو  نزلہ زکام بھی ہے'] = 'nazla16.wav'

        play_files['ِکیا آپ کو سانس لینے میں دشواری ہوتی ہے'] = 'saans16.wav'

        play_files['آپ کا صوبہ کیا ہے'] = 'province16.wav'

        play_files["ِآپ ہمارےپنجاب کے فوکل پرسن سے بات کر لیں جس کا نمبر ہے 03027168021"] = 'punjab16.wav'

        play_files["ِآپ ہمارے گلگت بلتستان کے فوکل پرسن سے بات کر لیں جس کا نمبر ہے 03474847023"] = 'gilgit16.wav'

        play_files["ِآپ ہمارےسندھ کے فوکل پرسن سے بات کر لیں جس کا نمبر ہے 030271680222"] = 'sindh16.wav'

        play_files["ِآپ ہمارے بلوچستان کے فوکل پرسن سے بات کر لیں جس کا نمبر ہے 03457176723"] = 'balochistan16.wav'

        play_files["ِآپ ہمارےسرحد کے فوکل پرسن سے بات کر لیں جس کا نمبر ہے 03227168023"] = 'nwfp16.wav'

        play_files["اپ قریبی ہسپتال سے ٹیسٹ کرا لیں"] = 'hospital16.wav'
        sc = set(['.',',','/'])
        header = {"Content-Type":"audio/x-wav", "rate": "16000" }
        try:
            call_id  = request.data['call_id']
            audio = request.data['audio']
            #print(type(audio))
            #print(audio.read())
            #return Response("hello")
            response = requests.post('http://localhost:8888/client/dynamic/recognize',data=audio.read(),headers=header)
            gstreamer_obj=json.loads(response.text)
            #print(gstreamer_obj)
            text = gstreamer_obj['hypotheses'][0]['utterance']
            text = ''.join([c for c in text if c not in sc])
            print(text)
            if text == "" or text == "هے":
                return Response(['maaf16.wav'])
            resp = requests.post("http://localhost:5005/webhooks/rest/webhook",data=json.dumps({'sender':str(call_id),'message':text}))
            chat_obj =json.loads(resp.text)[0]
            chat_text = chat_obj['text']
            print(chat_text)
            return Response([play_files[chat_text]]) 
            #return Response(text)
        except Exception as e: 
            return Response(str(e))            

            
        


