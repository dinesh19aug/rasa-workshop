## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot

## Search hospital happy path. Facility name with city or zip code 
* greet
  - utter_greet
  - utter_how_help
* search_provider{"facility_type":"hospital", "location":"St Louis"}
  - action_facility_search
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
* thanks
  - utter_goodbye