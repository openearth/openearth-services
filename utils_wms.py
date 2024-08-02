# -*- coding: utf-8 -*-
# Copyright notice
#   --------------------------------------------------------------------
#   Copyright (C) 2024 Deltares
#       Gerrit Hendriksen (gerrit.hendriksen@deltares.nl)
#       Ioanna Micha (Ioanna Micha)
#
#   This library is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This library is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this library.  If not, see <http://www.gnu.org/licenses/>.
#   --------------------------------------------------------------------
#
# This tool is part of <a href="http://www.OpenEarth.eu">OpenEarthTools</a>.
# OpenEarthTools is an online collaboration to share and manage data and
# programming tools in an open source, version controlled environment.
# Sign up to recieve regular updates of this function, and to contribute
# your own tools.

from owslib.wms import WebMapService
from owslib.util import ServiceException


def checkwfsfeature(wms, layer, layernameprinting=False):
    if layernameprinting:
        print(f"testing {layer}")
    lbbox = wms.contents[layer].boundingBox[0:4]
    lcrs = wms.contents[layer].boundingBox[-1]

    try:
        response = wms.getfeatureinfo(
            layers=[layer],
            srs=lcrs,
            bbox=lbbox,
            size=(10, 10),
            format="image/jpeg",
            query_layers=[layer],
            info_format="text/html",
            xy=(5, 5),
        )

        jf = response.read()
        if "ServiceException code" in str(jf):
            print("getfeaturinfo failed for ", layer)
    except TimeoutError as e:
        print(f"WMS server timed out for layer {layer} {e}")
    except ServiceException as e:
        print(f"WMS server error for layer {layer} {e}")


def checkgetmap(wms, layer):
    lbbox = wms.contents[layer].boundingBox[0:4]
    lcrs = wms.contents[layer].boundingBox[-1]

    try:
        response = wms.getmap(
            layers=[layer],
            srs=lcrs,
            bbox=lbbox,
            size=(10, 10),
            format="image/jpeg",
        )

        jf = response.read()
        if "ServiceException code" in str(jf):
            print("getfeaturinfo failed for ", layer)
    except TimeoutError as e:
        print(f"WMS timed out for layer {layer} {e}")
    except ServiceException as e:
        print(f"WMS error for layer {layer} {e}")
    except Exception as e:
        print(f"General exception for layer {layer} {e}")


def connecttowms(url):
    try:
        wms = WebMapService(url, version="1.3.0", timeout=180)
        layers = wms.contents
        print("connection succesful")
        return wms, layers
    except ServiceException as e:
        assert f"WMS server error for {url} {e}"


def __main__():
    urls = [
        "https://rwsprojectarchief.openearth.nl/geoserver/ows",
        "https://marineprojects.openearth.nl/geoserver/ows",
        "https://datahuiswadden.openearth.nl/geoserver/ows",
        "https://coastalhazardwheel.avi.deltares.nl/geoserver/ows",
        "https://deltaresdata.openearth.eu/geoserver/ows",
    ]
    url = urls[4]

    print(f"exploring {url}")
    wms, layers = connecttowms(url)

    for layer in layers:
        # checklayer(wms, layer)
        checkgetmap(wms, layer)
