import uuid
from concurrent.futures import ThreadPoolExecutor
from django.test import TestCase
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from .models import Wallet


# Create your tests here.

class ModelTestCase(TestCase):
    def setUp(self):
        self.wallet_rub = Wallet.objects.create(currency='RUB', balance=90000)
        self.wallet_usd = Wallet.objects.create(currency='USD', balance=80000)
        self.wallet_eur = Wallet.objects.create(currency='EUR', balance=70000)

    def test_wallet_creation(self):
        self.assertEqual(self.wallet_rub.currency, 'RUB')
        self.assertEqual(self.wallet_rub.balance, 90000)
        self.assertEqual(self.wallet_usd.currency, 'USD')
        self.assertEqual(self.wallet_usd.balance, 80000)
        self.assertEqual(self.wallet_eur.currency, 'EUR')
        self.assertEqual(self.wallet_eur.balance, 70000)

    def test_all_currencies(self):
        self.wallet_rub = Wallet.objects.create(currency='RUB', balance=999999)
        self.wallet_usd = Wallet.objects.create(currency='USD', balance=888888)
        self.wallet_eur = Wallet.objects.create(currency='EUR', balance=777777)

    def test_float_balance(self):
        self.wallet_rub = Wallet.objects.create(currency='RUB', balance=999999.0)
        self.wallet_usd = Wallet.objects.create(currency='USD', balance=80000.0)
        self.wallet_eur = Wallet.objects.create(currency='EUR', balance=70000.0)
        self.wallet_rub = Wallet.objects.create(currency='RUB', balance=999999.00)
        self.wallet_usd = Wallet.objects.create(currency='USD', balance=80000.00)
        self.wallet_eur = Wallet.objects.create(currency='EUR', balance=70000.00)


class TestAPI(APITestCase):

    def test_create_wallet(self):
        # Creating new record by post request
        data = {'currency': 'USD', 'balance': '7777'}
        response = self.client.post('/api/v1/wallets', data)
        # Object is created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Wallet.objects.last().currency, 'USD')
        self.assertEqual(Wallet.objects.last().balance, 7777)


class TestWalletAPI(APITestCase):
    def setUp(self):
        self.wallet = Wallet.objects.create(currency='RUB', balance=5000)
        self.wallet_url = reverse('wallet_operation', kwargs={'uuid': self.wallet.uuid})
        self.mock_wallet_url = reverse('wallet_operation', kwargs={'uuid': uuid.uuid4()})

    def test_deposit(self):
        initial_balance = self.wallet.balance
        deposit_amount = 1000
        data = {
            'operationType': 'DEPOSIT',
            'amount': deposit_amount
        }

        response = self.client.post(self.wallet_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.wallet.refresh_from_db()
        expected_balance = initial_balance + deposit_amount
        self.assertEqual(self.wallet.balance, expected_balance)
        self.assertEqual(response.data['balance'], expected_balance)

    def test_withdraw(self):
        initial_balance = self.wallet.balance
        withdraw_amount = 2000
        data = {
            'operationType': 'WITHDRAW',
            'amount': withdraw_amount
        }
        response = self.client.post(self.wallet_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.wallet.refresh_from_db()
        expected_balance = initial_balance - withdraw_amount
        self.assertEqual(self.wallet.balance, expected_balance)
        self.assertEqual(response.data['balance'], expected_balance)

    def test_not_enough_balance(self):
        initial_balance = self.wallet.balance
        withdraw_amount = 6000
        data = {
            'operationType': 'WITHDRAW',
            'amount': withdraw_amount
        }
        response = self.client.post(self.wallet_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # we get expected error
        self.assertEqual(response.data['error'], "Not enough balance")
        # balance didnt change
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, initial_balance)

    def test_wallet_does_not_exist(self):
        data = {
            'operationType': 'DEPOSIT',
            'amount': 1000
        }
        response = self.client.post(self.mock_wallet_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # we get expected error
        self.assertEqual(response.data['error'], "Wallet does not exist")

    def test_invalid_operation_type(self):
        invalid_operation_type = 'INVALID'
        data = {
            'operationType': invalid_operation_type,
            'amount': 1000
        }
        response = self.client.post(self.wallet_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # we get expected error
        self.assertEqual(response.data['operationType'], [
            ErrorDetail(string=f'"{invalid_operation_type}" is not a valid choice.', code='invalid_choice')])

    def test_invalid_amount(self):
        data_1 = {
            'operationType': 'DEPOSIT',
            'amount': -1000
        }
        data_2 = {
            'operationType': 'WITHDRAW',
            'amount': -1000
        }
        data_3 = {
            'operationType': 'DEPOSIT',
            'amount': 0
        }
        data_4 = {
            'operationType': 'WITHDRAW',
            'amount': 0
        }

        data_lte_0 = [data_1, data_2, data_3, data_4]

        for data in data_lte_0:
            response = self.client.post(self.wallet_url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            # we get expected error
            self.assertEqual(response.data['error'], 'Amount must be bigger than zero')

    def test_concurrent_requests(self):
        initial_balance = self.wallet.balance
        amount = 10
        cycles = 1000
        data = {
            'operationType': 'DEPOSIT',
            'amount': amount
        }
        with ThreadPoolExecutor(max_workers=10):
            responses = []
            for _ in range(cycles):
                response = self.client.post(self.wallet_url, data, format='json')
                responses.append(response)
            # checkout results
            for response in responses:
                self.assertEqual(response.status_code, 200)
        expected_balance = initial_balance + amount*cycles
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, expected_balance)

    def test_invalid_json_syntax(self):
        invalid_json = '{"key": "value" "another_key": "another_value"}'
        response = self.client.post(self.wallet_url, data=invalid_json, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_json_structure(self):
        invalid_json = '{"key": "value", "another_key": }'
        response = self.client.post(self.wallet_url, data=invalid_json, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_json_data(self):
        invalid_json = '{"key": undefined}'
        response = self.client.post(self.wallet_url, data=invalid_json, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


