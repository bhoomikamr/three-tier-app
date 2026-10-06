import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from './App';

// Mock fetch globally
global.fetch = jest.fn();

beforeEach(() => {
  fetch.mockClear();
});

test('renders dashboard heading and existing tasks', async () => {
  // Mock API returning initial tasks
  fetch.mockResolvedValueOnce({
    ok: true,
    json: async () => [
      { id: 1, title: 'Hi', status: 'Completed' },
      { id: 2, title: 'Run Sync Pipeline', status: 'Pending' }
    ],
  });

  render(<App />);

  expect(screen.getByText(/Production Task Dashboard/i)).toBeInTheDocument();

  // Wait for async fetch to render list items
  await waitFor(() => {
    expect(screen.getByText(/Hi - Status: Completed/i)).toBeInTheDocument();
    expect(screen.getByText(/Run Sync Pipeline - Status: Pending/i)).toBeInTheDocument();
  });
});

test('submits a new task via input form', async () => {
  // 1st fetch call: Initial load
  fetch.mockResolvedValueOnce({
    ok: true,
    json: async () => [],
  });

  render(<App />);

  // 2nd fetch call: POST response for creation
  fetch.mockResolvedValueOnce({
    ok: true,
    json: async () => ({ id: 3, title: 'New Test Task', status: 'Pending' }),
  });

  const input = screen.getByPlaceholderText(/Enter new critical task/i);
  const submitButton = screen.getByRole('button', { name: /Submit/i });

  fireEvent.change(input, { target: { value: 'New Test Task' } });
  fireEvent.click(submitButton);

  await waitFor(() => {
    expect(fetch).toHaveBeenCalledWith(
      '/api/v1/tasks',
      expect.objectContaining({
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: 'New Test Task' }),
      })
    );
  });
});