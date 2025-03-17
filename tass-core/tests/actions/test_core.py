import unittest
import tass.core.actions.core as core
import time


class TestCore(unittest.TestCase):
    def test_waitSeconds(self):
        wait = 3
        delta = 0.1
        startTime = time.time()
        core.wait(wait)
        endTime = time.time()
        self.assertAlmostEqual(endTime - startTime, wait, delta=delta)

    def test_waitMinutes(self):
        wait = 1
        delta = 0.1
        startTime = time.time()
        core.wait(wait, unit="m")
        endTime = time.time()
        self.assertAlmostEqual(endTime - startTime, (wait*60), delta=delta)
