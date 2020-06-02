## Execise: Add intents and stories for bot that will find the hospital for you

### Steps:
- Open the nlu.md and stories.md file
- The deafult bot has some pre-defined inetents for you in nlu.md file. Add few more if you like for greetings. intent:greet and intent:goodbye
- Delete all intents other than greet and goodbye.
- Based on the flow, you need an intent for customer queries, additional question from bot if it needs information from custome like zipcode or city and  bot responses to customer queries.

- Creat a intent for how users would provide thier location. Ex: List of cities that user may provide. Add internt:inform as below
```
## intent:inform
- Charlotte
- Davidson
- Virginia
- Cusseta
- Chicago
- Tuscon
- Columbus
- San Francisco

```

- Add the questions or queries that users may provide. Add a new intent in nlu.md as intent: search provider

```
## intent:search_provider
- I need a hospital
- find me a nearby hospital
- show me home health agencies
- hospital
- find me a nearby hospital in Charlotte
- I need a home health agency

```

- Stop and think. The above only classifies the intents of customer. We will cover this in episode 3. For now save the file and see what happens if we train the model.
- On terminal
```
rasa train nlu

```

- After the training is complete.
```
rasa shell
```

- Unlike the last time you will see message
```
Next message
```
Try the below quesries:
1. Find me a nearby hospital
2. find me a hospital in Charlotte 
3. Charlotte, NC
4. San Mateo
5. San Mateo, California
6. San mateo 94403
7. 94403
8. St Louis
9. St Louis Missouri

- Review the responses. Do you undesrstand what the response is telling you. Here's a sample

```
St Louis, Missouri
{
  "intent": {
    "name": "inform",
    "confidence": 0.9885903000831604
  },
  "entities": [],
  "intent_ranking": [
    {
      "name": "inform",
      "confidence": 0.9885903000831604
    },
    {
      "name": "goodbye",
      "confidence": 0.007535217329859734
    },
    {
      "name": "search_provider",
      "confidence": 0.0036257263273000717
    },
    {
      "name": "greet",
      "confidence": 0.00024872052017599344
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
  "text": "St Louis, Missouri"
}
```

```
hospital in charlotte
{
  "intent": {
    "name": "search_provider",
    "confidence": 0.999701738357544
  },
  "entities": [],
  "intent_ranking": [
    {
      "name": "search_provider",
      "confidence": 0.999701738357544
    },
    {
      "name": "goodbye",
      "confidence": 0.00018934565014205873
    },
    {
      "name": "greet",
      "confidence": 7.495113823097199e-05
    },
    {
      "name": "inform",
      "confidence": 3.3948028431041166e-05
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
  "text": "hospital in charlotte"
}
```

