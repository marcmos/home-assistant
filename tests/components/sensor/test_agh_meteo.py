from pytest import approx

from homeassistant.components import sensor
from homeassistant.components.sensor.agh_meteo import API_URL
from homeassistant.setup import setup_component
from tests.common import (get_test_home_assistant, load_fixture)


class TestAGHMeteo:
    def setup_method(self):
        self.hass = get_test_home_assistant()

    def teardown_method(self):
        self.hass.stop()

    def test_setup(self, aioclient_mock):
        aioclient_mock.get(API_URL, text=load_fixture('agh_meteo.xml'))
        assert setup_component(self.hass, sensor.DOMAIN, {
            'sensor': {
                'platform': 'agh_meteo',
            }
        })
        state = self.hass.states.get('sensor.agh_meteo')

        assert state is not None

        temperature = state.state
        assert temperature == '-0.7'
