import os
from temporalio.client import Client, TLSConfig

async def get_temporal_client() -> Client:
    cert_path = os.getenv("TEMPORAL_TLS_CERT")
    key_path = os.getenv("TEMPORAL_TLS_KEY")
    api_key = os.getenv("TEMPORAL_API_KEY")

    # Check for mTLS authentication
    if cert_path and key_path:
        with open(cert_path, "rb") as f:
            client_cert = f.read()
        with open(key_path, "rb") as f:
            client_key = f.read()

        return await Client.connect(
            os.getenv("TEMPORAL_ADDRESS"),
            namespace=os.getenv("TEMPORAL_NAMESPACE"),
            tls=TLSConfig(
                client_cert=client_cert,
                client_private_key=client_key,
            ),
        )
    elif api_key:
        return await Client.connect(
            os.getenv("TEMPORAL_ADDRESS"),
            namespace=os.getenv("TEMPORAL_NAMESPACE"),
            api_key=api_key,
            tls=True,
        )

    else:
        return await Client.connect(
            os.getenv("TEMPORAL_ADDRESS", "localhost:7233"),
            namespace=os.getenv("TEMPORAL_NAMESPACE", "default"),
        )
