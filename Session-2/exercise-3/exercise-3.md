## Execise: Review the actions file

- Open the actions.py file
- Review how to write a custom hello world message.
- There are two methods name and run.

> def name: defines the name of the custom action that is defined in the domain. This is how RASA knows how to connect the domain custom action with actions class.

> def run: Where we define on what to do - call database, api, service, read file etc. It accepts tracker to keep a context in the memory slot and dispatcher to return the response.

- Let's update this file to look for a hospital by calling a free API - http://www.communitybenefitinsight.org/api/get_hospitals.php. (In next exercise though not now)

- Before we do something complicated, lets return a dummy address to see if the custom action works.

- Update the **name** method to identify action_facility_search

```
 from typing import Any, Text, Dict, List

 from rasa_sdk import Action, Tracker
 from rasa_sdk.executor import CollectingDispatcher


 class ActionHelloWorld(Action):

     def name(self) -> Text:
         return "action_facility_search"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         dispatcher.utter_message(text="Here's the dummy address!")

         return []
```

- Re train your nlu model
```
rasa train nlu
```

- Retarin the core as well
```
rasa train
```

- Run the test
```
rasa shell
```

- You should see error when bot tries to call the custom action.

```
Your input ->  Good. I need a hospital
Can you please specify your city or zipcode?
Your input ->  Charlotte
2020-06-07 22:43:58 ERROR    rasa.core.actions.action  - The model predicted the custom action 'action_facility_search', but you didn't configure an endpoint to run this custom action. Please take a look at the docs and set an endpoint configuration via the --endpoints flag. https://rasa.com/docs/rasa/core/actions
2020-06-07 22:43:58 ERROR    rasa.core.processor  - Encountered an exception while running action 'action_facility_search'. Bot will continue, but the actions events are lost. Please check the logs of your action server for more information.
```

- In rasa each action.py file is a python file that needs to run on a server. To activate it enable the enpoints.yml, which is going to host this actions.py. by default it will be hosted on localhost:5055
Uncomment the following line in endppoints.yml
```
action_endpoint:
  url: "http://localhost:5055/webhook"
```

- Re-train
```
rasa train
```

- Run the actions
```
rasa run actions
```

- In a new command window, run the shell

```
rasa shell
```

