from typing import Any, Dict

from dotenv import dotenv_values


def get_dotenv_values(path: str = ".env") -> Dict[str, str | None]:
    """Reads the .env file and returns a dictionary of key-value pairs.

    Returns:
        Dict[str, str | None]: A dictionary containing the environment variables defined in the .env file.
    """
    return dotenv_values(path)


def get_dotenv_config(config_key: str, default: Any = None) -> Any:
    """Returns the value of a specific `config_key` from the environment variables file.

    Args:
        config_key (str): Key to be searched in the environment variables file.
        default (Any, optional): Value returned if no `config_key` is found. Defaults to None.

    Returns:
        Any: Value of the `config_key` if present in the environment variables file. Otherwise, the `default` value.
    """
    config = get_dotenv_values()
    return config.get(config_key, default)
