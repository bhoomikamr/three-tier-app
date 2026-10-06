import pytest
from unittest.mock import MagicMock, patch
from worker import process_next_task # Assuming worker processing logic is inside process_next_task

def test_worker_process_task_success():
    """Verify worker pops Redis task and updates DB status to Completed."""
    mock_redis = MagicMock()
    mock_db_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_db_conn.cursor.return_value = mock_cursor

    # Simulate popping a task ID from Redis queue
    mock_redis.brpop.return_value = ('task_queue', '1')

    with patch('worker.get_db_connection', return_value=mock_db_conn):
        # Run worker cycle
        processed = process_next_task(mock_redis)

        assert processed is True
        # Verify DB status update execution
        mock_cursor.execute.assert_called_with(
            "UPDATE tasks SET status = %s WHERE id = %s",
            ('Completed', 1)
        )
        mock_db_conn.commit.assert_called_once()