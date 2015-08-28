import logging
import logging.handlers
import sys

BYTES_IN_MB = 1048576
FIVE_MB = 5*BYTES_IN_MB

root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stderr)
ch.setLevel(logging.DEBUG)
fh = logging.handlers.RotatingFileHandler("registre.log", maxBytes=FIVE_MB)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
root.addHandler(ch)
