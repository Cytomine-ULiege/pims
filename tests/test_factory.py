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

from pims.app import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_env_config(tmp_path, monkeypatch):
    p = tmp_path / "test-config.cfg"
    p.write_text('FILE_ROOT_PATH="/tmp/test"')
    monkeypatch.setenv("PIMS_SETTINGS", str(p))

    assert create_app().config["FILE_ROOT_PATH"] == "/tmp/test"