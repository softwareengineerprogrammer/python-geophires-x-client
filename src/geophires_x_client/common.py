import logging
import sys

sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.INFO)
sh.setFormatter(logging.Formatter(fmt='[%(asctime)s][%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))

log = logging.getLogger('geophires-x-client')
log.addHandler(sh)
