from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SimpleField, ComplexField, ScoringProfile, DistanceScoringParameters, DistanceScoringFunction, CorsOptions
from time import sleep

from AzureAISearchDataSource import Restaurant

WAIT_TIME = 4000

def document_key_retriever(document: Restaurant):
    return document.restaurantId

def delay(time_in_ms: int):
    sleep(time_in_ms / 1000)

def delete_index(client: SearchIndexClient, name: str):
    client.delete_index(name)

async def upsert_documents(client: SearchClient, documents: list[Restaurant]):
    return await client.merge_or_upload_documents(documents)

async def create_index_if_not_exists(client: SearchIndexClient, name: str):
    restaurant_index = SearchIndex(
        name=name,
        fields=[
            SimpleField(name="restaurantId", type="Edm.String", key=True, filterable=True, sortable=True),
            SimpleField(name="restaurantName", type="Edm.String", searchable=True, filterable=True, sortable=True),
            SimpleField(name="description", type="Edm.String", searchable=True, analyzer_name="standard.lucene"),
            SimpleField(name="descriptionVectorEn", type="Collection(Edm.Single)", searchable=True, dimensions=1536, vectorSearchConfiguration="description_vector_config"),
            SimpleField(name="category", type="Edm.String", searchable=True, filterable=True, sortable=True, facetable=True),
            SimpleField(name="tags", type="Collection(Edm.String)", searchable=True, filterable=True, facetable=True),
            SimpleField(name="parkingIncluded", type="Edm.Boolean", filterable=True, sortable=True, facetable=True),
            SimpleField(name="smokingAllowed", type="Edm.Boolean", filterable=True, sortable=True, facetable=True),
            SimpleField(name="lastRenovationDate", type="Edm.DateTimeOffset", filterable=True, sortable=True, facetable=True),
            SimpleField(name="rating", type="Edm.Double", filterable=True, sortable=True, facetable=True),
            SimpleField(name="location", type="Edm.GeographyPoint", filterable=True, sortable=True),
            ComplexField(name="address", fields=[
                SimpleField(name="streetAddress", type="Edm.String", searchable=True),
                SimpleField(name="city", type="Edm.String", searchable=True, filterable=True, sortable=True, facetable=True),
                SimpleField(name="stateProvince", type="Edm.String", searchable=True, filterable=True, sortable=True, facetable=True),
                SimpleField(name="country", type="Edm.String", searchable=True, filterable=True, sortable=True, facetable=True),
                SimpleField(name="postalCode", type="Edm.String", searchable=True, filterable=True, sortable=True, facetable=True)
            ])
        ],
        suggesters=[
            {
                "name": "sg",
                "sourceFields": ["description", "restaurantName"],
                "searchMode": "analyzingInfixMatching"
            }
        ],
        scoring_profiles=[
            ScoringProfile(
                name="nearest",
                function_aggregation="sum",
                functions=[
                    DistanceScoringFunction(
                        field_name="location",
                        boost=2,
                        parameters=DistanceScoringParameters(
                            reference_point_parameter="myloc",
                            boosting_distance=100
                        )
                    )
                ]
            )
        ],
        cors_options=CorsOptions(allowed_origins=["*"])
    )

    await client.create_or_update_index(restaurant_index)
