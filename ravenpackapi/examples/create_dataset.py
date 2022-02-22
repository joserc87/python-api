from ravenpackapi import RPApi, Dataset

product = "rpa"  # or "edge"

# Product specific fields:
if product == "rpa":
    RP_STORY_ID = "rp_story_id"
    ENTITY_RELEVANCE = "relevance"
    EVENT_SENTIMENT = "event_sentiment_score"
    TITLE = "headline"
    ENTITY_SENTIMENT = None  # field does not exist in RPA
else:
    RP_STORY_ID = "rp_document_id"
    ENTITY_RELEVANCE = "entity_relevance"
    EVENT_SENTIMENT = "event_sentiment"
    TITLE = "title"
    ENTITY_SENTIMENT = "entity_sentiment"


api = RPApi(api_key="YOUR_API_KEY", product=product)

fields = [
    "timestamp_utc",
    RP_STORY_ID,
    "rp_entity_id",
    "entity_type",
    "entity_name",
    "country_code",
    ENTITY_RELEVANCE,
    ENTITY_SENTIMENT,
    EVENT_SENTIMENT,
    "topic",
    "group",
    TITLE,
]
# Note that edge has some extra fields
fields = [f for f in fields if f]

ds = api.create_dataset(
    Dataset(
        **{
            "product": product,
            "product_version": "1.0",
            "name": "Events in UK - example",
            "fields": fields,
            "filters": {
                "$and": [
                    {
                        ENTITY_RELEVANCE: {
                            "$gte": 90
                        }
                    },
                    {
                        "country_code": {
                            "$in": [
                                "GB"
                            ]
                        }
                    },
                    {
                        EVENT_SENTIMENT: {
                            "$nbetween": [-0.5, 0.5]
                        }
                    }
                ]
            },
            "frequency": "granular",
        }
    )
)

print("Dataset created", ds)
