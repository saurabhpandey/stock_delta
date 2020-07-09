"""
Program to find all the dates and stock prices for a given company, where
the change in stock price from previous day is more than given delta.
"""
import yfinance as yf
import unittest


class DeltaStocks(object):
    def __init__(self, stock, start, end, delta):
        self.stock = stock
        self.start = start
        self.end = end
        self.delta = delta
        self.validate()

    def validate(self):
        # We can add more checks, but these are just basic checks
        if not self.stock or not self.start or not self.end or self.delta <= 0:
            raise Exception('Invalid inpur values, exiting.')

    def get_delta_dates(self):
        stocks_by_date = self.fetch_stock_price()
        results = []
        previous = None
        for date, stock in stocks_by_date:
            if previous is None:
                previous = stock
                continue
            calculated_delta = self.find_delta(previous, stock)
            if abs(calculated_delta) >= self.delta:
                results.append((date, stock, calculated_delta))
            previous = stock
        return results

    def find_delta(self, prev, curr):
        return 100*(curr-prev)/prev

    def fetch_stock_price(self):
        stock_obj = yf.Ticker(self.stock)
        stock_data = stock_obj.history(start=self.start, end=self.end)
        stocks_by_date = []
        for data in stock_data.iterrows():
            stocks_by_date.append((str(data[0]), data[1][1]))
        return stocks_by_date

############# SAMPLE RUNS ####################################
"""
ds = DeltaStocks('MSFT', '2020-05-01', '2020-05-10', 0.5)
print(ds.get_delta_dates())
> [('2020-05-01 00:00:00', 178.14, -0.978321289605347), ('2020-05-05 00:00:00', 183.14, 2.5994397759103567)]

ds = DeltaStocks('MSFT', '2020-05-01', '2020-05-10', 0.5)
print(ds.get_delta_dates())
> [('2020-05-01 00:00:00', 178.14, -0.978321289605347), ('2020-05-05 00:00:00', 183.14, 2.5994397759103567)]

ds = DeltaStocks('MSFT', '2020-04-01', '2020-04-10', 5)
print(ds.get_delta_dates())
> [('2020-04-06 00:00:00', 166.04, 5.798394290811772)]

ds = DeltaStocks('MSFT', '2020-04-01', '2020-04-30', 4)
print(ds.get_delta_dates())
> [('2020-04-01 00:00:00', 157.31, -4.266066212268739), ('2020-04-06 00:00:00', 166.04, 5.798394290811772), ('2020-04-14 00:00:00', 173.27, 4.942159772273028)]
"""

class TestDeltaStocks(unittest.TestCase):
    """Few basic unit tests for the DeltaStocks class"""

    def test_valid(self):
        res = DeltaStocks(
            'MSFT', '2020-05-01', '2020-05-10', 0.5).get_delta_dates()
        self.assertEqual(2, len(res))
        expected = [
            ('2020-05-01 00:00:00', 178.14, -0.978321289605347),
            ('2020-05-05 00:00:00', 183.14, 2.5994397759103567)]
        self.assertEqual(expected, res)

        res = DeltaStocks(
            'MSFT', '2020-04-01', '2020-04-10', 5).get_delta_dates()
        self.assertEqual(1, len(res))
        expected = [('2020-04-06 00:00:00', 166.04, 5.798394290811772)]
        self.assertEqual(expected, res)

    def test_invalid(self):
        with self.assertRaises(Exception):
            ds = DeltaStocks('MSFT', '2020-05-01', '2020-05-10', 0)
        with self.assertRaises(Exception):
            ds = DeltaStocks('', '2020-05-01', '2020-05-10', 2)
        with self.assertRaises(Exception):
            ds = DeltaStocks('MSFT', '', '2020-05-10', 2)
        with self.assertRaises(Exception):
            ds = DeltaStocks('MSFT', '2020-05-01', '', 2)


if __name__ == '__main__':
    unittest.main()

############# UNIT TEST CASE RUN ####################################
"""
python3 stock_delta.py
..
----------------------------------------------------------------------
Ran 2 tests in 1.162s

OK
"""