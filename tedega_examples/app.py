#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tedega_share import (
    init_logger,
    get_logger,
    monitor_connectivity,
    monitor_system
)

from tedega_view import (
    create_application,
    config_view_endpoint
)

from tedega_storage.rdbms import (
    BaseItem,
    RDBMSStorageBase,
    init_storage,
    get_storage
)

########################################################################
#                                Model                                 #
########################################################################


class Ping(BaseItem, RDBMSStorageBase):
    __tablename__ = "pings"


########################################################################
#                              Controller                              #
########################################################################


@config_view_endpoint(path="/pings", method="GET", auth=None)
def ping():
    data = {}
    log = get_logger()
    with get_storage() as storage:

        factory = Ping.get_factory(storage)
        item = factory.create()
        storage.create(item)

        items = storage.read(Ping)
        data["total"] = len(items)
        data["data"] = [item.get_values() for item in items]
        log.info("Let's log something")
    return data


def build_app(servicename):
    # Define things we want to happen of application creation. We want:
    # 1. Initialise the fluent logger.
    # 2. Initialise the storage.
    # 3. Start the monitoring the connectivity of the service to "google".
    # 4. Start the monitoring the system's load every 10sec (CPU, RAM, DISK).
    run_on_init = [(init_logger, servicename),
                   (init_storage, None),
                   (monitor_connectivity, [("www.google.com", 80)]),
                   (monitor_system, 10)]
    application = create_application(servicename, run_on_init=run_on_init)
    return application

if __name__ == "__main__":
    application = build_app("tedega_examples")
    application.run()
