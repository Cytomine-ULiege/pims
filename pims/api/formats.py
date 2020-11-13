# * Copyright (c) 2020. Authors: see NOTICE file.
# *
# * Licensed under the Apache License, Version 2.0 (the "License");
# * you may not use this file except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *      http://www.apache.org/licenses/LICENSE-2.0
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.

from pims.api.exceptions import FormatNotFoundProblem
from pims.api.utils.response import response_list
from pims.formats import FORMATS


def _serialize_format(format):
    return {
        "id": format.get_identifier(),
        "name": format.get_name(),
        "remarks": format.get_remarks(),
        "readable": format.is_readable(),
        "writable": format.is_writable(),
        "convertible": format.is_convertible(),
        "plugin": format.get_plugin_name()
    }


def list_formats():
    formats = [_serialize_format(format) for format in FORMATS.values()]
    return response_list(formats)


def show_format(format_id):
    format_id = format_id.upper()
    if format_id not in FORMATS.keys():
        raise FormatNotFoundProblem(format_id)
    return _serialize_format(FORMATS[format_id])