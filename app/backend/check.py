"""Check configured OpenAI access without exposing credentials or provider error bodies."""
import sys
from openai import APIError, OpenAI
from core.config import get_settings


def main():
    settings = get_settings()
    if not settings.openai_api_key or not settings.openai_api_key.get_secret_value().strip():
        print('OpenAI API key is not configured.', file=sys.stderr)
        return 1
    try:
        with OpenAI(
            api_key=settings.openai_api_key.get_secret_value(),
            timeout=settings.openai_timeout_seconds, max_retries=settings.openai_max_retries,
        ) as client:
            for model in client.models.list():
                if 'gpt' in model.id:
                    print(model.id)
    except APIError as error:
        print(f'OpenAI access check failed ({type(error).__name__}).', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
