from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Use your vault URL here
KEY_VAULT_URL = "https://kv-ncpl-dev.vault.azure.net/"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

def get_secret(secret_name: str) -> str:
    secret = client.get_secret(secret_name)
    return secret.value
