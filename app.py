from flask import Flask, request
import requests
import json
from decouple import config
import random


app = Flask(__name__)

@app.route('/')
def hello():
    return 'hello world!'

api_url = 'https://api.telegram.org'                     #자주쓰는 경로
token = config('TOKEN')                                  #개별로 발급받은 토큰정보 decouple 모듈을 설치해서 숨긴다. .env 파일
chat_id = config('CHAT_ID')                              # 보낼사람 id (.gitignore에 .env추가)
naver_client_id = config('NAVER_CLIENT_ID')
naver_client_secret = config('NAVER_CLIENT_SECRET')

@app.route('/send/<text>')
def send(text):
    res = requests.get(f'{api_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}')
    return 'ok!'


@app.route('/chatbot', methods=['post'])
def chatbot():
    from_telegram = request.get_json()
    chat_id = from_telegram.get('message').get('from').get('id')
    text = from_telegram.get('message').get('text')
    
    
    # statue code 200 -> ok! 잘 접수했다.

    # 메뉴추천
    if text=='/메뉴':
        menus = ['새마을식당','초원삼겹살','멀캠20층','홍콩반점','순남시래기']
        lunch = random.choice(menus)
        response = lunch
    # 로또번호    
    elif text=='/lotto':
        lotto = random.sample(range(1,46),6)
        lotto = sorted(lotto)
        response = f'추천 로또 번호는 {lotto}입니다.'
    # 파파고 API 번역
    elif text[0:4]=='/번역 ':
        to_be_translated = text[4:]
        url = 'https://openapi.naver.com/v1/papago/n2mt'
        headers = {
           'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
           'X-Naver-Client-Id':naver_client_id,
           'X-Naver-Client-Secret':naver_client_secret
        }
        data = f'source=ko&target=en&text={to_be_translated}'.encode('utf-8')
        res = requests.post(url,headers=headers,data=data).json()
        response = res.get('message').get('result').get('translatedText')
    # 이외의 문구        
    else:
        response = f'너는 {text} 라고 보냈는데, 내가 할 줄 아는 건 메뉴야.'
    # res = requests.get(f'{api_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}}')
    res = requests.get(f'{api_url}/bot{token}/sendMessage?chat_id={chat_id}&text={response}')
    return 'ok', 200


app.run(debug=True)   #로컬 디버그용
 