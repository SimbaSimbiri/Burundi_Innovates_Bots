from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
#pip install googlesearch-python in your terminal before the next step
from googlesearch import search 

app = Flask(__name__)

@app.route('/googleSearchBot', methods = ['POST'])
def googleBot():

    incoming_msg = request.values.get("Body","")
    resp = MessagingResponse()

    query =  incoming_msg

    #using the search functionality to input a search query in google and bring
    #the links of the first declared number of results as a list
    results = search(query, num_results = 5)

    # displaying result
    msg = resp.message(f"--- Results for '{incoming_msg}' ---")
    for result in results:
        msg = resp.message(result)
   
    return str(resp)


if __name__ == '__main__':
    app.run(port=4000)


