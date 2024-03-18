import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient

def delete_index(client: SearchIndexClient, name: str):
    client.delete_index(name)

index = 'restaurants'
search_api_key = os.getenv('AZURE_SEARCH_KEY')
search_api_endpoint = os.getenv('AZURE_SEARCH_ENDPOINT')
credentials = AzureKeyCredential(search_api_key)

search_index_client = SearchIndexClient(search_api_endpoint, credentials)
delete_index(search_index_client, index)