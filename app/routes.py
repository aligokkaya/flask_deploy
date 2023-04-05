from flask import redirect,url_for,request,render_template
from app import app
from langdetect import detect
import requests
from bs4 import BeautifulSoup
import requests
from PIL import Image
import numpy as np
from io import BytesIO

# text = "एमओओसी पर 20 सर्वाधिक"
# lang = detect(text)

# print(lang) 



@app.route('/', methods=['GET', 'POST'])
def login():
    jso={'link':[],
            'language':[],
             'image':[]
            }
    if request.method == 'POST':
        url=request.form['username']
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        jso={'link':[],
            'language':[],
             'image':[]
            }

        for link in soup.find_all('a'):
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            lang = detect(text)
            jso['link'].append(link.get('href'))
            jso['language'].append(lang)
            # jso['image'].append(lang)
            if len(jso['language']) > 10:
                break

        
        for image in soup.find_all('img'):
            img_url=image.get('src')
            try:
                img_url = img['src']
                response = requests.get(img_url)
                img = Image.open(BytesIO(response.content))
                img_pixels = np.array(img.convert('L'))
                std_dev = np.std(img_pixels)
                if std_dev < 10:
                    print(img_url + ' is blurred.')
                    jso['image'].append(img_url + ' is blurred.')
                else:
                    print(img_url + ' is not blurred.')
                    jso['image'].append(img_url + ' is not blurred.')
            except:
                jso['image'].append(img_url + ' is not blurred.')
            
            if len(jso['image'])>10:
                break
        # print(images)
    # print(jso)
        # print(links)
    
    return render_template('index.html',jso=jso)
