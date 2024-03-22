from dataclasses import dataclass
from typing import Optional, List
from azure.search.documents.indexes.models import _edm as EDM
from azure.search.documents.models import VectorQuery, VectorizedQuery
from teams.ai.embeddings import OpenAIEmbeddings, AzureOpenAIEmbeddings
from teams.state.memory import Memory
from teams.state.state import TurnContext
from teams.ai.tokenizers import Tokenizer

from indexers.data import get_embedding_vector

@dataclass
class Doc:
    docId: Optional[str] = None
    docTitle: Optional[str] = None
    description: Optional[str] = None
    descriptionVector: Optional[List[float]] = None

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
    async def render_data(self):
        pass
    
class Result:
    def __init__(self, output, length, too_long):
        self.output = output
        self.length = length
        self.too_long = too_long

class AzureAISearchDataSource(DataSource):
    def __init__(self, options: AzureAISearchDataSourceOptions):
        self.name = options.name
        self.options = options
        self.searchClient = SearchClient(
            options.azureAISearchEndpoint,
            options.indexName,
            AzureKeyCredential(options.azureAISearchApiKey)
        )

    async def render_data(self, _context: TurnContext, memory: Memory, tokenizer: Tokenizer, maxTokens):
        query = memory.get('temp.input')
        embedding = await get_embedding_vector(query)
        vector_query = VectorizedQuery(vector=embedding, k_nearest_neighbors=2, fields="descriptionVector")
            
        print(query)

        if not query:
            return {'output': '', 'length': 0, 'tooLong': False}

        selectedFields = [
            'docTitle',
            'description',
            'descriptionVector',
        ]

        searchResults = self.searchClient.search(
            search_text=query,
            select=selectedFields,
            vector_queries=[vector_query],
        )

        if not searchResults:
            return Result('', 0, False)

        usedTokens = 0
        doc = ''
        for result in searchResults:
            tokens = len(tokenizer.encode(json.dumps(result["description"])))

            if usedTokens + tokens > maxTokens:
                break

            doc += json.dumps(result["description"])
            usedTokens += tokens

        return Result(doc, usedTokens, usedTokens > maxTokens)