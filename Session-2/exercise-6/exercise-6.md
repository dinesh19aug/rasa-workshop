## Execise: Connecting to API

- Open actions.py
- Replace everything with following code

```
# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet,FollowupAction 
from rasa_sdk.forms import FormAction

##Code credit - https://github.com/RasaHQ
# We use the medicare.gov database to find information about 3 different
# healthcare facility types, given a city name, zip code or facility ID
# the identifiers for each facility type is given by the medicare database
# xubh-q36u is for hospitals
# b27b-2uc7 is for nursing homes
# 9wzi-peqs is for home health agencies

ENDPOINTS = {
    "base": "https://data.medicare.gov/resource/{}.json",
    "xubh-q36u": {
        "city_query": "?city={}",
        "zip_code_query": "?zip_code={}",
        "id_query": "?provider_id={}"
    },
    "b27b-2uc7": {
        "city_query": "?provider_city={}",
        "zip_code_query": "?provider_zip_code={}",
        "id_query": "?federal_provider_number={}"
    },
    "9wzi-peqs": {
        "city_query": "?city={}",
        "zip_code_query": "?zip={}",
        "id_query": "?provider_number={}"
    }
}

FACILITY_TYPES = {
    "hospital":
        {
            "name": "hospital",
            "resource": "xubh-q36u"
        },
    "nursing_home":
        {
            "name": "nursing home",
            "resource": "b27b-2uc7"
        },
    "home_health":
        {
            "name": "home health agency",
            "resource": "9wzi-peqs"
        }
}

def _create_path(base: Text, resource: Text,
                 query: Text, values: Text) -> Text:
    """Creates a path to find provider using the endpoints."""

    if isinstance(values, list):
        return (base + query).format(
            resource, ', '.join('"{0}"'.format(w) for w in values))
    else:
        return (base + query).format(resource, values)


def _find_facilities(location: Text, resource: Text) -> List[Dict]:
    """Returns json of facilities matching the search criteria."""

    if str.isdigit(location):
        full_path = _create_path(ENDPOINTS["base"], resource,
                                 ENDPOINTS[resource]["zip_code_query"],
                                 location)
    else:
        full_path = _create_path(ENDPOINTS["base"], resource,
                                 ENDPOINTS[resource]["city_query"],
                                 location.upper())
    #print("Full path:")
    #print(full_path)
    results = requests.get(full_path).json()
    return results


def _resolve_name(facility_types, resource) ->Text:
    for key, value in facility_types.items():
        if value.get("resource") == resource:
            return value.get("name")
    return ""

class FindFacilityTypes(Action):
    """This action class allows to display buttons for each facility type
    for the user to chose from to fill the facility_type entity slot."""

    def name(self) -> Text:
        """Unique identifier of the action"""

        return "find_facility_types"


    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List:

        buttons = []
        for t in FACILITY_TYPES:
            facility_type = FACILITY_TYPES[t]
            payload = "/inform{\"facility_type\": \"" + facility_type.get(
                "resource") + "\"}"

            buttons.append(
                {"title": "{}".format(facility_type.get("name").title()),
                 "payload": payload})

        # TODO: update rasa core version for configurable `button_type`
        dispatcher.utter_button_template("utter_greet", buttons, tracker)
        return []


class FindHealthCareAddress(Action):
    """This action class retrieves the address of the user's
    healthcare facility choice to display it to the user."""

    def name(self) -> Text:
        """Unique identifier of the action"""

        return "find_healthcare_address"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict]:

        facility_type = tracker.get_slot("facility_type")
        healthcare_id = tracker.get_slot("facility_id")
        full_path = _create_path(ENDPOINTS["base"], facility_type,
                                 ENDPOINTS[facility_type]["id_query"],
                                 healthcare_id)
        results = requests.get(full_path).json()
        if results:
            selected = results[0]
            if facility_type == FACILITY_TYPES["hospital"]["resource"]:
                address = "{}, {}, {} {}".format(selected["address"].title(),
                                                 selected["city"].title(),
                                                 selected["state"].upper(),
                                                 selected["zip_code"].title())
            elif facility_type == FACILITY_TYPES["nursing_home"]["resource"]:
                address = "{}, {}, {} {}".format(selected["provider_address"].title(),
                                                 selected["provider_city"].title(),
                                                 selected["provider_state"].upper(),
                                                 selected["provider_zip_code"].title())
            else:
                address = "{}, {}, {} {}".format(selected["address"].title(),
                                                 selected["city"].title(),
                                                 selected["state"].upper(),
                                                 selected["zip"].title())

            return [SlotSet("facility_address", address)]
        else:
            print("No address found. Most likely this action was executed "
                  "before the user choose a healthcare facility from the "
                  "provided list. "
                  "If this is a common problem in your dialogue flow,"
                  "using a form instead for this action might be appropriate.")

            return [SlotSet("facility_address", "not found")]


class FacilityForm(FormAction):
    """Custom form action to fill all slots required to find specific type
    of healthcare facilities in a certain city or zip code."""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "facility_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["facility_type", "location"]

    def slot_mappings(self) -> Dict[Text, Any]:
        return {"facility_type": self.from_entity(entity="facility_type",
                                                  intent=["inform",
                                                          "search_provider"]),
                "location": self.from_entity(entity="location",
                                             intent=["inform",
                                                     "search_provider"])}

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]
               ) -> List[Dict]:
        """Once required slots are filled, print buttons for found facilities"""

        location = tracker.get_slot('location')
        facility_type = tracker.get_slot('facility_type')

        results = _find_facilities(location, facility_type)
        button_name = _resolve_name(FACILITY_TYPES, facility_type)
        if len(results) == 0:
            dispatcher.utter_message(
                "Sorry, we could not find a {} in {}.".format(button_name,
                                                              location.title()))
            return []

        buttons = []
        # limit number of results to 3 for clear presentation purposes
        for r in results[:3]:
            if facility_type == FACILITY_TYPES["hospital"]["resource"]:
                facility_id = r.get("provider_id")
                name = r["hospital_name"]
            elif facility_type == FACILITY_TYPES["nursing_home"]["resource"]:
                facility_id = r["federal_provider_number"]
                name = r["provider_name"]
            else:
                facility_id = r["provider_number"]
                name = r["provider_name"]

            payload = "/inform{\"facility_id\":\"" + facility_id + "\"}"
            buttons.append(
                {"title": "{}".format(name.title()), "payload": payload})

        if len(buttons) == 1:
            message = "Here is a {} near you:".format(button_name)
        else:
            if button_name == "home health agency":
                button_name = "home health agencie"
            message = "Here are {} {}s near you:".format(len(buttons),
                                                         button_name)

        # TODO: update rasa core version for configurable `button_type`
        dispatcher.utter_button_message(message, buttons)

        return []
```

- Add some more intents in data/nlu.md file

```
## intent:affirm
- yes
- yes sure
- absolutely
- for sure
- yes yes yes
- definitely
- yeah
- si
- ok
- okay


## synonym:xubh-q36u
- hospital
- hospitals

## synonym:9wzi-peqs
- home health agency
- home health agencies

## synonym:b27b-2uc7
- nursing home
- nursing homes
```

- Update existing intents

```
## intent:goodbye
- Bye
- Bye!
- Goodbye
- See you later
- Bye bot
- Goodbye friend
- bye
- bye for now
- catch you later
- gotta go
- See you
- goodnight
- have a nice day
- i'm off
- see you later alligator
- we'll speak soon

## intent:inform
- [Sitka](location)
- [Juneau](location)
- [Virginia](location)
- [Cusseta](location)
- [Chicago](location)
- [Tucson](location)
- [Columbus](location)
- [Valdez](location)
- [Preston](location)
- [Huntsville](location)
- [Boulder](location)
- [California](location)
- [Tulsa](location)
- [Colorado](location)
- [Goodyear](location)
- [Albuquerque](location)
- [Scottsdale](location)
- [Hibbing](location)
- [Norman](location)
- [San](location)
- [Peoria](location)
- [New](location)
- [Corpus](location)
- [Montgomery](location)
- [Wichita](location)
- [Aurora](location)
- [Denver](location)
- [Sierra](location)
- [Georgetown](location)
- [Birmingham](location)
- [Fayetteville](location)
- [Carson](location)
- [Raleigh](location)
- [Bakersfield](location)
- [Mobile](location)
- [Detroit](location)
- [Bunnell](location)
- [Chattanooga](location)
- [Mesa](location)
- [Fernley](location)
- [Marana](location)
- [Yuma](location)
- [Little](location)
- [Athens](location)
- [Hartsville](location)
- [Port](location)
- [Tampa](location)
- [Fresno](location)
- [Unalaska](location)
- [Eloy](location)
- [Salt](location)
- [Jackson](location)
- [Fort](location)
- [Casa](location)
- [Charleston](location)
- [Henderson](location)
- [Durham](location)
- [Abilene](location)
- [Palmdale](location)
- [Babbitt](location)
- [Surprise](location)
- [Cape](location)
- [Shreveport](location)
- [Rio](location)
- [Savannah](location)
- [Reno](location)
- [Orlando](location)
- [North](location)
- [Tallahassee](location)
- [Amarillo](location)
- [St](location)
- [Knoxville](location)
- [Sacramento](location)
- [Clarksville](location)
- [Los Angeles](location)
- [New York](location)
- [Las Vegas](location)
- [San Diego](location)
- [San Antonio](location)
- [El Paso](location)
- [Kansas location](location)
- [San Francisco](location)
- [Santa Barbara](location)
- [home health agency](facility_type)
- [hospital](facility_type)
- [nursing home](facility_type)
- a [home health agency](facility_type)
- a [hospital](facility_type)
- a [nursing home](facility_type)

## intent:search_provider
- i need a [hospital](facility_type)
- find me a nearby [hospital](facility_type)
- show me [hospitals](facility_type)
- [hospital](facility_type)
- find me a nearby [hospital](facility_type) my zip code is [10119](location)
- i need a [home health agency](facility_type)
- find me a nearby [home health agency](facility_type)
- show me [home health agency](facility_type)
- [home health agency](facility_type)
- find me a nearby [home health agency](facility_type) my zip code is [10119](location)
- find me a nearby [nursing home](facility_type)
- show me [nursing home](facility_type)
- [nursing home](facility_type)
- find me a nearby [nursing home](facility_type) my zip code is [10119](location)
- i need a [hospital](facility_type) my zip code is [77494](location)
- my zip code is [30277](location) and i need a [nursing home](facility_type)
- my zip code is [86602](location) and i need a [hospital](facility_type)
- my zip code is [47516](location) and i need a [home health agency](facility_type)
- i need a [nursing home](facility_type) at [77474](location)
- i need a [hospital](facility_type) at [77474](location)
- i need a [home health agency](facility_type) at [77474](location)
- i am in [Amarillo](location) and i need a [nursing home](facility_type)
- i am in [New York](location) and i need a [hospital](facility_type)
- i am in [Las Vegas](location) and i need a [home healt agency](facility_type)
- i need a [nursing home](facility_type) in [Katy](location)
- i need a [hospital](facility_type) in [Waco](location)
- i need a [home health agency](facility_type) in [Clarksville](location)
- show me [nursing home](facility_type) in [Knoxville](location)
- show me [hospital](facility_type) in [Durham](location)
- show me [home health agency](facility_type) in [Detroit](location)
- find me a nearby [home health agency](facility_type) in [Reno](location)
- hi i am in [Tampa](location) i need a [nursing  home](facility_type:b27b-2uc7)
- hi i am in [San Diego](location) i need a [hospital](facility_type:xubh-q36u)
- hi i am in [Nashville](location) i need a [home health agenc](facility_type:9wzi-peqs)
- hi i am in [Sacramento](location) i need a [nursing  home](facility_type:b27b-2uc7)
- hi i am in [Springfield](location) i need a [hospital](facility_type:xubh-q36u)
- hi i am in [Atlanta](location) i need a [home health agenc](facility_type:9wzi-peqs)
- hi i am in [Chicago](location) i need a [nursing  home](facility_type:b27b-2uc7)
- hi i am in [Santa Cruz](location) i need a [hospital](facility_type:xubh-q36u)
- hi i am in [Boston](location) i need a [home health agenc](facility_type:9wzi-peqs)
- hello i am in [Tampa](location) i need a [nursing  home](facility_type:b27b-2uc7)
- hello i am in [San Diego](location) i need a [hospital](facility_type:xubh-q36u)
- hello i am in [Nashville](location) i need a [home health agenc](facility_type:9wzi-peqs)
- hello i am in [Sacramento](location) i need a [nursing  home](facility_type:b27b-2uc7)
- hello i am in [Springfield](location) i need a [hospital](facility_type:xubh-q36u)
- hello i am in [Atlanta](location) i need a [home health agenc](facility_type:9wzi-peqs)
- hello i am in [Chicago](location) i need a [nursing  home](facility_type:b27b-2uc7)
- hello i am in [Santa Cruz](location) i need a [hospital](facility_type:xubh-q36u)
- hello i am in [Boston](location) i need a [home health agenc](facility_type:9wzi-peqs)
- Good morning i am in [Tampa](location) i need a [nursing  home](facility_type:b27b-2uc7)
- Good morning i am in [San Diego](location) i need a [hospital](facility_type:xubh-q36u)
- Good morning i am in [Nashville](location) i need a [home health agenc](facility_type:9wzi-peqs)
- Good morning i am in [Sacramento](location) i need a [nursing  home](facility_type:b27b-2uc7)
- Good morning i am in [Springfield](location) i need a [hospital](facility_type:xubh-q36u)
- Good morning i am in [Atlanta](location) i need a [home health agenc](facility_type:9wzi-peqs)
- Good morning i am in [Chicago](location) i need a [nursing  home](facility_type:b27b-2uc7)
- Good morning i am in [Santa Cruz](location) i need a [hospital](facility_type:xubh-q36u)
- Good morning i am in [Boston](location) i need a [home health agenc](facility_type:9wzi-peqs)
- Hello again i need a [nursing home](facility_type) in [Katy](location)
- Hello again i need a [hospital](facility_type) in [Waco](location)
- Hello again i need a [home health agency](facility_type) in [Clarksville](location)
- Good morning i need a [nursing home](facility_type) in [Katy](location)
- Good morning i need a [hospital](facility_type) in [Waco](location)
- Good morning i need a [home health agency](facility_type) in [Clarksville](location)
- Can you tell me a [nursing home](facility_type) in [Oklahoma City](location) ?

## intent:thanks
- Thanks
- Thank you
- Thank you so much
- Thanks bot
- Thanks for that
- cheers
- cheers bro
- ok thanks!
- perfect thank you
- thanks a bunch for everything
- thanks for the help
- thanks a lot
- amazing, thanks
- cool, thanks
- cool thank you


## intent:mood_great
- perfect
- very good
- great
- amazing
- wonderful
- I am feeling very good
- I am great
- I'm good

## intent:mood_unhappy
- sad
- very sad
- unhappy
- bad
- very bad
- awful
- terrible
- not very good
- extremely sad
- so sad

## regex:location
- [0-9]{5}
```

- Add another policy in config.yml file

```
  - name: KerasPolicy
  - name: FormPolicy
  - name: TwoStageFallbackPolicy
```

- Retrain the nlu model
```
rasa train nlu
```

- Test the nlu mode
```
rasa shell nlu

Try few sample queries:
- In need a hsopital
- I need a doctor in charlotte NC

```

- Notice the intent section. 
```
"entities": [
    {
      "entity": "facility_type",
      "start": 7,
      "end": 15,
      "value": "xubh-q36u", ***********
      "extractor": "DIETClassifier",
      "processors": [
        "EntitySynonymMapper"
      ]
    }
  ],
```

- Now go ahead and update the stories

```
## happy_path
* greet
    - find_facility_types
* inform{"facility_type": "xubh-q36u"}    
    - facility_form
    - form{"name": "facility_form"}
    - form{"name": null}
* inform{"facility_id": 4245}
    - find_healthcare_address
    - utter_address
* thanks
    - utter_noworries

## happy_path_multi_requests
* greet
    - find_facility_types
* inform{"facility_type": "xubh-q36u"}
    - facility_form
    - form{"name": "facility_form"}
    - form{"name": null}
* inform{"facility_id": "747604"}
    - find_healthcare_address
    - utter_address
* search_provider{"facility_type": "xubh-q36u"}
    - facility_form
    - form{"name": "facility_form"}
    - form{"name": null}
* inform{"facility_id": 4245}   
    - find_healthcare_address
    - utter_address

## happy_path2
* search_provider{"location": "Austin", "facility_type": "xubh-q36u"}
    - facility_form
    - form{"name": "facility_form"}
    - form{"name": null}
* inform{"facility_id": "450871"}
    - find_healthcare_address
    - utter_address
* thanks
    - utter_noworries

## story_goodbye
* goodbye
    - utter_goodbye

## story_thankyou
* thanks
    - utter_noworries
```

- Update the domain for new intents

```
Under intents
 - out_of_scope
```

 Under entities
```
  - facility_id
```
 Slots:
```
 slots:
  facility_type:
    type: unfeaturized
  facility_address:
    type: unfeaturized
  facility_id:
    type: unfeaturized
  location:
    type: unfeaturized
```
Add forms:
```
forms:
- facility_form
```
Update actions
```
actions:
  - utter_noworries
  - utter_greet
  - utter_goodbye
  - utter_ask_location
  - utter_ask_facility_type
  - find_facility_types
  - find_healthcare_address
  - utter_address
```

Update responses

```
utter_greet:
  - text: "Hi. What are you looking for?"
  - text: "Hey there! Please choose one of the healthcare facility options:"
  - text: "Hello! What can I help you find today?"

  utter_goodbye:
  - text: "Talk to you later!"
  - text: "Have a good day."
  - text: "Until next time!"

  utter_noworries:
  - text: "My pleasure."
  - text: "You are welcome!"

  utter_ask_facility_type:
  - text: "Choose one of the following to search for: hospital, nursing home, or home health agency."

  utter_ask_location:
  - text: "Please provide your city name."
  - text: "What is your current city?"
  - text: "Please provide your city name or zip code."
  - text: "Please enter your zip code or city name to find local providers."

  utter_address:
  - text: "The address is {facility_address}."

```

- Train

```
rasa train
```

- run
```
rasa run actions
rasa shell
```