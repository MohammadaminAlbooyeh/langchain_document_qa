# Troubleshooting

## Common Issues

### API Key Errors
Ensure your `.env` file has valid API keys.

### Database Errors
Run `python scripts/init_db.py` to initialize the database.

### Vector Store Errors
Delete the `chroma_db/` directory and restart.

### CORS Errors
Ensure the frontend URL is in the CORS allow list.
