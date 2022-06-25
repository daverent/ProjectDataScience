import datetime as dt
from typing import Any, Text, Dict, List
from os import path

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import json


class ActionTime(Action):

    def name(self) -> Text:
        return "action_show_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=f"{dt.datetime.now()}")

        return []


class ActionSaySupportType(Action):

    def name(self) -> Text:
        return "action_say_support_type"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        support_type = tracker.get_slot("support_type")
        if not support_type:
            dispatcher.utter_message(
                text="I don't know the kind of support you asked for.")
        else:
            dispatcher.utter_message(
                text=f"You requested {support_type} support!")
        return []


class ActionCheckProductTips(Action):

    def name(self) -> Text:
        return "action_check_product_tips"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        file = "json/products.json"

        product_id = str(tracker.get_slot("product_id"))

        dispatcher.utter_message(
            text=f"You requested support for product: {product_id}")

        if path.isfile(file):
            with open('json/products.json') as json_file:
                data = json.load(json_file)

            products = data['products']  # Scarto l'indentazione dei prodotti

            chosen = {}
            for prod in products:
                if prod['product_id'] == product_id.lower():
                    chosen = prod  # Scelgo il prodotto richiesto
            
            image = chosen["image"]
            dispatcher.utter_message(image=image)

            if chosen:
                first = True
                # Ciclo per stampare soluzioni
                for solution in chosen['solutions']:
                    if first:
                        dispatcher.utter_message(
                            text="One possible previously provided solution for your product:")
                    else:
                        dispatcher.utter_message(
                            text="Another previously provided solution:")
                    dispatcher.utter_message(text=solution['text'])
                    first = False

            else:
                dispatcher.utter_message(
                    text=f"We don't have any previously provided solutions for your product.")
    
        else:
            dispatcher.utter_message(
                text=f"We don't have any previously provided solutions for your product.")


class ActionSaveTechnicalTicket(Action):

    def name(self) -> Text:
        return "action_save_technical_ticket"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        file = 'json/technical_tickets.json'

        name = tracker.get_slot("name")
        surname = tracker.get_slot("surname")
        product_id = tracker.get_slot("product_id")
        email = tracker.get_slot("email")
        phone_number = tracker.get_slot("phone_number")

        if path.isfile(file):

            with open(file) as fp:
                tickets = json.load(fp)
            ticket_id = tickets[-1]['ticket_id']+1
            data_ticket = {'ticket_id': ticket_id, 'name': name, 'surname': surname,
                           'product_id': product_id, 'email': email, 'phone_number': phone_number}
            data = tickets + [data_ticket]

        else:
            data = [{'ticket_id': 0, 'name': name, 'surname': surname,
                     'product_id': product_id, 'email': email, 'phone_number': phone_number}]

        with open(file, 'w') as outfile:
            json.dump(data, outfile)


class ActionSaveFinancialTicket(Action):

    def name(self) -> Text:
        return "action_save_financial_ticket"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        file = 'json/financial_tickets.json'

        name = tracker.get_slot("name")
        surname = tracker.get_slot("surname")
        email = tracker.get_slot("email")
        phone_number = tracker.get_slot("phone_number")

        if path.isfile(file):

            with open(file) as fp:
                tickets = json.load(fp)
            ticket_id = tickets[-1]['ticket_id']+1
            data_ticket = {'ticket_id': ticket_id, 'name': name,
                           'surname': surname, 'email': email, 'phone_number': phone_number}
            data = tickets + [data_ticket]

        else:
            data = [{'ticket_id': 0, 'name': name, 'surname': surname,
                     'email': email, 'phone_number': phone_number}]

        with open(file, 'w') as outfile:
            json.dump(data, outfile)

class ActionSaveTechnologicalTicket(Action):

    def name(self) -> Text:
        return "action_save_technological_ticket"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        file = 'json/technological_tickets.json'

        name = tracker.get_slot("name")
        surname = tracker.get_slot("surname")
        technological_problem = tracker.get_slot("technological_problem")
        email = tracker.get_slot("email")
        phone_number = tracker.get_slot("phone_number")

        if path.isfile(file):

            with open(file) as fp:
                tickets = json.load(fp)
            ticket_id = tickets[-1]['ticket_id']+1
            data_ticket = {'ticket_id': ticket_id, 'name': name, 'technological_problem': technological_problem,
                           'surname': surname, 'email': email, 'phone_number': phone_number}
            data = tickets + [data_ticket]

        else:
            data = [{'ticket_id': 0, 'name': name, 'surname': surname, 'technological_problem': technological_problem,
                     'email': email, 'phone_number': phone_number}]

        with open(file, 'w') as outfile:
            json.dump(data, outfile)