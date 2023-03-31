import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests

def get_request(url, **kwargs):
    
    # If argument contain API KEY
    api_key = kwargs.get("api_key")
    print("GET from {} ".format(url))
    try:
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            # Call get method of requests library with URL and parameters
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
def post_request(url, json_payload, **kwargs):
    #print(kwargs)
    #print("GET from {} ".format(url))  
    try:
        response = requests.post(url, params=kwargs, headers={'Content-Type': 'application/json'}, 
                                 json=json_payload)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    json_data = json.loads(response.text)
    #print("With status {} ".format(status_code))
    return json_data


# Create a get_dealers_from_cf method to get dealers from a cloud function

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result and "doc" in json_result and "dealerships" in json_result["doc"]:
        # Get the list of dealerships from JSON
        dealerships = json_result["doc"]["dealerships"]
        # For each dealership object
        for dealership in dealerships:
            # Create a CarDealer object with values from the dealership dictionary
            dealer_obj = CarDealer(
                address=dealership["address"],
                city=dealership["city"],
                full_name=dealership["full_name"],
                id=dealership["id"],
                lat=dealership["lat"],
                long=dealership["long"],
                short_name=dealership["short_name"],
                st=dealership["st"],
                zip=dealership["zip"]
            )
            results.append(dealer_obj)
        return results



# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealerId):
    reviews_list = []
    results = get_request(url, dealerId=dealerId)
    if results:
        for review in results:
            review_object = DealerReview(
                dealership=review.get("dealership", ""),
                name=review.get("name", ""),
                purchase=review.get("purchase", ""),
                id=review.get("id", ""),
                review=review.get("review", ""),
                purchase_date=review.get("purchase_date", ""),
                car_make=review.get("car_make", ""),
                car_model=review.get("car_model", ""),
                car_year=review.get("car_year", ""),
                sentiment="",
            )
            review_object.sentiment = analyze_review_sentiments(review_object.review)
            reviews_list.append(review_object)
    return reviews_list



# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text): 

    url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/ed1820d4-8fc6-4852-afb2-c2bb7f5686c5" 

    api_key = "Sjdb1drxG_fDo4o94UUToRPoSKpLN1k0MLnzAy2xZO3o" 

    authenticator = IAMAuthenticator(api_key) 

    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator) 

    natural_language_understanding.set_service_url(url) 

    response = natural_language_understanding.analyze( text=text ,features=Features(sentiment=SentimentOptions(targets=[text])), language="en").get_result() 

    label=json.dumps(response, indent=2) 

    label = response['sentiment']['document']['label'] 

    return(label) 



