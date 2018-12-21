import logging

DOMAIN = 'templights'

_LOGGER = logging.getLogger(__name__)


def setup(hass, config):
    def handle_update(call):
        temp = float(hass.states.get('sensor.agh_meteo').state)

        blue = [0, 0, 255]
        red = [255, 0, 0]
        color = blue if temp < 0 else red

        bounded = max(-10., min(temp, 10.))

        white = round(-(abs(bounded)) * 51 + 255)

        _LOGGER.debug('Temperature: %f, new color: %s, white: %d', temp, str(color), white)

        hass.services.call('light', 'turn_on', {'rgb_color': color, 'white_value': white}, False)

    hass.services.register('templights', 'update', handle_update)

    return True
