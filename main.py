from device import Device
from stats import Stats

import requests, time, json, logging

logger = logging.getLogger(__name__)

my_device = Device()
stats = Stats()
def post_stats():
  current_stats = stats.get_current_stats()
  data = my_device.encodeAsDevice(current_stats)
  requests.post("http://ds.vnr.is:2425/check_config", data=data)

while True:
  try:
    post_stats()
  except Exception as e:
    logger.info("Error connecting to server: {0}\n waitng 5 seconds".format(e))
  time.sleep(5)
