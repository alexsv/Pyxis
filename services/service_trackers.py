# Service working with trackers.
# All services are launched automatically by services/services_launcher.py.
#import pgdb
#import config.db as db_config
from services.service_base import SharedService


class TrackersService(SharedService):
    def get_trackers(modified_since=None):
        """Get list of trackers.

        :Parameters:
            - `modified_since`: retrieve only trackers modified since given time.
        """
        # Stub for now.
        return [1,2,3,4,5]
