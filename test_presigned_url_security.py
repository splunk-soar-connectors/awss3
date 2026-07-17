# Copyright (c) 2026 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from pathlib import Path


def test_presigned_url_method_and_lifetime_are_bounded() -> None:
    connector = (Path(__file__).parent / "s3_connector.py").read_text()

    assert 'client_method != "put_object"' in connector
    assert "1 <= expiration <= 3600" in connector


def test_presigned_url_parameters_are_allowlisted() -> None:
    connector = (Path(__file__).parent / "s3_connector.py").read_text()

    assert 'set(method_parameters) - {"ContentType"}' in connector
    assert "method_parameters.update(required_parameters)" in connector


def test_manifest_exposes_only_put_object() -> None:
    manifest = (Path(__file__).parent / "s3.json").read_text()

    assert '"value_list": [\n                        "put_object"\n                    ]' in manifest
