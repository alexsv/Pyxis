"""This module provide man functionality to deal with trackers pool.
"""

import gevent

from config.init.trackers import event_dispatcher
from config.init.trackers import sender
from shared.events.Event import NewTrackerAddedEvent, TrackerConfigChangedEvent, \
                                TrackerDeletedEvent, LoggerInfoEvent
from shared.services.services_api import trackers_api


class TrackerCollection:

    """This class is responsible for adding new trackers to the scheduler and
    updating configuration of existing trackers.
    """

    scheduler = None

    def __init__(self, scheduler, storage=None):
        self.scheduler = scheduler
        self.storage = storage

        self._trackers_api = None

    def _config_changes_handler(self, tracker_changed_event):
        """Handle tracker configuration changes.
        """
        tracker = self._trackers_api.get_trackers(
                                tracker_id=tracker_changed_event.tracker_id)[0]
        tracker.set_storage(self.storage)
        self.scheduler.add_tracker(tracker)

    def _tracker_deletion_handler(self, tracker_deleted_event):
        """Handle tracker deletion.
        """
        self.scheduler.remove_tracker(tracker_deleted_event.tracker_id)

    def _tracker_updater(self):
        """Manage trackers queue.
        Add new trackers and update trackers configuration in case when it
        changed.
        """
        event_dispatcher.subscribe(
           [NewTrackerAddedEvent, TrackerConfigChangedEvent],
           self._config_changes_handler)
        event_dispatcher.subscribe([TrackerDeletedEvent],
           self._tracker_deletion_handler)

        gevent.spawn(event_dispatcher.dispatch)

    def _initialize(self):
        """Perform all required initialization.
        """
        self._trackers_api = trackers_api()

    def load_trackers(self):
        """This method is responsible for loading all trackers into scheduler.`
        """
        updated_trackers = \
           self._trackers_api.get_trackers(modified_since=None)

        for tracker in updated_trackers:
            tracker.set_storage(self.storage)
            self.scheduler.add_tracker(tracker)

        sender.fire(LoggerInfoEvent,
                    message='%d trackers loaded.' % (len(updated_trackers,)))



    def start(self):
        """Start main method in separate thread.
        """
        self._initialize()
        self.load_trackers()
        self._tracker_updater()

