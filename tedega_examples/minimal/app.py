#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import tedega_examples
from tedega_storage import init_storage
from tedega_view import (
        start_server,
        config_view_endpoint
)

########################################################################
#                                Model                                 #
########################################################################


########################################################################
#                              Controller                              #
########################################################################

@config_view_endpoint(path="/ping", method="GET", auth=None)
def ping():
    return {"data": "Pong"}


if __name__ == "__main__":
    # Init the storage.
    init_storage()

    # Build path from where the view can load the API configuration.
    package_directory = os.path.dirname(os.path.abspath(__file__))
    swagger = os.path.abspath(os.path.join(package_directory, "swagger.yaml"))

    # Start the serving the view with the given swagger config. Also
    # provide the current modul as modul to be scanned for configured
    # view endpoints.
    start_server(swagger_config=swagger, modul=tedega_examples)
