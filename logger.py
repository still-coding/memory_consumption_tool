import logging

logger = logging.getLogger(__name__)

# set level to logging.WARNING to log sending alarms
logger.setLevel(level=logging.WARNING)
file_handler = logging.FileHandler("mem_cons_tool.log", mode='w')
logger.addHandler(file_handler)
