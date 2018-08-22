from device import Device
from stats import Stats

import requests, time, json, logging

logger = logging.getLogger(__name__)

my_device = Device()

# Stats Thread to constantly poll /proc and get up to date stats
stats = Stats()
stats.start()

def post_stats():
  current_stats = stats.get_stats()
  data = my_device.encodeAsDevice(current_stats)
  print(data)
  # requests.post("http://ds.vnr.is:2425/check_config", data=data)

while True:
  try:
    post_stats()
  except Exception as e:
    logger.info("Error connecting to server: {0}\n waiting 5 seconds".format(e))
  time.sleep(5)
