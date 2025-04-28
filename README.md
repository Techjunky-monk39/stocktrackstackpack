# StockTrackStackPack

StockTrackStackPack is a Python-based application designed for stock analysis and tracking. It provides tools for analyzing stock data, generating insights, and visualizing trends using various Python libraries.

## Features
- **Stock Analysis**: Analyze stock data using `stock_analysis.py`.
- **AI Insights**: Generate AI-driven insights with `ai_insights.py`.
- **User Authentication**: Manage user authentication with `auth.py`.
- **Database Integration**: Handle database operations with `database.py`.
- **Streamlit Interface**: A user-friendly web interface built with Streamlit.

## Prerequisites
- Python 3.11 or higher
- Docker (optional, for containerized deployment)

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd stocktrackstackpack
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application
### Locally
Run the application using Streamlit:
```bash
streamlit run app.py
```

### Using Docker
1. Build the Docker image:
   ```bash
   docker build -t stocktrackstackpack .
   ```

2. Run the Docker container:
   ```bash
   docker run -p 5000:5000 stocktrackstackpack
   ```

3. Access the application at `http://localhost:5000`.

## File Structure
- `app.py`: Main entry point for the Streamlit application.
- `ai_insights.py`: AI-driven insights module.
- `auth.py`: User authentication module.
- `database.py`: Database interaction module.
- `stock_analysis.py`: Stock analysis tools.
- `user_data.py`: User data management.
- `utils.py`: Utility functions.
- `.streamlit/config.toml`: Streamlit configuration.
- `requirements.txt`: Python dependencies.
- `Dockerfile`: Docker configuration.
- `pyproject.toml`: Project metadata and dependencies.

## Troubleshooting

If you encounter issues, follow these steps:

1. **Check Logs**:
   - Application errors: Refer to `app_errors.log`.
   - Database errors: Refer to `db_errors.log`.

2. **Verify Dependencies**:
   Ensure all dependencies in `requirements.txt` are installed:
   ```bash
   pip install -r requirements.txt
   ```

3. **Validate Database Connection**:
   Test the database connection using `test_db_connection.py`:
   ```bash
   python test_db_connection.py
   ```

4. **Contact Support**:
   If the issue persists, please submit an issue with detailed logs.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.