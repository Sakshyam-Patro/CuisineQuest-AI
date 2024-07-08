# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
# import pymongo 
# import re
# from pymongo import MongoClient
# from typing import Any, Text, Dict, List
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.forms import FormValidationAction
# from datetime import datetime, timedelta
# import parsedatetime as pdt  # Ensure parsedatetime is installed

# # import logging

# # logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', handlers=[
# #     logging.FileHandler("app.log"),
# #     logging.StreamHandler()
# # # ])

# # logger = logging.getLogger(__name__)

# # cal = parsedatetime.Calendar()
# cal = pdt.Calendar()

# # MongoDB connection
# client = MongoClient("mongodb://localhost:27017/")
# db = client["Restaurants"]
# collection = db["Zomato"]
# booking_collection = db["Bookings"]

# class RestaurantForm(FormValidationAction):
#     def name(self) -> Text:
#         return "restaurant_form"

#     def validate_user_name(
#         self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
#     ) -> Dict[Text, Any]:
#         if value and len(value.strip()) > 0:
#             return {"user_name": value}
#         else:
#             dispatcher.utter_message(text="Please provide a valid name.")
#             return {"user_name": None}

#     def validate_restaurant_name(
#         self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
#     ) -> Dict[Text, Any]:
#         if value and len(value.strip()) > 0:
#             # Check if restaurant exists in database
#             restaurant = collection.find_one({"name": value})
#             if restaurant:
#                 return {"restaurant_name": value}
#             else:
#                 dispatcher.utter_message(text=f"I'm sorry, I couldn't find a restaurant named '{value}'. Please check the spelling or try another restaurant.")
#                 return {"restaurant_name": None}
#         else:
#             dispatcher.utter_message(text="Please provide a valid restaurant name.")
#             return {"restaurant_name": None}
            

#     def validate_phone_number(
#         self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
#     ) -> Dict[Text, Any]:
#         if not value:
#             dispatcher.utter_message(text="What is your phone number?")
#             return {"phone_number": None}
#         phone_pattern = r"^\d{10}$"
#         if not re.match(phone_pattern, value):
#             dispatcher.utter_message(text="Please provide a valid 10-digit phone number.")
#             return {"phone_number": None}
#         return {"phone_number": value}

#     def validate_email(
#         self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
#     ) -> Dict[Text, Any]:
#         if not value:
#             dispatcher.utter_message(text="What is your email?")
#             return {"email": None}
#         email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
#         if not re.match(email_pattern, value):
#             dispatcher.utter_message(text="This email is invalid. Please provide a valid email address.")
#             return {"email": None}
#         return {"email": value}

#     def validate_date(
#         self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
#     ) -> Dict[Text, Any]:
#         if not value:
#             dispatcher.utter_message(text="What date would you like to book? (e.g., 29 June, tomorrow, next Friday)")
#             return {"date": None}
#         try:
#             parsed_date = datetime.strptime(value, "%Y-%m-%d")
#             booking_date = parsed_date.date()
#             today = datetime.now().date()
#             if booking_date < today:
#                 dispatcher.utter_message(text="Sorry, you can't book for a date in the past. Please provide a future date.")
#                 return {"date": None}
#             if booking_date > today + timedelta(days=30):
#                 dispatcher.utter_message(text="Sorry, you can only book up to 30 days in advance. Please choose a closer date.")
#                 return {"date": None}
#             formatted_date = booking_date.strftime("%Y-%m-%d")
#             return {"date": formatted_date}
#         except ValueError:
#             dispatcher.utter_message(text="I couldn't understand that date. Please try again with a clearer date format.")
#             return {"date": None}

#     def validate_time(
#         self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
#     ) -> Dict[Text, Any]:
#         if not value:
#             dispatcher.utter_message(text="What time would you like to book? (e.g., 7pm, 10:30 pm, 14:00)")
#             return {"time": None}
#         try:
#             parsed_time = datetime.strptime(value, "%H:%M")
#             booking_time = parsed_time.time()
#             opening_time = datetime.strptime("11:00", "%H:%M").time()
#             closing_time = datetime.strptime("22:00", "%H:%M").time()
#             if booking_time < opening_time or booking_time > closing_time:
#                 dispatcher.utter_message(text="Sorry, bookings are only available between 11:00 AM and 10:00 PM. Please choose a time within this range.")
#                 return {"time": None}
#             formatted_time = booking_time.strftime("%H:%M")
#             return {"time": formatted_time}
#         except ValueError:
#             dispatcher.utter_message(text="I couldn't understand that time. Please try again with a clearer time format.")
#             return {"time": None}

# class ActionSubmitForm(Action):
#     def name(self) -> Text:
#         return "action_submit_form"

#     def run(
#         self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
#     ) -> List[Dict[Text, Any]]:
#         user_name = tracker.get_slot("user_name")
#         restaurant_name = tracker.get_slot("restaurant_name")
#         phone_number = tracker.get_slot("phone_number")
#         email = tracker.get_slot("email")
#         date = tracker.get_slot("date")
#         time = tracker.get_slot("time")
        
#         # Here you could add logic to actually create the booking in your database
#         booking = {
#             "user_name": user_name,
#             "restaurant_name": restaurant_name,
#             "phone_number": phone_number,
#             "email": email,
#             "date": date,
#             "time": time
#         }
#         booking_collection.insert_one(booking)
        
#         dispatcher.utter_message(
#             text=f"Thank you {user_name}, your booking at {restaurant_name} on {date} at {time} has been confirmed."
#         )
#         return []


















# Restaurant form
# class RestaurantForm(FormValidationAction):
#     def name(self) -> Text:
#         return "restaurant_form"

#     @staticmethod
#     def required_slots(tracker: Tracker) -> List[Text]:
#         return ["user_name", "restaurant_name", "phone_number", "email", "date", "time"]

#     def validate_user_name(
#         self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
#     ) -> Dict[Text, Any]:
#         if not value:
#             dispatcher.utter_message(text="Please provide your name.")
#             return {"user_name": None}
#         return {"user_name": value}

#     def validate_restaurant_name(
#         self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
#     ) -> Dict[Text, Any]:
#         if not value:
#             dispatcher.utter_message(text="Which restaurant are you interested in booking?")
#             return {"restaurant_name": None}

#         restaurant = collection.find_one({"name": {"$regex": f"^{re.escape(value)}$", "$options": "i"}})
#         if not restaurant:
#             dispatcher.utter_message(text=f"I'm sorry, I couldn't find a restaurant named '{value}'. Could you please check the spelling or provide another restaurant name?")
#             return {"restaurant_name": None}
        
#         return {"restaurant_name": restaurant["name"]}

#     def validate_phone_number(
#         self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
#     ) -> Dict[Text, Any]:
#         if not value:
#             dispatcher.utter_message(Text="What is your phone number?")
#             return {"phone_number": None}

#         phone_pattern = r"^\d{10}$"  # Define a regular expression pattern for a 10-digit phone number
#         if not re.match(phone_pattern, value):
#             dispatcher.utter_message(template="utter_invalid_phone_number")
#             return {"phone_number": None}
        
#         return {"phone_number": value}

#     def validate_email(
#         self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
#     ) -> Dict[Text, Any]:
#         if not value:
#             dispatcher.utter_message(text="What is your email?")
#             return {"email": None}

#         email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"  # Define an email validation pattern
#         if not re.match(email_pattern, value):
#             dispatcher.utter_message(text="This email is invalid.")
#             return {"email": None}

#         return {"email": value}

#     def validate_date(
#         self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
#     ) -> Dict[Text, Any]:
#         if not value:
#             dispatcher.utter_message(template="what date would you like to book?")
#             return {"date": None}
        
#         return {"date": value}

#     def validate_time(
#         self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
#     ) -> Dict[Text, Any]:
#         if not value:
#             dispatcher.utter_message(template="What time would you like to book?")
#             return {"time": None}

#         return {"time": value}
        
    # async def submit(
    #     self,
    #     dispatcher: CollectingDispatcher,
    #     tracker: Tracker,
    #     domain: Dict[Text, Any],
    # ) -> List[Dict[Text, Any]]:
    #     # Retrieve the filled slot values
    #     user_name = tracker.get_slot("user_name")
    #     restaurant_name = tracker.get_slot("restaurant_name")
    #     phone_number = tracker.get_slot("phone_number")
    #     email = tracker.get_slot("email")
    #     date = tracker.get_slot("date")
    #     time = tracker.get_slot("time")

    #     # Perform any additional actions with the collected slot values here
    #     # For example, you can save them to a database or perform an API call

    #     # Confirm booking to the user
    #     dispatcher.utter_message(
    #         template="utter_confirm_booking",
    #         user_name=user_name,
    #         restaurant_name=restaurant_name,
    #         phone_number=phone_number,
    #         email=email,
    #         date=date,
    #         time=time,
    #     )

    #     return []

# class ActionSubmitForm(Action):
#     def name(self) -> Text:
#         return "action_submit_form"

#     def run(
#         self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
#     ) -> List[Dict[Text, Any]]:
#         user_name = tracker.get_slot("user_name")
#         restaurant_name = tracker.get_slot("restaurant_name")
#         phone_number = tracker.get_slot("phone_number")
#         email = tracker.get_slot("email")
#         date = tracker.get_slot("date")
#         time = tracker.get_slot("time")

#         # Here you might want to add logic to save the booking to your database

#         dispatcher.utter_message(
#             template="utter_confirm_booking",
#             user_name=user_name,
#             restaurant_name=restaurant_name,
#             phone_number=phone_number,
#             email=email,
#             date=date,
#             time=time,
#         )

#         return []


# class RestaurantForm(FormValidationAction):
#     def name(self) -> Text:
#         return "restaurant_form"

    # @staticmethod
    # def required_slots(self) -> List[Text]:
    #     return ["user_name", "restaurant_name", "phone_number", "email", "date", "time"]
# Async version corrected with the required parameters
    # async def required_slots(
    #         self, 
    #         _slots_mapped_in_domain: List[Text], 
    #         _dispatcher: "CollectingDispatcher", 
    #         _tracker: "Tracker", 
    #         _domain: Dict,  # Assuming usage of a generic dict type hint as previously discussed
    #     ) -> List[Text]:
    #         return ["user_name", "restaurant_name", "phone_number", "email", "date", "time"]
#     async def required_slots(
#                 self,
#                 slots_mapped_in_domain: List[Text],
#                 dispatcher: CollectingDispatcher,
#                 tracker: Tracker,
#                 domain: Dict
#         ) -> List[Text]:
#             return ["user_name", "restaurant_name", "phone_number", "email", "date", "time"]


#     def validate_user_name(
#         self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
#     ) -> Dict[Text, Any]:
#         if not value:
#             dispatcher.utter_message(text="Please provide your name.")
#             return {"user_name": None}
#         return {"user_name": value}

#     def validate_restaurant_name(
#         self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
#     ) -> Dict[Text, Any]:
#         if not value:
#             dispatcher.utter_message(text="Which restaurant are you interested in booking?")
#             return {"restaurant_name": None}

#         restaurant = collection.find_one({"name": {"$regex": f"^{re.escape(value)}$", "$options": "i"}})
#         if not restaurant:
#             dispatcher.utter_message(text=f"I'm sorry, I couldn't find a restaurant named '{value}'. Could you please check the spelling or provide another restaurant name?")
#             return {"restaurant_name": None}
        
#         return {"restaurant_name": restaurant["name"]}

#     def validate_phone_number(
#         self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
#     ) -> Dict[Text, Any]:
#         if not value:
#             dispatcher.utter_message(text="What is your phone number?")
#             return {"phone_number": None}

#         phone_pattern = r"^\d{10}$"
#         if not re.match(phone_pattern, value):
#             dispatcher.utter_message(text="Please provide a valid 10-digit phone number.")
#             return {"phone_number": None}
        
#         return {"phone_number": value}

#     def validate_email(
#         self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
#     ) -> Dict[Text, Any]:
#         if not value:
#             dispatcher.utter_message(text="What is your email?")
#             return {"email": None}

#         email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
#         if not re.match(email_pattern, value):
#             dispatcher.utter_message(text="This email is invalid. Please provide a valid email address.")
#             return {"email": None}

#         return {"email": value}

#     def validate_date(
#         self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
#     ) -> Dict[Text, Any]:
#         if not value:
#             dispatcher.utter_message(text="What date would you like to book? (e.g., 29 June, tomorrow, next Friday)")
#             return {"date": None}
        
#         try:
#             # Parse the date string
#             parsed_date, _ = cal.parseDT(value, datetime.now())
#             booking_date = parsed_date.date()
            
#             today = datetime.now().date()
#             if booking_date < today:
#                 dispatcher.utter_message(text="Sorry, you can't book for a date in the past. Please provide a future date.")
#                 return {"date": None}
#             if booking_date > today + timedelta(days=30):
#                 dispatcher.utter_message(text="Sorry, you can only book up to 30 days in advance. Please choose a closer date.")
#                 return {"date": None}
            
#             # Format the date as a string for storage
#             formatted_date = booking_date.strftime("%Y-%m-%d")
#             return {"date": formatted_date}
#         except ValueError:
#             dispatcher.utter_message(text="I couldn't understand that date. Please try again with a clearer date format.")
#             return {"date": None}

#     def validate_time(
#         self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
#     ) -> Dict[Text, Any]:
#         if not value:
#             dispatcher.utter_message(text="What time would you like to book? (e.g., 7pm, 10:30 pm, 14:00)")
#             return {"time": None}

#         try:
#             # Parse the time string
#             parsed_time, _ = cal.parseDT(value, datetime.now())
#             booking_time = parsed_time.time()
            
#             opening_time = datetime.strptime("11:00", "%H:%M").time()
#             closing_time = datetime.strptime("22:00", "%H:%M").time()
            
#             if booking_time < opening_time or booking_time > closing_time:
#                 dispatcher.utter_message(text="Sorry, bookings are only available between 11:00 AM and 10:00 PM. Please choose a time within this range.")
#                 return {"time": None}
            
#             # Format the time as a string for storage
#             formatted_time = booking_time.strftime("%H:%M")
#             return {"time": formatted_time}
#         except ValueError:
#             dispatcher.utter_message(text="I couldn't understand that time. Please try again with a clearer time format.")
#             return {"time": None}

# # class ActionSubmitForm(Action):
# #     def name(self) -> Text:
# #         return "action_submit_form"

# #     def run(
# #         self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
# #     ) -> List[Dict[Text, Any]]:
        
# #         # Retrieve slots from tracker
# #         user_name = tracker.get_slot("user_name")
# #         restaurant_name = tracker.get_slot("restaurant_name")
# #         phone_number = tracker.get_slot("phone_number")
# #         email = tracker.get_slot("email")
# #         date = tracker.get_slot("date")
# #         time = tracker.get_slot("time")

# #         # Save booking to MongoDB
# #         booking_data = {
# #             "user_name": user_name,
# #             "restaurant_name": restaurant_name,
# #             "phone_number": phone_number,
# #             "email": email,
# #             "date": date,
# #             "time": time,
# #             "booking_timestamp": datetime.now()
# #         }

# #         try:
# #             booking_collection.insert_one(booking_data)
# #             dispatcher.utter_message(
# #                 text="Thank you! Your booking has been confirmed.",
# #                 user_name=user_name,
# #                 restaurant_name=restaurant_name,
# #                 phone_number=phone_number,
# #                 email=email,
# #                 date=date,
# #                 time=time,
# #             )
# #         except Exception as e:
# #             dispatcher.utter_message(text="I'm sorry, there was an error saving your booking. Please try again later.")
# #             print(f"Error saving booking: {str(e)}")

# #         return []

# class ActionSubmitForm(Action):
#     def name(self) -> Text:
#         return "action_submit_form"

#     def run(
#         self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
#     ) -> List[Dict[Text, Any]]:
#         # Check if all required slots are filled
#         if all(tracker.get_slot(slot) for slot in ["user_name", "restaurant_name", "phone_number", "email", "date", "time"]):
#             # Retrieve slots from tracker
#             user_name = tracker.get_slot("user_name")
#             restaurant_name = tracker.get_slot("restaurant_name")
#             phone_number = tracker.get_slot("phone_number")
#             email = tracker.get_slot("email")
#             date = tracker.get_slot("date")
#             time = tracker.get_slot("time")

#             # Example logic to save booking or any other action
#             dispatcher.utter_message(
#                 text=f"Thank you {user_name}, your booking at {restaurant_name} on {date} at {time} has been confirmed."
#             )
#         else:
#             # Prompt user to fill remaining required slots
#             dispatcher.utter_message(template="utter_ask_" + next(self.required_slots()))

#         return []


# import logging
from typing import Any, Coroutine, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import SlotSet, EventType
from datetime import datetime, timedelta
import parsedatetime as pdt
import re
from pymongo import MongoClient
from rasa_sdk.types import DomainDict
from pymongo.errors import PyMongoError
# from logging.handlers import RotatingFileHandler
import os
# Set up logging
# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     filename='actions.log',  # Log file name
#     filemode='w'  # Overwrite the log file on each run
# )
# logger = logging.getLogger(__name__)

# if not os.path.exists('logs'):
#     os.makedirs('logs')

# # Set up logging
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

# # Create handlers
# c_handler = logging.StreamHandler()  # Console handler
# f_handler = RotatingFileHandler('logs/actions.log', maxBytes=10*1024*1024, backupCount=5)  # File handler

# # Create formatters and add it to handlers
# log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# c_handler.setFormatter(log_format)
# f_handler.setFormatter(log_format)

# # Add handlers to the logger
# logger.addHandler(c_handler)
# logger.addHandler(f_handler)


# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["Restaurants"]
collection = db["Zomato"]
booking_collection = db["Bookings"]

# Initialize parsedatetime
cal = pdt.Calendar()

class ValidateRestaurantForm(FormValidationAction):
    def name(self) -> Text:
        return "restaurant_form"

    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Text]:
        unfilled_slots = []

        # Check each slot if it's already filled or needs to be requested
        for slot_name in slots_mapped_in_domain:
            if tracker.slots.get(slot_name) is None:
                unfilled_slots.append(slot_name)

        return unfilled_slots if unfilled_slots else []

    def validate_user_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if isinstance(slot_value, str) and slot_value.strip():
            return {"user_name": slot_value}  # Valid name provided
        else:
            if not slot_value:
                # Slot value is None or empty string
                dispatcher.utter_message(text="Please provide a valid name.")
            return {"user_name": None}  # Return None to indicate slot is not filled yet

    def validate_restaurant_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if collection.find_one({"name": slot_value}):
            return {"restaurant_name": slot_value}
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find that restaurant. Please try again.")
            return {"restaurant_name": None}

    def validate_date(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        try:
            booking_date = datetime.strptime(slot_value, "%Y-%m-%d").date()
            today = datetime.now().date()
            if not (today <= booking_date <= today + timedelta(days=30)):
                dispatcher.utter_message(text="Please provide a date within the next 30 days.")
                return {"date": None}
            return {"date": slot_value}
        except ValueError:
            dispatcher.utter_message(text="Please provide a valid date in the format YYYY-MM-DD.")
            return {"date": None}

    def validate_time(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        try:
            time_formats = ["%I:%M %p", "%I %p", "%I:%M%p", "%I%p"]
            parsed_time = next((datetime.strptime(slot_value.upper(), fmt).time() for fmt in time_formats if self._try_parse_time(slot_value.upper(), fmt)), None)
            if not parsed_time:
                raise ValueError
            
            if not (datetime.strptime("10:00 AM", "%I:%M %p").time() <= parsed_time <= datetime.strptime("10:00 PM", "%I:%M %p").time()):
                dispatcher.utter_message(text="Please provide a time between 10:00 AM and 10:00 PM.")
                return {"time": None}
            
            return {"time": parsed_time.strftime("%I:%M %p")}  # Store in 12-hour format
        except ValueError:
            dispatcher.utter_message(text="Please provide a valid time (e.g., 7 pm, 9:30 pm).")
            return {"time": None}

    def _try_parse_time(self, time_str: Text, time_format: Text) -> bool:
        try:
            datetime.strptime(time_str, time_format)
            return True
        except ValueError:
            return False

    def validate_email(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if "@" in slot_value:
            return {"email": slot_value}
        else:
            dispatcher.utter_message(text="Please provide a valid email address.")
            return {"email": None}
        
    def validate_phone_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if slot_value.isdigit() and len(slot_value) == 10:
            return {"phone_number": slot_value}
        else:
            dispatcher.utter_message(text="Please provide a valid 10-digit phone number.")
            return {"phone_number": None}


class ActionSubmitForm(Action):
    def name(self) -> Text:
        return "action_submit_form"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:
        user_name = tracker.get_slot("user_name")
        restaurant_name = tracker.get_slot("restaurant_name")
        date = tracker.get_slot("date")
        time = tracker.get_slot("time")
        email = tracker.get_slot("email")
        phone_number = tracker.get_slot("phone_number")

             # Check if all required slots are filled
        if not all([user_name, restaurant_name, date, time, email, phone_number]):
            # Prompt the user to fill all the required details
            dispatcher.utter_message(text="Please fill all the required details to book the restaurant.")
            return [SlotSet("restaurant_form", None)]  # Reset the form to ensure it stays active

        booking_details = {
            "user_name": user_name,
            "restaurant_name": restaurant_name,
            "date": date,
            "time": time,
            "email": email,
            "phone_number": phone_number,
        }

        # Insert booking details into the bookings collection
        booking_collection.insert_one(booking_details)

        dispatcher.utter_message(response="utter_confirm_booking", 
                                 user_name=user_name, 
                                 restaurant_name=restaurant_name, 
                                 date=date, 
                                 time=time, 
                                 email=email, 
                                 phone_number=phone_number)

        return [SlotSet(slot_name, None) for slot_name in booking_details.keys()]
