import os
from temporalio.client import Client, TLSConfig
from temporalio.envconfig import ClientConfig


async def get_temporal_client() -> Client:
    config_file_path = os.getenv("TEMPORAL_CONFIG_PATH")
    profile_name = os.getenv("TEMPORAL_PROFILE_NAME")
    if config_file_path and profile_name:
        # DO PROFILE THING
        connect_config = ClientConfig.load_client_connect_config(
            profile=profile_name,
            config_file=config_file_path,
        )
        return await Client.connect(**connect_config)
    else:
        return await Client.connect(
            os.getenv("TEMPORAL_ADDRESS", "localhost:7233"),
            namespace=os.getenv("TEMPORAL_NAMESPACE", "default"),
        )
