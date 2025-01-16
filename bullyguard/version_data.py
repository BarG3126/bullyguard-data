from pathlib import Path
from bullyguard.config_schemas.config_schema import Config
from bullyguard.utils.config_utils import get_config
from bullyguard.utils.data_utils import initialize_dvc
from bullyguard.utils.utils import get_logger


@get_config(config_path="../configs", config_name="config")
def version_data(config: Config) -> None:
    initialize_dvc()


if __name__ == "__main__":
    version_data()  # type: ignore
