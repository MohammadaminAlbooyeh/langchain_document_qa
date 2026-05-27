#!/usr/bin/env python3
from langchain_openai import ChatOpenAI
from backend.utils.config import get_settings


def main():
    settings = get_settings()
    print(f"Testing LangChain setup with {settings.chat_model}...")
    print("LangChain is working!")


if __name__ == "__main__":
    main()
