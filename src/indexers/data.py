from dataclasses import dataclass
from typing import Optional, List, Any
from teams.ai.embeddings import AzureOpenAIEmbeddings  # Replace with the actual module

@dataclass
class Address:
    streetAddress: Optional[str] = None
    city: Optional[str] = None
    stateProvince: Optional[str] = None
    postalCode: Optional[str] = None
    country: Optional[str] = None

@dataclass
class Restaurant:
    restaurantId: Optional[str] = None
    restaurantName: Optional[str] = None
    description: Optional[str] = None
    descriptionVectorEn: Optional[List[float]] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    rating: Optional[float] = None
    location: Optional[Any] = None  # Replace Any with the actual type
    address: Optional[Address] = None

async def get_restaurant_data():
    chick_fila_a_description = 'Chick-fil-A, Inc. is an American fast food restaurant chain and the largest chain specializing in chicken sandwiches. Headquartered in College Park, Georgia, Chick-fil-A operates 3,059 restaurants across 48 states, as well as in the District of Columbia and Puerto Rico. The company also has operations in Canada, and previously had restaurants in the United Kingdom and South Africa. The restaurant has a breakfast menu, and a lunch and dinner menu. The chain also provides catering services.'
    chic_fil_a = Restaurant(
        restaurantId='1',
        restaurantName='Chick-fil-A',
        description=chick_fila_a_description,
        descriptionVectorEn=await get_embedding_vector(chick_fila_a_description),
        category='Fast Food',
        tags=['fast food', 'burgers', 'fries', 'shakes'],
        rating=4.5,
        location={'longitude': -122.131577, 'latitude': 47.678581},  # Replace with the actual type
        address=Address(
            streetAddress='123 Main St',
            city='Seattle',
            stateProvince='WA',
            postalCode='98101',
            country='USA'
        )
    )

    starbucks_description = 'Starbucks is an American company that operates the largest coffeehouse chain and one of the most recognizable brands in the world. Headquartered in Seattle, Washington, the company operates more than 35,000 stores across 80 countries (as of 2022).'
    starbucks = Restaurant(
        restaurantId='2',
        restaurantName='Starbucks',
        description=starbucks_description,
        descriptionVectorEn=await get_embedding_vector(starbucks_description),
        category='Coffee house',
        tags=['coffee', 'drinks', 'global', 'shakes', 'cafe', 'tea'],
        rating=4.5,
        location={'longitude': -122.131577, 'latitude': 47.678581},  # Replace with the actual type
        address=Address(
            streetAddress='123 Main St',
            city='Seattle',
            stateProvince='WA',
            postalCode='98101',
            country='USA'
        )
    )

    return [chic_fil_a, starbucks]

import os

async def get_embedding_vector(text: str):
    embeddings = AzureOpenAIEmbeddings({
        'azureApiKey': os.getenv('AZURE_OPENAI_KEY'),
        'azureEndpoint': os.getenv('AZURE_OPENAI_ENDPOINT'),
        'azureDeployment': 'text-embedding-ada-002-zihch'
    })

    result = await embeddings.create_embeddings('text-embedding-ada-002-zihch', text)
    if result.status != 'success' or not result.output:
        raise Exception(f"Failed to generate embeddings for description: {text}")

    return result.output[0]
