import unittest
from unittest.mock import patch, MagicMock
from app import fetch_articles  # Replace with the correct import path

class TestFetchArticles(unittest.TestCase):
    
    @patch('app.requests.get')  # Mocking the requests.get call
    def test_fetch_articles_success(self, mock_get):
        """Test when API call is successful"""
        
        # Sample mock response data
        mock_response_data = {
            'articles': [
                {'title': 'Test Article 1', 'description': 'Description 1', 'url': 'http://example.com/1'},
                {'title': 'Test Article 2', 'description': 'Description 2', 'url': 'http://example.com/2'}
            ],
            'totalResults': 2
        }
        
        # Configuring the mock to return the above data as JSON
        mock_get.return_value = MagicMock(status_code=200)
        mock_get.return_value.json.return_value = mock_response_data
        
        # Call the function to test
        articles, total_results = fetch_articles(page=1)
        
        # Assertions
        self.assertEqual(len(articles), 2)
        self.assertEqual(total_results, 2)
        self.assertEqual(articles[0]['title'], 'Test Article 1')
        self.assertEqual(articles[1]['description'], 'Description 2')

    @patch('app.requests.get')
    def test_fetch_articles_with_topic(self, mock_get):
        """Test fetching articles with a specific topic"""
        
        # Sample mock response data for a specific topic
        mock_response_data = {
            'articles': [
                {'title': 'Tech News', 'description': 'Latest in tech', 'url': 'http://example.com/tech'}
            ],
            'totalResults': 1
        }
        
        mock_get.return_value = MagicMock(status_code=200)
        mock_get.return_value.json.return_value = mock_response_data
        
        # Call the function with a specific topic
        articles, total_results = fetch_articles(page=1, topic='technology')
        
        # Assertions
        self.assertEqual(len(articles), 1)
        self.assertEqual(total_results, 1)
        self.assertEqual(articles[0]['title'], 'Tech News')

    @patch('app.requests.get')
    def test_fetch_articles_api_failure(self, mock_get):
        """Test when API call fails (non-200 status code)"""
        
        # Configure the mock to return a failed response
        mock_get.return_value = MagicMock(status_code=500)
        
        # Call the function to test
        articles, total_results = fetch_articles(page=1)
        
        # Assertions
        self.assertEqual(articles, [])  # Expecting empty list
        self.assertEqual(total_results, 0)  # Expecting 0 total results

    @patch('app.requests.get')
    def test_fetch_articles_no_articles(self, mock_get):
        """Test when no articles are returned by the API"""
        
        # Mocking an empty articles response
        mock_response_data = {
            'articles': [],
            'totalResults': 0
        }
        
        mock_get.return_value = MagicMock(status_code=200)
        mock_get.return_value.json.return_value = mock_response_data
        
        # Call the function
        articles, total_results = fetch_articles(page=1)
        
        # Assertions
        self.assertEqual(articles, [])  # No articles should be returned
        self.assertEqual(total_results, 0)  # Total results should be 0


if __name__ == '__main__':
    unittest.main()
