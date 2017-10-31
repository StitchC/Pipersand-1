from unittest import TestCase

from ..core.Company import Company

class FunctionalTest(TestCase):

    def test_start_game_with_initial_state(self):
        company = Company()
        # 公司状态是第一年第一季
        self.assertEqual(company.year, 1)
        self.assertEqual(company.season, 1)
        # 现金是60
        self.assertEqual(company.cash, 60)

    # def test_
