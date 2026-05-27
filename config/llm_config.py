from pydantic_settings import BaseSettings


class LLMConfiguration(BaseSettings):
    default_provider: str = "openai"
    openai_model: str = "gpt-4o-mini"
    anthropic_model: str = "claude-3-opus-20240229"
    local_model: str = "llama3.2"
    temperature: float = 0.0
    max_tokens: int = 4096
    top_p: float = 1.0

    class Config:
        env_prefix = "LLM_"
        extra = "ignore"
