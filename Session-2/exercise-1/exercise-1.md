## Execise: Add new story for search medical facility

### Steps:
- open "data/stories.md"
- Add the below story
```
## Search hospital happy path. Facility name with city or zip code 
* greet
  - utter_greet
* search_provider{"facility_type":"hospital", "location":"St Louis"}
  - action_facility_search
* thanks
  - utter_goodbye
```

> Pre defined bot uttereances start with utter_xxx and custom actiions starts with action_xxx

- Add few more stories so that model could learn. 
- Let's add story where user does not provide location

```
## Search facility with no city or zip code
* greet
  - utter_greet
* search_provider{"facility_type":"hospital"}
  - utter_ask_location
* inform{"location":"Charlotte"}
  - action_facility_search
* thanks
  - utter_goodbye
```

- Try training the model

```
rasa train
```

> Did you notice the error?

```
  File "c:\users\dines\anaconda3\envs\workshop\lib\site-packages\rasa\core\domain.py", line 548, in _raise_action_not_found_exception
    f"Cannot access action '{action_name}', "
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