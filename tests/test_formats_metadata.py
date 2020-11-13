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

import json

import pytest

from pims.formats.utils.metadata import Metadata, MetadataType, MetadataStore, boolean_parser, json_parser, \
    ImageMetadata, ImageChannel


def test_boolean_parser():
    assert boolean_parser(True) is True
    assert boolean_parser(False) is False
    assert boolean_parser("truE") is True
    assert boolean_parser("YeS") is True
    assert boolean_parser("nO") is False

    with pytest.raises(ValueError):
        boolean_parser("test")

    with pytest.raises(ValueError):
        boolean_parser(1)


def test_json_parser():
    assert json_parser("{}") == dict()
    assert json_parser('{ "age":100}') == dict(age=100)
    assert json_parser("{\"age\":100 }") == dict(age=100)
    assert json_parser('{"age":100 }') == dict(age=100)
    assert json_parser('{"foo":[5,6.8],"foo":"bar"}') == dict(foo="bar")

    with pytest.raises(ValueError):
        json_parser("{asdf}")

    with pytest.raises(ValueError):
        json_parser("{'age':100 }")


def test_metadatatype():
    assert MetadataType.STRING.name == "STRING"
    assert MetadataType.INTEGER.name == "INTEGER"
    assert MetadataType.BOOLEAN.name == "BOOLEAN"
    assert MetadataType.DECIMAL.name == "DECIMAL"
    assert MetadataType.JSON.name == "JSON"


def test_metadata():
    data = [
        ("b", MetadataType.STRING, "b"),
        ("2", MetadataType.INTEGER, 2),
        ("2.2", MetadataType.DECIMAL, 2.2),
        ("True", MetadataType.BOOLEAN, True),
        ("true", MetadataType.BOOLEAN, True),
        ('{"a":2}', MetadataType.JSON, json.loads('{"a":2}'))
    ]

    for item in data:
        value, dtype, parsed_value = item
        m = Metadata("test", value, dtype, "NAMESPACE")
        assert m.key == "test"
        assert m.raw_value == value
        assert m.dtype == dtype
        assert m.parsed_value == parsed_value
        assert m.namespace == "NAMESPACE"

        m = Metadata("test", value)
        assert m.key == "test"
        assert m.raw_value == value
        assert m.dtype == dtype
        assert m.parsed_value == parsed_value
        assert m.namespace == ""


def test_metadatastore():
    ms = MetadataStore()
    assert len(ms) == 0

    ms.set("a", "b", MetadataType.STRING)
    assert len(ms) == 1
    assert ms["a"] == Metadata("a", "b", MetadataType.STRING)
    assert ms.get("a") == Metadata("a", "b", MetadataType.STRING)
    assert ms.get_value("a") == "b"
    assert ms.get_dtype("a") == MetadataType.STRING

    assert ms.get_dtype("foo", MetadataType.INTEGER) == MetadataType.INTEGER
    assert ms.get_value("foo", 42) == 42

    ms.set("a", "2")
    assert len(ms) == 1
    assert ms.get("a") == Metadata("a", "2", MetadataType.INTEGER)
    assert ms.get("a") == Metadata("a", "2")
    assert ms.get_value("a") == 2
    assert ms.get_value("a", parsed=False) == "2"

    d = dict(a=Metadata("a", 2))
    assert str(ms) == str(d)
    assert repr(ms) == str(d)
    assert next(iter(ms)) == next(iter(d))
    assert ms.keys() == d.keys()
    for a, b in zip(ms.values(), d.values()):
        assert a == b
    for a, b in zip(ms.items(), d.items()):
        assert a == b
    assert "b" not in ms
    assert "a" in ms

    ms["foo"] = Metadata("foo", 2)
    assert "foo" in ms

    with pytest.raises(NotImplementedError):
        del ms["foo"]


def test_to_metadata_store():
    imd = ImageMetadata()
    imd.width = 10
    imd.height = 100
    imd.objective.nominal_magnification = 2
    imd.microscope.model = "foo"
    imd.associated.has_label = True
    imd.set_channel(ImageChannel(index=1))

    store = imd.to_metadata_store(MetadataStore())
    assert store.get_value("image.width") == 10
    assert store.get_value("image.height") == 100
    assert store.get_value("objective.nominal_magnification") == 2
    assert store.get_value("channel[1].index") == 1
    assert store.get_value("microscope.model") == "foo"
    assert store.get_value("associated.has_label") is True