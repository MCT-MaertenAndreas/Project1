from threading import Thread
import sys

from ..repo.database import Database
from ..rest.routing import Routing
from ..util.users import UserUtils
from ...config import db_config

from ..util.logger import log


class RestManager(Thread):
    def __init__(self, debug = False):
        Thread.__init__(self)

        # Make sure the Thread shuts down if the main process exits
        # Since this thread doesn't need cleanup we can just kill it
        self.daemon = True

        self.routing = Routing(self, debug)
        self.db = Database(db_config, debug)

        self.user_utils = UserUtils(self.db)

    def run(self):
        log.info('REST', 'Started')

        self.routing.start()

    def kill(self):
        sys.exit()
