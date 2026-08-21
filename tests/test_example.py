from performance_lab.runner import Runner


def test_example_program():
    runner = Runner("examples/example.py")
    result = runner.run()

    assert result.returncode == 0
    assert "Hello, Jadon!" in result.stdout

    print(result.stdout)