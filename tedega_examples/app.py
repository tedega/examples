#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tedega_view import (
    start_server,
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
    with get_storage() as storage:

        factory = Ping.get_factory(storage)
        item = factory.create()
        storage.create(item)

        items = storage.read(Ping)
        data["total"] = len(items)
        data["data"] = [item.get_values() for item in items]
    return data

if __name__ == "__main__":
    init_storage()
    start_server("tedega_examples")
