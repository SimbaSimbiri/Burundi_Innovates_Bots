from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import requests

#this is the endpoint url obtained from openai chat APIs
URL = "https://api.openai.com/v1/chat/completions"

openai.api_key = "YOUR API KEY"

#below is one of the arguments of the payload we will input to a post request
#it tells the AI how to act. You can change this to "You are a helpful programmer"
#or "You are a helpful business analytic"
messages = [{"role": "system", "content": "You are conversant with the history of Burundi and your responses are strictly under 150 words"}]

app = Flask(__name__)

@app.route('/gptBot', methods=['POST'])
def gptBot():

    incoming_msg = request.values.get("Body","")
    resp = MessagingResponse()
    #below we append the message argument with what our user will input from 
    #whatsapp. Note the role value changed
    messages.append({"role": "user", "content": incoming_msg})
    
    # the below payload specifies what model of chatgpt we are using and the messages
    #input. The other arguments can be left as default
    payload = {"model" : "gpt-3.5-turbo", "messages" : messages, "stream":False,
               "temperature" : 1.0,"top_p":1.0 }
    #below we use our "Authorization" key to input our speicific API-KEY so that 
    #every post request is granted permision to access openai's API
    headers = {"Content-Type" : "application/json", "Authorization": f"Bearer {openai.api_key}"}

    responseGpt = requests.post(URL, headers= headers, json= payload, stream= False)
    
    #we then change our response to a json type format so that our response is
    #easily accessible by a sequence of keys
    data = responseGpt.json()

    #since we can only send three requests to the API per minute
    # highly advisable to send only one per minute) we first check if we can 
    # still use our API. If we have overused it, we will receive
    #an error about using all of our quota
    if "error" in data:
        response_text = data["error"]["message"]
        resp.message(response_text)
    #if we still have sufficient quota, we access our response from chatgpt 
    else:
        response_text = data["choices"][0]["message"]["content"]       
        resp.message(response_text)
    
    return str(resp)

if __name__ == '__main__':
    app.run(port=4000)





