import os
import asyncio

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient

from .utils import create_index_if_not_exists, upsert_documents 
from AzureAISearchDataSource import Restaurant
from .data import get_restaurant_data
from config import Config

async def setup():
    index = 'restaurants'

    search_api_key = Config.AZURE_SEARCH_KEY
    search_api_endpoint = Config.AZURE_SEARCH_ENDPOINT
    credentials = AzureKeyCredential(search_api_key)

    search_index_client = SearchIndexClient(search_api_endpoint, credentials)
    await create_index_if_not_exists(search_index_client, index)
    await asyncio.sleep(5)

    search_client = SearchClient(search_api_endpoint, index, credentials)

    data = await get_restaurant_data()
    await upsert_documents(search_client, data)
