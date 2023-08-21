from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route('/translationBot', methods=['POST'])
def translationBot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()

    #below is our url endpoint that we obtain from rapidapi's website
    url = "https://google-translate1.p.rapidapi.com/language/translate/v2"
    #below is our payload. We replace the query q with our incoming message
    payload = {
	"q": incoming_msg,
    #other target language codes can be found in the about page here
    #  https://rapidapi.com/petadata/api/rapid-translate/details use them
    #  to change target and source languages
	"target": "fr-fr",
	"source": "en"
    }
    #this header dictionary below is also specific to every user
    headers = {
	"content-type": "application/x-www-form-urlencoded",
	"Accept-Encoding": "application/gzip",
	"X-RapidAPI-Key": "You will be given your own API-KEY after sign up",
	"X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
    }

    #we finally make a post request to the translation API
    #with the endpoint url, payload, and headers as arguments
    response = requests.post(url, data=payload, headers=headers)

   #finally, we convert the response to an accessible json file and use the necessary keys
   # to access our translated text. Your translated text will probably be accessed
   # similarly    
    translatedstr = str(response.json()["data"]["translations"][0]["translatedText"])

    resp.message(translatedstr)
    
   
    return str(response)



if __name__ == '__main__':
    app.run(port=4000)








