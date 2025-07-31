from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# ✅ Define Key Vault name
KEY_VAULT_NAME = "kv-ncpl-dev"
KEY_VAULT_URL = f"https://{KEY_VAULT_NAME}.vault.azure.net/"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

def get_secret(secret_name: str) -> str:
    secret = client.get_secret(secret_name)
    return secret.value
