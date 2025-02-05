from unittest import TestCase

class TestHeadlessMode(TestCase):
    def test_pygame_independence(self):
        import sys

        self.assertFalse('pygame' in sys.modules, "Pre import of AchtungDieKurveGame, pygame should not be included")

        from game import AchtungDieKurveGame

        game = AchtungDieKurveGame(mode="headless")

        self.assertFalse('pygame' in sys.modules, msg="pygame should not be imported in 'headless' mode")


    def test_headless_run(self):
        pass

