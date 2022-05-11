import requests
import json
# import related models here
from .models import *
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        # no authentication GET
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)

    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["data"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                    zip=dealer["zip"], state=dealer["state"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf (url, dealer_id):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealership=dealer_id)

    if json_result:
        # Get the row list in JSON as dealers
        rvs = json_result["data"]
        # For each dealer object

        if not rvs: 
            return results
        for rv in rvs:
            print(rv)
            # Get its content in `doc` object
            # Create a CarDealer object with values in `doc` object
            #name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id
            obj = DealerReview(dealership=rv["dealership"], name=rv["name"], purchase=rv["purchase"],
                                    review=rv["review"], purchase_date=rv["purchase_date"],
                                   car_make=rv["car_make"], car_model=rv["car_model"], car_year=rv["car_year"])
            obj.sentiment = analyze_review_sentiments(obj.review)
            
            results.append(obj)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative


# {
#   "apikey": "5NYIZbaXjwxv4JLs80RLPQ8uiri0dgkmHa8SYIE7CDSY",
#   "iam_apikey_description": "Auto-generated for key crn:v1:bluemix:public:natural-language-understanding:au-syd:a/eab9a66088c2473699205c17d5a23b25:4a17a882-fb41-4338-a601-ae6ddd3973cc:resource-key:0d7a15ea-73de-4c6c-ad93-8d41f5bd253d",
#   "iam_apikey_name": "Service credentials-1",
#   "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Manager",
#   "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/eab9a66088c2473699205c17d5a23b25::serviceid:ServiceId-c0093894-2ac2-417a-8914-ca745b73f485",
#   "url": "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/4a17a882-fb41-4338-a601-ae6ddd3973cc"
# }
def analyze_review_sentiments(text):
    api_key = "5NYIZbaXjwxv4JLs80RLPQ8uiri0dgkmHa8SYIE7CDSY"
    url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/4a17a882-fb41-4338-a601-ae6ddd3973cc"
    texttoanalyze= text
    version = '2020-08-01'
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2020-08-01',
    authenticator=authenticator
    )
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze(
        text=text,
        features= Features(sentiment= SentimentOptions()),
        language="en"
    ).get_result()
    print(json.dumps(response))
    sentiment_score = str(response["sentiment"]["document"]["score"])
    sentiment_label = response["sentiment"]["document"]["label"]
    print(sentiment_score)
    print(sentiment_label)
    sentimentresult = sentiment_label
    
    return sentimentresult


def post_request(url, payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    print(payload)
    response = requests.post(url, params=kwargs, json=payload)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data