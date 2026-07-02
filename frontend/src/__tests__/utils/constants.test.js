describe('constants', () => {
  beforeEach(() => {
    delete process.env.REACT_APP_API_URL;
    delete process.env.REACT_APP_API_PREFIX;
    jest.resetModules();
  });

  it('uses default API_URL when env var is not set', () => {
    const { API_URL } = require('../../utils/constants');
    expect(API_URL).toBe('http://localhost:8000');
  });

  it('uses env var API_URL when set', () => {
    process.env.REACT_APP_API_URL = 'http://api.example.com';
    const { API_URL } = require('../../utils/constants');
    expect(API_URL).toBe('http://api.example.com');
  });

  it('exports expected constants', () => {
    const constants = require('../../utils/constants');
    expect(constants.API_PREFIX).toBe('/api/v1');
    expect(constants.MAX_UPLOAD_SIZE).toBe(100);
    expect(constants.SUPPORTED_TYPES).toEqual(['pdf', 'docx', 'txt']);
    expect(constants.DEFAULT_TOP_K).toBe(5);
  });
});
