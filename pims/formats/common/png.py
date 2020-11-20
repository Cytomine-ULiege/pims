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
from pims.formats import AbstractFormat
from pims.formats.utils.metadata import ImageMetadata


class PNGFormat(AbstractFormat):
    def init_standard_metadata(self):
        self._image_metadata = ImageMetadata()

    def init_complete_metadata(self):
        pass

    @classmethod
    def match(cls, proxypath):
        buf = proxypath.get("signature", proxypath.path.signature)
        return (len(buf) > 3 and
                buf[0] == 0x89 and
                buf[1] == 0x50 and
                buf[2] == 0x4E and
                buf[3] == 0x47)