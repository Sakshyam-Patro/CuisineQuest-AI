# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import logging
from datetime import datetime, timedelta
from typing import Any, Text, Dict, List
from pymongo import MongoClient
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import AllSlotsReset, Restarted
from fuzzywuzzy import process
from bson.son import SON


from rasa_sdk.types import DomainDict
from rasa_sdk import Action
from rasa_sdk.events import EventType
import parsedatetime as pdt
import re

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

file_handler = logging.FileHandler('rasa_actions.log')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
# Initialize MongoDB client
client = MongoClient("mongodb://localhost:27017/")
db = client["Restaurants"]
collection = db["Zomato"]
booking_collection = db["Bookings"]

# Initialize parsedatetime
cal = pdt.Calendar()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ValidateRestaurantForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_restaurant_form"

    def validate_user_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        # Basic validation for user name
        if len(slot_value.strip()) > 0:
            return {"user_name": slot_value}
        else:
            dispatcher.utter_message(text="Please enter a valid name.")
            return {"user_name": None}

    def validate_restaurant_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        try:
            restaurant = collection.find_one({"name": {"$regex": f"^{re.escape(slot_value)}$", "$options": "i"}})
            if restaurant:
                return {"restaurant_name": restaurant['name']}
            else:
                dispatcher.utter_message(text=f"Sorry, {slot_value} is not in our database. Please try another restaurant.")
                return {"restaurant_name": None}
        except Exception as e:
            dispatcher.utter_message(text="Sorry, I couldn't verify the restaurant name. Please try again.")
            return {"restaurant_name": None}

    def validate_date(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        try:
            # Try to parse the date
            current_year = datetime.now().year
            date = datetime.strptime(f"{slot_value} {current_year}", "%d %B %Y").date()
            # Check if the date is in the future
            today = datetime.now().date()
            if date < today:
                date = date.replace(year=current_year + 1)
            return {"date": date.strftime("%d %B %Y")}
        except ValueError:
            dispatcher.utter_message(text="That's not a valid date. Please enter a date in the format 'DD Month' (e.g., '3 March').")
            return {"date": None}

    def validate_time(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        try:
            # Try to parse the time
            time = datetime.strptime(slot_value, "%I %p").time()
            return {"time": time.strftime("%I:%M %p")}
        except ValueError:
            try:
                # Try another common format
                time = datetime.strptime(slot_value, "%I:%M %p").time()
                return {"time": time.strftime("%I:%M %p")}
            except ValueError:
                dispatcher.utter_message(text="That's not a valid time. Please enter a time in the format 'HH:MM AM/PM' or 'HH AM/PM' (e.g., '07:30 PM' or '7 PM').")
                return {"time": None}

    def validate_email(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if re.match(r"[^@]+@[^@]+\.[^@]+", slot_value):
            return {"email": slot_value}
        else:
            dispatcher.utter_message(text="Please enter a valid email address.")
            return {"email": None}

    def validate_phone_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if len(slot_value) == 10 and slot_value.isdigit():
            return {"phone_number": slot_value}
        else:
            dispatcher.utter_message(text="Please enter a valid 10-digit phone number.")
            return {"phone_number": None}
class ActionSubmitForm(Action):
    def name(self) -> Text:
        return "action_submit_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_name = tracker.get_slot("user_name")
        restaurant_name = tracker.get_slot("restaurant_name")
        date = tracker.get_slot("date")
        time = tracker.get_slot("time")
        email = tracker.get_slot("email")
        phone_number = tracker.get_slot("phone_number")

        dispatcher.utter_message(response="utter_confirm_booking",
                                 user_name=user_name,
                                 restaurant_name=restaurant_name,
                                 date=date,
                                 time=time,
                                 email=email,
                                 phone_number=phone_number)

        return [AllSlotsReset()]

# Provide Restaurant Info
class ActionTellRestaurantInfo(Action):
    def name(self) -> Text:
        return "action_tell_restaurant_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get the entire user message
        user_message = tracker.latest_message.get('text')
        
        # Remove common phrases to isolate the restaurant name
        prefixes_to_remove = ['tell me about', 'what do you know about', 'give me information on', 'can you provide details about']
        for prefix in prefixes_to_remove:
            if user_message.lower().startswith(prefix):
                restaurant_name = user_message[len(prefix):].strip()
                break
        else:
            restaurant_name = user_message

        logger.debug(f"Searching for restaurant: {restaurant_name}")
        
        # Get all restaurant names from the database
        all_restaurants = list(collection.find({}, {"name": 1}))
        restaurant_names = [r['name'] for r in all_restaurants]

        # Use fuzzy matching to find the closest match
        best_match, score = process.extractOne(restaurant_name, restaurant_names)

        logger.debug(f"Best match: {best_match}, score: {score}")

        if score > 80:  # You can adjust this threshold
            restaurant = collection.find_one({"name": best_match})
            
            if restaurant:
                info = f"Here's what I know about {restaurant['name']}:\n"
                info += f"Address: {restaurant['address']}\n"
                info += f"Cuisine: {restaurant['cuisines']}\n"
                info += f"Cost for two: ₹{restaurant['approx_cost(for two people)']}\n"
                info += f"Online ordering: {restaurant['online_order']}\n"
                info += f"Table booking: {restaurant['book_table']}\n"
                info += f"Type: {restaurant['rest_type']}\n"
                info += f"Location: {restaurant['location']}\n"
                
                if restaurant['phone']:
                    info += f"Phone: {restaurant['phone']}\n"
                
                dispatcher.utter_message(text=info)
            else:
                dispatcher.utter_message(text=f"I'm sorry, I couldn't find any information about {best_match}.")
        else:
            dispatcher.utter_message(text=f"I'm sorry, I couldn't find a restaurant matching '{restaurant_name}'. Could you please check the spelling and try again?")
        
        return []
    
# Tell the time
class ActionTellTime(Action):
    def name(self) -> Text:
        return "action_tell_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        current_time = datetime.now().strftime("%H:%M")
        message = f"The current time is {current_time}."
        
        dispatcher.utter_message(text=message)
        
        return []
class ActionResetBookingForm(Action):
    def name(self) -> Text:
        return "action_reset_booking_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [AllSlotsReset(), Restarted()]
        
# Recommend by Cuisine
class ActionRecommendByCuisine(Action):
    def name(self) -> Text:
        return "action_recommend_by_cuisine"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        cuisine = tracker.get_slot("cuisine")
        if not cuisine:
            dispatcher.utter_message(text="I'm sorry, I couldn't understand which cuisine you're looking for. Could you please specify the cuisine?")
            return []

        pipeline = [
            {"$match": {"cuisines": {"$regex": cuisine, "$options": "i"}}},
            {"$sort": SON([("rating", -1)])},
            {"$limit": 5}
        ]

        top_restaurants = list(collection.aggregate(pipeline))

        if not top_restaurants:
            dispatcher.utter_message(text=f"I'm sorry, I couldn't find any restaurants serving {cuisine} cuisine.")
            return []

        response = f"Here are the top 5 restaurants serving {cuisine} cuisine:\n\n"
        for restaurant in top_restaurants:
            response += f"- {restaurant['name']} (Rating: {restaurant['rating']})\n"
            response += f"  Address: {restaurant['address']}\n"
            response += f"  Cost for two: ₹{restaurant['approx_cost(for two people)']}\n\n"

        dispatcher.utter_message(text=response)
        return []

# Recommend by Location
class ActionRecommendByLocation(Action):
    def name(self) -> Text:
        return "action_recommend_by_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        location = tracker.get_slot("location")
        if not location:
            dispatcher.utter_message(text="I'm sorry, I couldn't understand which location you're looking for. Could you please specify the location?")
            return []

        pipeline = [
            {"$match": {"location": {"$regex": location, "$options": "i"}}},
            {"$sort": SON([("rating", -1)])},
            {"$limit": 5}
        ]

        top_restaurants = list(collection.aggregate(pipeline))

        if not top_restaurants:
            dispatcher.utter_message(text=f"I'm sorry, I couldn't find any restaurants in {location}.")
            return []

        response = f"Here are the top 5 restaurants in {location}:\n\n"
        for restaurant in top_restaurants:
            response += f"- {restaurant['name']} (Rating: {restaurant['rating']})\n"
            response += f"  Cuisine: {restaurant['cuisines']}\n"
            response += f"  Address: {restaurant['address']}\n"
            response += f"  Cost for two: ₹{restaurant['approx_cost(for two people)']}\n\n"

        dispatcher.utter_message(text=response)
        return []
    
# Random Restaurant
class ActionSurpriseRestaurant(Action):
    def name(self) -> Text:
        return "action_surprise_restaurant"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        random_restaurant = collection.aggregate([{ "$sample": { "size": 1 } }]).next()

        response = "Here's a random restaurant suggestion for you:\n\n"
        response += f"- {random_restaurant['name']} (Rating: {random_restaurant['rate']})\n"
        response += f"  Cuisine: {random_restaurant['cuisines']}\n"
        response += f"  Location: {random_restaurant['location']}\n"
        response += f"  Address: {random_restaurant['address']}\n"
        response += f"  Cost for two: ₹{random_restaurant['approx_cost(for two people)']}\n"

        dispatcher.utter_message(text=response)
        return []

# class ActionSubmitForm(Action):
#     def name(self) -> Text:
#         return "action_submit_form"

#     async def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: DomainDict,
#     ) -> List[EventType]:
#         user_name = tracker.get_slot("user_name")
#         restaurant_name = tracker.get_slot("restaurant_name")
#         date = tracker.get_slot("date")
#         time = tracker.get_slot("time")
#         email = tracker.get_slot("email")
#         phone_number = tracker.get_slot("phone_number")

#         # Check if all required slots are filled
#         if not all([user_name, restaurant_name, date, time, email, phone_number]):
#             logger.debug("Not all required slots are filled.")
#             dispatcher.utter_message(text="Please fill all the required details to book the restaurant.")
#             return []  # Return an empty list instead of trying to set a non-existent slot

#         booking_details = {
#             "user_name": user_name,
#             "restaurant_name": restaurant_name,
#             "date": date,
#             "time": time,
#             "email": email,
#             "phone_number": phone_number,
#         }

#         # Insert booking details into the bookings collection
#         booking_collection.insert_one(booking_details)

#         dispatcher.utter_message(response="utter_confirm_booking", 
#                                  user_name=user_name, 
#                                  restaurant_name=restaurant_name, 
#                                  date=date, 
#                                  time=time, 
#                                  email=email, 
#                                  phone_number=phone_number)
        
#         return []

#         return [SlotSet(slot_name, None) for slot_name in ["user_name", "restaurant_name", "date", "time", "email", "phone_number"]]


# # Cuisine Recommendation 
# class ActionRecommendByCuisine(Action):
#     def name(self) -> Text:
#         return "action_recommend_by_cuisine"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         cuisine = next(tracker.get_latest_entity_values("cuisine"), None)
        
#         if not cuisine:
#             last_message = tracker.latest_message.get('text')
#             if last_message and len(last_message.split()) <= 3:  # Assume it's a cuisine if it's a short phrase
#                 cuisine = last_message
#             else:
#                 dispatcher.utter_message(text="What cuisine would you like to look into?")
#                 return []

#         try:
#             logger.debug(f"Searching for cuisine: {cuisine}")
            
#             # Query MongoDB for top 5 restaurants of the specified cuisine
#             top_restaurants = list(collection.find(
#                 {"cuisines": {"$regex": cuisine, "$options": "i"}}
#             ).sort("rate", -1).limit(5))

#             logger.debug(f"Query result: {top_restaurants}")

#             if not top_restaurants:
#                 dispatcher.utter_message(text=f"I'm sorry, but I couldn't find any {cuisine} restaurants in our database.")
#                 return []

#             response = f"Here are the top 5 {cuisine} restaurants:\n\n"
#             for i, restaurant in enumerate(top_restaurants, 1):
#                 name = restaurant.get("name", "Unknown")
#                 rate = restaurant.get("rate", "N/A")
#                 response += f"{i}. {name} (Rating: {rate})\n"

#             dispatcher.utter_message(text=response)
#         except Exception as e:
#             logger.error(f"Error in action_recommend_by_cuisine: {str(e)}")
#             dispatcher.utter_message(text="I'm sorry, but I encountered an error while fetching restaurant recommendations. Please try again later.")

#         return []

# # Location Recommendation 
# class ActionRecommendByLocation(Action):
#     def name(self) -> Text:
#         return "action_recommend_by_location"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         location = tracker.get_slot("location")
#         cuisine = tracker.get_slot("cuisine")

#         if not location:
#             dispatcher.utter_message(text="I'm sorry, but I need to know which location you're interested in.")
#             return []

#         try:
#             logger.debug(f"Searching for location: {location}, cuisine: {cuisine}")

#             # Base query
#             query = {"location": {"$regex": location, "$options": "i"}}

#             # Add cuisine to query if provided
#             if cuisine:
#                 query["cuisines"] = {"$regex": cuisine, "$options": "i"}

#             # Query MongoDB for top 5 restaurants in the specified location (and cuisine, if provided)
#             top_restaurants = list(collection.find(query).sort("rate", -1).limit(5))

#             logger.debug(f"Query result: {top_restaurants}")

#             if not top_restaurants:
#                 message = f"I'm sorry, but I couldn't find any restaurants in {location}"
#                 if cuisine:
#                     message += f" serving {cuisine} cuisine"
#                 message += "."
#                 dispatcher.utter_message(text=message)
#                 return []

#             response = f"Here are the top 5 restaurants in {location}"
#             if cuisine:
#                 response += f" serving {cuisine} cuisine"
#             response += ":\n\n"

#             for i, restaurant in enumerate(top_restaurants, 1):
#                 name = restaurant.get("name", "Unknown")
#                 rate = restaurant.get("rate", "N/A")
#                 cuisines = restaurant.get("cuisines", "Various")
#                 response += f"{i}. {name} (Rating: {rate}, Cuisine: {cuisines})\n"

#             dispatcher.utter_message(text=response)
#         except Exception as e:
#             logger.error(f"Error in action_recommend_by_location: {str(e)}")
#             dispatcher.utter_message(text="I'm sorry, but I encountered an error while fetching restaurant recommendations. Please try again later.")

#         return []
    

# class ActionRecommendByCuisineAndLocation(Action):
#     def name(self) -> Text:
#         return "action_recommend_by_cuisine_and_location"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         cuisine = tracker.get_slot("cuisine")
#         location = tracker.get_slot("location")

#         if not cuisine or not location:
#             dispatcher.utter_message(text="I need both a cuisine and a location to give you recommendations.")
#             return []

#         try:
#             query = {
#                 "cuisines": {"$regex": cuisine, "$options": "i"},
#                 "location": {"$regex": location, "$options": "i"}
#             }
#             top_restaurants = list(collection.find(query).sort("rate", -1).limit(5))

#             if not top_restaurants:
#                 dispatcher.utter_message(text=f"I'm sorry, but I couldn't find any {cuisine} restaurants in {location}.")
#                 return []

#             response = f"Here are the top 5 {cuisine} restaurants in {location}:\n\n"
#             for i, restaurant in enumerate(top_restaurants, 1):
#                 name = restaurant.get("name", "Unknown")
#                 rate = restaurant.get("rate", "N/A")
#                 response += f"{i}. {name} (Rating: {rate})\n"

#             dispatcher.utter_message(text=response)
#         except Exception as e:
#             logger.error(f"Error in action_recommend_by_cuisine_and_location: {str(e)}")
#             dispatcher.utter_message(text="I'm sorry, but I encountered an error while fetching restaurant recommendations. Please try again later.")

#         return []