import asyncio
import requests

from datetime import datetime
from socket import gethostname

from .config import settings
from .logger import logger

# TODO: maybe should do something about API throttling 

class Alarmist:

    def __init__(self):
        self.authenticate()

    
    def __send_post_request(self, url: str, payload: dict) -> None:
        try:
            r = requests.post(url, json=payload)
            r.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            logger.error(f"Sending request - Http Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            logger.error(f"Sending request - Connection Error: {errc}")
        except requests.exceptions.Timeout as errt:
            logger.error(f"Sending request - Timeout Error: {errt}")
        except requests.exceptions.RequestException as excr:
            logger.error(f"Sending request - Oops, something else: {excr}")


    async def send_alarm(self, timestamp: datetime, message: str, value: int) -> None:
        alarm_data = {
            "timestamp": timestamp,
            "host": gethostname(),
            "message": message,
            "value": value,
        }
        return await asyncio.to_thread(self.__send_post_request, settings.api_url, alarm_data)
        


    # TODO: maybe auth functionality will be needed
    def authenticate(self) -> None:
        pass
