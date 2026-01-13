import pytest
from hooks.set_var_defaults import main
from testing.util import get_resource_path


@pytest.mark.parametrize(
    "asset_path, expected_path",
    [
        (get_resource_path('ExportedAvatar.asset'), get_resource_path('ExportedAvatar_expected.asset')),
        (get_resource_path('MouseSensibility.asset'), get_resource_path('MouseSensibility_expected.asset')),
        (get_resource_path('MusicVolume.asset'), get_resource_path('MusicVolume_expected.asset')),
    ],
    ids=["ExportedAvatar", "MouseSensibility", "MusicVolume"]
)
def test_not_pass(asset_path: str, expected_path: str):
    with open(asset_path, 'rb') as f:
        orig_content_bytes = f.read()
    try:
        ret = main([asset_path])
        assert ret == 1
        with open(asset_path, 'rb') as f:
            changed_content_bytes = f.read()
        with open(expected_path, 'rb') as f:
            expected_content_bytes = f.read()
        assert changed_content_bytes == expected_content_bytes
    finally:
        with open(asset_path, 'wb') as f:
            f.write(orig_content_bytes)


@pytest.mark.parametrize(
    "asset_path",
    [get_resource_path('Name.asset'), get_resource_path('TEEUUID.asset')],
    ids=["Name", "TEEUUID"]
)
def test_pass(asset_path: str):
    with open(asset_path, 'rb') as f:
        orig_content_bytes = f.read()
    try:
        ret = main([asset_path])
        assert ret == 0
        with open(asset_path, 'rb') as f:
            changed_content_bytes = f.read()
        assert orig_content_bytes == changed_content_bytes
    finally:
        with open(asset_path, 'wb') as f:
            f.write(orig_content_bytes)
