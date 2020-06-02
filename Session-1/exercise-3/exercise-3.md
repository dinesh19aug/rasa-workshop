## Execise: Add intents and stories for bot that will find the hospital for you

### Steps:
- Open the nlu.md and stories.md file
- Add the entities and its label to **intent:inform**
- Update nlu.md for **inform** and **search_type** intent
```
## intent:inform
- [Charlotte](location)
- [Davidson](location)
- [Virginia](location)
- [Cusseta](location)
- [Chicago](location)
- [Tuscon](location)
- [Columbus](location)
- [San Francisco](location)


## intent:search_provider
- I need a hospital
- find me a nearby hospital
- show me home health agencies
- hospital
- find me a nearby hospital in [Charlotte](location)
- I need a home health agency
```

- Can you spot any other entities? How about type of facility?

- Remember a user can also search for dentist office or nursing home etc. Let's identify those as label search facility.

- Train the model
```
rasa train nlu
```

- test the model
```
rasa shell
```

- Try the following messages:
```
- hospital
- find me a hospital in charlotte
- find me a dentist in San mateo 94403
```

- Do you understand the output now? What is the difference between exercise 2 and exercise 3 outputs?

```
find me a hospital in charlotte 28262
{
  "intent": {
    "name": "search_provider",
    "confidence": 0.9999931454658508
  },
  "entities": [
    {
      "entity": "facility_type",
      "start": 10,
      "end": 18,
      "value": "hospital",
      "extractor": "DIETClassifier"
    },
    {
      "entity": "location",
      "start": 22,
      "end": 31,
      "value": "charlotte",
      "extractor": "DIETClassifier"
    },
    {
      "entity": "zipcode",
      "start": 32,
      "end": 37,
      "value": "28262",
      "extractor": "DIETClassifier"
    }
  ],
  "intent_ranking": [
    {
      "name": "search_provider",
      "confidence": 0.9999931454658508
    },
    {
      "name": "greet",
      "confidence": 6.706336989736883e-06
    },
    {
      "name": "goodbye",
      "confidence": 1.2057277842814074e-07
    },
    {
      "name": "inform",
      "confidence": 3.071594179004933e-08
    }
  ],
  "response_selector": {
    "default": {
      "response": {
        "name": null,
        "confidence": 0.0
      },
      "ranking": [],
      "full_retrieval_intent": null
    }
  },
  "text": "find me a hospital in charlotte 28262"
}

```