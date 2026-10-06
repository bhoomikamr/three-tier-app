import pytest
import json
from unittest.mock import MagicMock, patch
# Assuming your main Flask file is app.py
from app import app 

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_tasks_empty(client):
    """Test retrieving tasks when DB returns empty results."""
    with patch('app.get_db_connection') as mock_db:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn

        response = client.get('/api/v1/tasks')
        assert response.status_code == 200
        assert json.loads(response.data) == []

def test_create_task_success(client):
    """Test creating a task: verifies DB insert and Redis queue push."""
    with patch('app.get_db_connection') as mock_db, \
         patch('app.redis_client') as mock_redis:
        
        # Mock DB Cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (1, 'Run Sync Pipeline', 'Pending')
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn

        # Execute POST request
        payload = {'title': 'Run Sync Pipeline'}
        response = client.post(
            '/api/v1/tasks',
            data=json.dumps(payload),
            content_type='application/json'
        )

        # Assertions
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['id'] == 1
        assert data['status'] == 'Pending'
        
        # Verify Redis lpush was triggered for the worker
        mock_redis.lpush.assert_called_once()