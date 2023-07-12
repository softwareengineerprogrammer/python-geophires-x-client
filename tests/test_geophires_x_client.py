from geophires_x_client.cli import main


def test_main():
    assert main([]) == 0
