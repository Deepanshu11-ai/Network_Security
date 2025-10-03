import sys
import logging
from types import ModuleType
from pathlib import Path
from logging.handlers import RotatingFileHandler

# setup file logging
_log_dir = Path(__file__).parent.parent / "logs"
_log_dir.mkdir(parents=True, exist_ok=True)
_log_file = _log_dir / "network_security.log"

_handler = RotatingFileHandler(str(_log_file), maxBytes=5_000_000, backupCount=3)
_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

logger = logging.getLogger("networksecurity")
logger.setLevel(logging.INFO)
if not logger.handlers:
    logger.addHandler(_handler)

class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_detail: ModuleType = sys):
        super().__init__(error_message)
        self.error_message = error_message

        _, _, exc_tb = error_detail.exc_info()
        if exc_tb is not None:
            self.lineno = exc_tb.tb_lineno
            self.file_name = exc_tb.tb_frame.f_code.co_filename
        else:
            self.lineno = None
            self.file_name = None

        # log the error to the file (include traceback)
        msg = ("error occurred in python script name [{0}] at line number [{1}] "
               "error message [{2}]").format(self.file_name, self.lineno, str(self.error_message))
        logger.error(msg, exc_info=error_detail.exc_info())

    def __str__(self):
        return ("error occurred in python script name [{0}] at line number [{1}] "
                "error message [{2}]").format(self.file_name, self.lineno, str(self.error_message))

if __name__ == "__main__":
    try:
        logging.info("about to divide by zero")
        a = 1 / 0
    except Exception as e:
        raise NetworkSecurityException(e, sys)