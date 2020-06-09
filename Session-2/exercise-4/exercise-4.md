## Execise: Add a new slot for location and facility

- Open domain.yml and two text slots for location and facility_type

```
slots:
  location:
    type: text
  facility_type:
    type: text  
```

- Update the uttereance to use slots.

```
  utter_ask_location:
  - text: "Can you please specify your city or zipcode?" 
  - text: "I need the address to find the nearest {facility_type}"
```

Ex - The above utterance can be used when users asks why do you need my city or zipcode. This is one of the ways to bring customer back to story flow.

- Slots are also useful for custom actions.
- Update the action.py class

```
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
        dispatcher.utter_message(text="Here's the dummy address for {} in {}: {}".format(facility, location, dummy_address))

        return []
```

- Train and run 
- Now if you want to store some result when the custom actions returns a value then it can be done via slot event.
- Add a new import
```
from rasa_sdk.events import SlotSet
```

- Update the run to set the value address in address slot

```
return [SlotSet("address", dummy_address)]
```

- Now we need to tell RASA on what to do with this returned value. To do this it needs to be reflected in Story

```
## Search hospital happy path. Facility name with city or zip code 
* greet
  - utter_greet
  - utter_how_help
* search_provider{"facility_type":"hospital", "location":"St Louis"}
  - action_facility_search
  - slot{"address":"Some address is returned"}
* thanks
  - utter_goodbye

## Search facility with no city or zip code
* greet
  - utter_greet
  - utter_how_help
* search_provider{"facility_type":"hospital"}
  - utter_ask_location
* inform{"location":"Charlotte"}
  - action_facility_search
  - slot{"address":"Some address is returned"}
* thanks
  - utter_goodbye
```

- Let the domain know about.

```
  address:
    type: unfeaturized
```

- Notice that it is set as unfaeturized because at this point we dont know what to do with it and it should not affect the call flow.

- Train again and run