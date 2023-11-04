import unittest
from flask_testing import TestCase
from app import create_app


class SettingBase(TestCase):
    def create_app(self):
        return create_app('testing')

    def setUp(self):
        self.source = 'USD'
        self.target = 'JPY'
        self.amount = '$1,525'

class CheckCurrencyConvert(SettingBase):
    def test_convert_currency(self):
        response = self.client.get(
            f'/convert?source={self.source}&target={self.target}&amount={self.amount}',)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], 'success')
        self.assertEqual(data['amount'], '$170,496.53')

    def test_amount_float(self):
        self.amount = '$1.525'
        response = self.client.get(
            f'/convert?source={self.source}&target={self.target}&amount={self.amount}',)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], 'success')
        self.assertEqual(data['amount'], '$170.5')

    def test_not_exist_currency_name(self):
        self.source = 'ABC'
        response = self.client.get(
            f'/convert?source={self.source}&target={self.target}&amount={self.amount}',)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], 'fail')
        self.assertEqual(data['error_msg'], 'source or target not exists')

    def test_missing_parameter(self):
        response = self.client.get(
            f'/convert?target={self.target}&amount={self.amount}',)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], 'fail')
        self.assertEqual(data['error_msg'], 'source or target not exists')

    def test_case_sensitive(self):
        self.target = 'jpy'
        response = self.client.get(
            f'/convert?source={self.source}&target={self.target}&amount={self.amount}',)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], 'success')
        self.assertEqual(data['amount'], '$170,496.53')

    def test_negative_amount(self):
        self.amount = '-1'
        response = self.client.get(
            f'/convert?source={self.source}&target={self.target}&amount={self.amount}',)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], 'fail')
        self.assertEqual(data['error_msg'],
                         'amount needs to be greater or equal than 0')
    

if __name__ == '__main__':
    unittest.main()
