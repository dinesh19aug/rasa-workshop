## Execise: Explore the existing domain

### Steps:
- Open the domain.yml file
- Look at what is defined?
> Can you spot the 4 core components of our chatbot - Intent, response, actiions etc?

- Do you understand why bot complained when you tried to train the bot in previous exercise?

```
    "Cannot access action '{action_name}', "
NameError: Cannot access action 'action_facility_search', as that name is not a registered action for this domain. Available actions are:
         - action_listen
         - action_restart
         - action_session_start
         - action_default_fallback
         - action_deactivate_form
         - action_revert_fallback_events
         - action_default_ask_affirmation
         - action_default_ask_rephrase
         - action_back
         - utter_cheer_up
         - utter_did_that_help
         - utter_goodbye
         - utter_greet
         - utter_happy
         - utter_iamabot
```

- Look at intents - do you see which  intents are missing? Hint: nlu.md
- Add the missing intents.

```
  - inform
  - search_provider
```

- Let's add default bot responses from our stories. Find any missing utterences. Hint: stories.md

```
utter_ask_location:
  - text: "Can you please specify your city or zipcode?" 
```

- Is that all? Not yet - What about entities? How do we tell bot to identtify entities? Good observation. Let's add that

```
entities:
  - facility_type
  - location
```

- Now let's add our custom action

```
actions:
  - action_facility_search
```

- train the model and notice the missing intent message

```
rasa train
```

>c:\users\dines\anaconda3\envs\workshop\lib\site-packages\rasa\core\training\dsl.py:431: UserWarning: Found unknown intent 'thanks' on line 39. Please, make sure that all intents are listed in your domain yaml.

- Go ahead and fix this. DIY task.

- Why are we not using "rasa train nlu". rasa train nlu is used when you add some new uttereances that customer may utter. If there is no change in the nlu.md file then you don't need to retrain your model.

>Logs: Core model training completed.
NLU data/configuration did not change. No need to retrain NLU model.

- Run and test the model.

```
rasa shell
```

- Try the following. 

```
I need a hospital in 28027
I need a doctor
I need a doctor (Respond with Charlotte when bot asks for location)
I need a doctor in Charlotte
```

- In the next exercise we will fix the error for custom action 

