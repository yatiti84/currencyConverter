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
    def test_convert_currency_success(self):
        response = self.client.get(
            f'/convert?source={self.source}&target={self.target}&amount={self.amount}',)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], 'success')
        self.assertEqual(data['amount'], '$170,496.53')

    def test_amount_is_float(self):
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

    def test_missing_source_will_fail(self):
        response = self.client.get(
            f'/convert?target={self.target}&amount={self.amount}',)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], 'fail')
        self.assertEqual(data['error_msg'], 'source or target not exists')

    def test_missing_target_will_fail(self):
        response = self.client.get(
            f'/convert?source={self.source}&amount={self.amount}',)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], 'fail')
        self.assertEqual(data['error_msg'], 'source or target not exists')

    def test_missing_amount_will_raise_error(self):
        response = self.client.get(
            f'/convert?source={self.source}&target={self.target}',)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], 'fail')
        self.assertEqual(data['error_msg'], 'amount is missing.')

    def test_target_ignore_case(self):
        self.target = 'jpy'
        response = self.client.get(
            f'/convert?source={self.source}&target={self.target}&amount={self.amount}',)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], 'success')
        self.assertEqual(data['amount'], '$170,496.53')

    def test_source_ignore_case(self):
        self.source = 'usd'
        response = self.client.get(
            f'/convert?source={self.source}&target={self.target}&amount={self.amount}',)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], 'success')
        self.assertEqual(data['amount'], '$170,496.53')

    def test_negative_amount_will_fail(self):
        self.amount = '-1'
        response = self.client.get(
            f'/convert?source={self.source}&target={self.target}&amount={self.amount}',)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], 'fail')
        self.assertEqual(data['error_msg'],
                         'amount needs to be greater or equal than 0')

    def test_amount_is_not_number(self):
        self.amount = "hello"
        response = self.client.get(
            f'/convert?source={self.source}&target={self.target}&amount={self.amount}',)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['msg'], 'fail')
        self.assertEqual(data['error_msg'],
                         "could not convert string to float: 'hello'")
