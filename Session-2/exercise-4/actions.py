# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_facility_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #get the facility type that use is searching
        facility = tracker.get_slot("facility_type")
        location = tracker.get_slot("location")
        dummy_address= "1000 Medical Plaza dr"
        dispatcher.utter_message("Here's the dummy address for {} in {}: {}".format(facility, location, dummy_address))

        return [SlotSet("address", dummy_address)]
