import unittest
from unittest.mock import patch, Mock
from index import determine_status, lambda_handler

class TestLambdaFunction(unittest.TestCase):
    def test_determine_status_upcoming(self):
        self.assertEqual(determine_status('2025-04-01T12:00:00.000Z', None), 'upcoming')

    def test_determine_status_success(self):
        self.assertEqual(determine_status('2024-03-01T12:00:00.000Z', True), 'success')

    def test_determine_status_failed(self):
        self.assertEqual(determine_status('2024-03-01T12:00:00.000Z', False), 'failed')

    @patch('index.requests.get')
    @patch('index.boto3.resource')
    def test_lambda_handler_manual(self, mock_dynamodb, mock_requests):
        # Mockear respuestas de la API
        mock_rockets = Mock()
        mock_rockets.json.return_value = [{'id': 'falcon9', 'name': 'Falcon 9'}]
        mock_launches = Mock()
        mock_launches.json.return_value = [{
            'id': 'launch1',
            'name': 'Starlink-1',
            'rocket': 'falcon9',
            'date_utc': '2024-03-01T12:00:00.000Z',
            'success': True
        }]
        mock_requests.side_effect = [mock_rockets, mock_launches]

        # Mockear DynamoDB
        mock_table = Mock()
        mock_table.get_item.return_value = {}
        mock_dynamodb.return_value.Table.return_value = mock_table

        # Invocar manualmente
        result = lambda_handler({}, None)
        self.assertEqual(result['statusCode'], 200)
        self.assertIn('new_launches', json.loads(result['body']))

if __name__ == '__main__':
    unittest.main()