import asyncio
from temporalio.client import Client
from temporalio.envconfig import ClientConfigProfile

async def get_temporal_client() -> Client:
    default_profile = ClientConfigProfile.load()
    print("Loaded profile:", default_profile)
    connect_config = default_profile.to_client_connect_config()

    print("Connect config:", connect_config)

    # Connect to the client using the loaded configuration.
    client = await Client.connect(**connect_config)
    print(f"✅ Client connected to {client.service_client.config.target_host} in namespace '{client.namespace}'")

    return client