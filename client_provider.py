from temporalio.client import Client
from temporalio.envconfig import ClientConfig


async def get_temporal_client() -> Client:
    config = ClientConfig.load_client_connect_config()
    config["target_host"] = config.get("target_host") or "localhost:7233"
    config["namespace"] = config.get("namespace") or "default"
    return await Client.connect(**config)
