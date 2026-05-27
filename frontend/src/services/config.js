const config = {
  apiUrl: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  apiPrefix: process.env.REACT_APP_API_PREFIX || '/api/v1',
  title: process.env.REACT_APP_TITLE || 'LangChain Document QA',
  maxUploadSize: 100 * 1024 * 1024,
  supportedFileTypes: ['.pdf', '.docx', '.txt'],
};

export default config;
