import axios from 'axios';

jest.mock('axios');

describe('API service', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('creates axios instance with correct config', () => {
    const api = require('../../services/api').default;
    expect(axios.create).toHaveBeenCalledWith(
      expect.objectContaining({
        timeout: 30000,
        headers: { 'Content-Type': 'application/json' },
      })
    );
  });

  it('transforms error responses', async () => {
    const errorResponse = {
      response: { data: { detail: 'Document not found' } },
      message: 'Request failed',
    };
    axios.create.mockReturnValue({
      interceptors: {
        response: {
          use: jest.fn((onFulfilled, onRejected) => {
            const result = onRejected(errorResponse);
            expect(result).rejects.toThrow('Document not found');
          }),
        },
      },
    });
    require('../../services/api');
  });

  it('falls back to error message when no detail', async () => {
    const errorResponse = {
      response: { data: {} },
      message: 'Network Error',
    };
    axios.create.mockReturnValue({
      interceptors: {
        response: {
          use: jest.fn((onFulfilled, onRejected) => {
            const result = onRejected(errorResponse);
            expect(result).rejects.toThrow('Network Error');
          }),
        },
      },
    });
    require('../../services/api');
  });
});
