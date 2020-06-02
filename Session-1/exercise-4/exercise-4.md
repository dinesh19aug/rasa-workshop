## Execise: Explore existing pipeline

### Steps:
- run "rasa shell"
- Check confidence value of the following
```
hi
Find me a doctor
Find me a nursing home
Find me a nurse
Find me a doctor's office
```

- Open the config.yml file. Notice that the default settings for pipeline are set to supervised.
```
language: en
pipeline:
  - name: WhitespaceTokenizer
  - name: RegexFeaturizer
  - name: LexicalSyntacticFeaturizer
  - name: CountVectorsFeaturizer
  - name: CountVectorsFeaturizer
    analyzer: "char_wb"
    min_ngram: 1
    max_ngram: 4
  - name: DIETClassifier
    epochs: 100
  - name: EntitySynonymMapper
  - name: ResponseSelector
    epochs: 100
```

- Change the max_ngram to 1
- retrain
```
rasa train nlu
```

- run "rasa shell"
- Check confidence value of the following
```
hi
Find me a doctor
Find me a nursing home
Find me a nurse
Find me a doctor's office
```

## Switch pipeline to following
- Comment out the old pipeline and new one
```
#pipeline:
#  - name: WhitespaceTokenizer
#  - name: RegexFeaturizer
#  - name: LexicalSyntacticFeaturizer
#  - name: CountVectorsFeaturizer
#  - name: CountVectorsFeaturizer
#    analyzer: "char_wb"
#    min_ngram: 1
#    max_ngram: 4
#  - name: DIETClassifier
#    epochs: 100
#  - name: EntitySynonymMapper
#  - name: ResponseSelector
#    epochs: 100
pipeline:
  - name: SpacyNLP
  - name: SpacyTokenizer
  - name: SpacyFeaturizer
  - name: RegexFeaturizer
  - name: CRFEntityExtractor
  - name: EntitySynonymMapper
  - name: SklearnIntentClassifier

```
- You might get error about spacy not installed.
- run the following one after the other
> If using pip
```
pip install -U spacy

python -m spacy download en_core_web_md

python -m spacy link en_core_web_md en
```
> If using conda
```
conda install -c conda-forge spacy

python -m spacy download en_core_web_md

python -m spacy link en_core_web_md en

```

- Now re train 
```
rasa train nlu
```
- Test
```
rasa shell
```

- Check confidence value of the following
```
hi
Find me a doctor
Find me a nursing home
Find me a nurse
Find me a doctor's office
```

## Food for thought
- Does punctuations matter
- Does punctuations affect the model
- What about class bias? Ex - If I add 10 samples like "Find me a doctor", "Find me a nursing home"," Find me a ..." and so on. What would happen if add a new intent called
intent:find_restaurant
- find me a mexican restaurant


