import stats, crypt
import requests, time, json, logging

device_id = 1
logger = logging.getLogger(__name__)
def post_stats():
  stts = stats.get_stats()
  dat = {'device_id': device_id, 'stats': stts, 'timestamp':time.time()}
  data = crypt.encode_for_server(json.dumps(dat))
  requests.post("http://ds.vnr.is:2425/check_config", data=data)

while True:
  try:
    post_stats()
  except Exception as e:
    logger.info("error connecting to server")
  time.sleep(5)
