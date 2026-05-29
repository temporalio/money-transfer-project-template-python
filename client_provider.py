import os
import pathlib
import platform
from temporalio.client import Client, TLSConfig
from temporalio.envconfig import ClientConfig


# Configures and returns a Temporal Client. This uses the default
# settings, unless the TEMPORAL_PROFILE environment variable is set,
# in which case it configures it as per the specified profile name.
async def get_temporal_client() -> Client:
    config_file_path = get_config_file_path()
    profile_name = os.getenv("TEMPORAL_PROFILE")
    if profile_name and config_file_path.is_file():
        connect_config = ClientConfig.load_client_connect_config(
            profile=profile_name,
            config_file=str(config_file_path),
        )
        return await Client.connect(**connect_config)
    else:
        return await Client.connect(
            os.getenv("TEMPORAL_ADDRESS", "localhost:7233"),
            namespace=os.getenv("TEMPORAL_NAMESPACE", "default"),
        )


# Returns the path representing the default location of the
# configuration file, based on the current operating system.
def get_config_file_path() -> pathlib.Path:
    home = pathlib.Path.home()
    system = platform.system()

    if system == "Darwin":
        config_file_path = home / "Library/Application Support/temporalio/temporal.toml"
    elif system == "Windows":
        app_data = os.getenv("AppData")
        if app_data is None:
            raise RuntimeError("AppData environment variable not set")
        config_file_path = pathlib.Path(app_data) / "temporalio/temporal.toml"
    else:
        xdg_config_home = os.getenv("XDG_CONFIG_HOME")
        if xdg_config_home:
            config_file_path = (
                pathlib.Path(xdg_config_home) / "temporalio/temporal.toml"
            )
        else:
            config_file_path = home / ".config/temporalio/temporal.toml"

    return config_file_path
