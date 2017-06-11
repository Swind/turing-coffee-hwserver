from utils.logger import get_logger

logger = get_logger(__name__)

class GPIO:
    OUT = "out"
    IN = "in"

    BOARD = "board"

    def setmode(self, mode):
        logger.info("GPIO setmode to {}".format(mode))

    def output(self, pin_number, mode):
        logger.info("GPIO output {} to {}".format(mode, pin_number))


