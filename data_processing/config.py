from dotenv import load_dotenv, find_dotenv

# Load environment variables from a .env file
def load_env(env_path):
    dotenv_path = find_dotenv(env_path)
    load_dotenv(dotenv_path, override=True)
