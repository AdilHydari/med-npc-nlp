from app import create_app
from dotenv import load_dotenv
import os

load_dotenv()  # This will load environment variables from a .env file

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5200))  # Use the port from environment variable or default to 5200
    app.run(host='0.0.0.0', port=port, debug=True)  # Ensure the port matches the proxy

