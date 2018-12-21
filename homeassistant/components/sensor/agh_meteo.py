import logging
from datetime import timedelta

import xmltodict

from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

REQUIREMENTS = ['xmltodict==0.11.0']

_LOGGER = logging.getLogger(__name__)

API_URL = 'http://meteo2.ftj.agh.edu.pl/meteo/meteo.xml'


async def async_setup_platform(hass, config, async_add_entities,
                               discovery_info=None):
    entity = AGHMeteoSensor(API_URL, hass)
    await entity.async_update()
    async_add_entities([entity])


class AGHMeteoSensor(Entity):
    @property
    def name(self):
        return 'agh_meteo'

    @property
    def unit_of_measurement(self):
        return TEMP_CELSIUS

    @property
    def state(self) -> str:
        return str(self._temperature)

    def __init__(self, url, hass):
        self._url = url
        self._hass = hass
        self._temperature = None

    @Throttle(timedelta(minutes=5))
    async def async_update(self) -> None:
        response = await self.async_fetch_state()
        if response is None:
            return
        data = xmltodict.parse(await response.text())
        self._temperature = float(data['meteo']['dane_aktualne']['ta'].split()[0])

    async def async_fetch_state(self):
        _LOGGER.debug('Fetching data...')
        session = async_get_clientsession(self._hass)
        response = await session.get(self._url)
        return response
