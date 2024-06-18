from app import create_app
from dotenv import load_dotenv

load_dotenv()  # This will load environment variables from a .env file

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)  # Ensure the port matches the proxy