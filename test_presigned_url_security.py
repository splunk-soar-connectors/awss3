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
