import logging

logging.basicConfig(filename='log.txt', level=logging.INFO)

log = logging.getLogger('ex')

try:
    raise RuntimeError
except RuntimeError:
    log.exception('Error!!!!!!')
h = 'hello'

print(h.encode('utf-8'))