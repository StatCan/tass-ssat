from .reporter_factory import get_reporter


def report(reporter, result):
    _reporter = get_reporter(**reporter)
