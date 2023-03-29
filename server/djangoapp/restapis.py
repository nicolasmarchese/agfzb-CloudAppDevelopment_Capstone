import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(
            url,
            headers={'Content-Type': 'application/json'},
            params=kwargs
        )
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

def get_dealer_by_state(url, state):
    dealership = get_request(url, state=state)
    return dealership

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



