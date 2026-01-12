from hooks.set_var_defaults import main
from testing.util import get_resource_path


def test_game_var_not_pass():
    orig_path = get_resource_path('MouseSensibility.asset')
    expected_path = get_resource_path('MouseSensibility_expected.asset')
    with open(orig_path, 'rb') as f:
        orig_content = f.read()
    try:
        ret = main([orig_path])
        assert ret == 1
        with open(orig_path, 'r') as f:
            changed_content = f.read()
        with open(expected_path, 'r') as f:
            expected_content = f.read()
        assert changed_content.strip() == expected_content.strip()
    finally:
        with open(orig_path, 'wb') as f:
            f.write(orig_content)


def test_game_var_not_pass_anchor():
    orig_path = get_resource_path('ExportedAvatar.asset')
    expected_path = get_resource_path('ExportedAvatar_expected.asset')
    with open(orig_path, 'rb') as f:
        orig_content = f.read()
    try:
        ret = main([orig_path])
        assert ret == 1
        with open(orig_path, 'r') as f:
            changed_content = f.read()
        with open(expected_path, 'r') as f:
            expected_content = f.read()
        assert changed_content.strip() == expected_content.strip()
    finally:
        with open(orig_path, 'wb') as f:
            f.write(orig_content)


def test_game_var_pass():
    orig_path = get_resource_path('Name.asset')
    with open(orig_path, 'r') as f:
        orig_content = f.read()
    try:
        ret = main([orig_path])
        with open(orig_path, 'r') as f:
            changed_content = f.read()
        assert changed_content.strip() == orig_content.strip()
    finally:
        with open(orig_path, 'w') as f:
            f.write(orig_content)


def test_not_game_var():
    orig_path = get_resource_path('TEEUUID.asset')
    with open(orig_path, 'rb') as f:
        orig_content = f.read()
    try:
        ret = main([orig_path])
        assert ret == 0
    finally:
        with open(orig_path, 'wb') as f:
            f.write(orig_content)
