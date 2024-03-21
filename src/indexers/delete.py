import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient

from config import Config

def delete_index(client: SearchIndexClient, name: str):
    client.delete_index(name)

index = 'contoso-electronics'
search_api_key = Config.AZURE_SEARCH_KEY
search_api_endpoint = Config.AZURE_SEARCH_ENDPOINT
credentials = AzureKeyCredential(search_api_key)

search_index_client = SearchIndexClient(search_api_endpoint, credentials)
delete_index(search_index_client, index)