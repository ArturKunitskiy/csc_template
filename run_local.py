"""Local development: python run_local.py"""

from app import create_app

if __name__ == "__main__":
    create_app().run(debug=True, port=5000)
