from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import os
import requests
import json
import re
#import pan import media
from pan.settings import BASE_DIR
# Create your views here.
def upload(request):
    if request.method == 'POST':
        uploaded_file= request.FILES['document']
        name= uploaded_file.name
        fs= FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        print(uploaded_file.name)
    return render(request, 'homepage.html')

def result(request):
    if request.method == 'POST':
        uploaded_file= request.FILES['document']
        name= uploaded_file.name
        
    def ocr_space_file(filename, overlay=False, api_key='f31d91e72588957', language='eng'):
      

        payload = {'isOverlayRequired': overlay,
                'apikey': api_key,
                'language': language,
                }
        with open(filename, 'rb') as f:
            r = requests.post('https://api.ocr.space/parse/image',
                            files={filename: f},
                            data=payload,
                            )
        return r.content.decode()

    #file= os.path.join(BASE_DIR, 'media/imgg.pdf')
    
    #test_file = ocr_space_file(filename= os.path.join(BASE_DIR, file), language='pol')
    apath="media"
    dir_list= os.listdir(apath)
    file_name= dir_list[0]
    final0= os.path.join(apath, file_name)
    print(final0)
    final=os.path.join(BASE_DIR, final0)
   
    test_file = ocr_space_file(filename= os.path.join(BASE_DIR, final), language='pol')
   
    data= json.loads(test_file)
    s=data['ParsedResults'][0] ['ParsedText']
    print(s)
    first_word = s.split()

    #print(first_word[1])
   
    c=0
    name= ""
    for i in first_word:
        if(c>2 and first_word[c][0].isnumeric()== False):
            name= name+" "+ first_word[c]
            
            c=c+1
        elif(first_word[c][0].isnumeric()== True):
            break
        else:
            c=c+1

    #Adding all the values to the dictionary which will later to be displayed on the front end
    name=name  
    date= first_word[c][0:2]
    month=first_word[c][3:5]
    year=first_word[c][6:10]
    num=first_word[c+4]
    
    os.remove(final)
    context={'name' : name, 'day': date, 'month': month, 'year': year, 'number': num}
    return render(request, 'homepag.html', context )
            