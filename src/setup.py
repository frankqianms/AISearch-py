import os
import asyncio

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient

from indexers.utils import create_index_if_not_exists, upsert_documents
from indexers.data import get_doc_data
from config import Config

async def setup():
    index = 'contoso-electronics'

    search_api_key = Config.AZURE_SEARCH_KEY
    search_api_endpoint = Config.AZURE_SEARCH_ENDPOINT
    credentials = AzureKeyCredential(search_api_key)

    search_index_client = SearchIndexClient(search_api_endpoint, credentials)
    await create_index_if_not_exists(search_index_client, index)
    
    print("Create index succeeded. If it did not exist, waiting for 5 seconds...")
    await asyncio.sleep(5)

    search_client = SearchClient(search_api_endpoint, index, credentials)

    data = await get_doc_data()
    await upsert_documents(search_client, data)

    print("Upload of new document succeeded")
    
asyncio.run(setup())
print("setup finished")

