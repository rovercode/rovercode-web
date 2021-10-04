"""Logging handlers."""
import json
import logging
import requests


class SumoHandler(logging.Handler):
    """Handler to send to sumologic."""

    def __init__(self, host, url, level=logging.NOTSET):
        """Create handler."""
        super().__init__(level)

        self.host = host
        self.url = url

    def emit(self, record):
        """Send to sumologic."""
        try:
            requests.post(
                f'https://{self.host}{self.url}',
                json=json.loads(record.getMessage())
            )
        except Exception:  # pylint: disable=broad-except
            self.handleError(record)
