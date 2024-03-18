from dataclasses import dataclass
from typing import Optional, List
from azure.search.documents.indexes.models import _edm as EDM
from teams.ai.embeddings import OpenAIEmbeddings, AzureOpenAIEmbeddings
from teams.state.memory import Memory
from teams.state.state import TurnContext
from teams.ai.tokenizers import Tokenizer
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
    location: Optional[EDM.GeographyPoint] = None  # Replace 'GeographyPoint' with the actual type
    address: Optional[Address] = None

@dataclass
class AzureAISearchDataSourceOptions:
    name: str
    indexName: str
    azureOpenAIApiKey: str
    azureOpenAIEndpoint: str
    azureOpenAIEmbeddingDeployment: str
    azureAISearchApiKey: str
    azureAISearchEndpoint: str

from abc import ABC, abstractmethod
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
import json

class DataSource(ABC):
    @abstractmethod
    async def renderData(self):
        pass

class AzureAISearchDataSource(DataSource):
    def __init__(self, options: AzureAISearchDataSourceOptions):
        self.name = options.name
        self.options = options
        self.searchClient = SearchClient(
            options.azureAISearchEndpoint,
            options.indexName,
            AzureKeyCredential(options.azureAISearchApiKey)
        )

    async def renderData(self, _context: TurnContext, memory: Memory, tokenizer: Tokenizer, maxTokens):
        query = memory.get('temp.input')

        if not query:
            return {'output': '', 'length': 0, 'tooLong': False}

        selectedFields = [
            'restaurantId',
            'restaurantName',
            'description',
            'category',
            'tags',
            'rating',
            'location',
            'address'
        ]

        searchResults = await self.searchClient.search(query, {
            'searchFields': ['category', 'tags', 'restaurantName'],
            'select': selectedFields
        })

        if not searchResults.results:
            return {'output': '', 'length': 0, 'tooLong': False}

        usedTokens = 0
        doc = ''
        for result in searchResults.results:
            formattedResult = self.formatDocument(result.document)
            tokens = len(tokenizer.encode(formattedResult))

            if usedTokens + tokens > maxTokens:
                break

            doc += formattedResult
            usedTokens += tokens

        return {'output': doc, 'length': usedTokens, 'tooLong': usedTokens > maxTokens}

    def formatDocument(self, result: Restaurant):
        return f"<context>{json.dumps(result)}</context>"

    async def getEmbeddingVector(self, text: str):
        embeddings = AzureOpenAIEmbeddings({
            'azureApiKey': self.options.azureOpenAIApiKey,
            'azureEndpoint': self.options.azureOpenAIEndpoint,
            'azureDeployment': self.options.azureOpenAIEmbeddingDeployment
        })

        result = await embeddings.create_embeddings(self.options.azureOpenAIEmbeddingDeployment, text)
        if result.status != 'success' or not result.output:
            raise Exception(f"Failed to generate embeddings for description: {text}")

        return result.output[0]