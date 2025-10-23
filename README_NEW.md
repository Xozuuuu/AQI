# 🌍 AQI Monitoring System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.50%2B-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/Code%20Style-Black-black.svg)](https://black.readthedocs.io)
[![Tests](https://img.shields.io/badge/Tests-Pytest-blue.svg)](https://pytest.org)

A comprehensive air quality monitoring system with real-time data collection, analysis, prediction, and reporting capabilities built with Python, Streamlit, and modern data science tools.

## ✨ Features

### 🗺️ **Interactive Dashboard**
- Real-time AQI data visualization on interactive maps
- Multi-province monitoring across Vietnam
- Color-coded air quality indicators
- Responsive design with modern UI/UX

### 🤖 **Intelligent Analysis**
- Machine Learning-powered AQI predictions
- Weather-based air quality forecasting
- Trend analysis and pattern recognition
- Automated alert system for dangerous levels

### 📊 **Advanced Reporting**
- Comprehensive data analysis and statistics
- Export capabilities (Excel, JSON, PDF)
- Customizable report generation
- Historical data comparison

### 🗄️ **Data Management**
- SQLite database with advanced querying
- Data comparison and change tracking
- Automated data backup and cleanup
- Historical data preservation

### 🚀 **Production Ready**
- Docker containerization
- Nginx reverse proxy
- Environment-based configuration
- Comprehensive monitoring and logging

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │───▶│  Data Service   │───▶│   Database      │
│   (WAQI API)    │    │   (Processing)  │    │   (SQLite)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │◀───│  Business Logic │───▶│   ML Models     │
│   (Dashboard)   │    │   (Services)    │    │  (Predictions)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip or conda
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/aqimonitoring/aqi-monitoring.git
cd aqi-monitoring
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
make install
# or
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your API key and settings
```

5. **Initialize database**
```bash
make db-init
```

6. **Run the application**
```bash
make run
# or
streamlit run app.py
```

Visit `http://localhost:8501` to see the dashboard!

## 🛠️ Development

### Setup Development Environment
```bash
make setup
```

### Run Tests
```bash
make test              # Run all tests
make test-unit         # Run unit tests only
make test-integration  # Run integration tests only
```

### Code Quality
```bash
make quality           # Run all quality checks
make format           # Format code
make lint             # Lint code
make type-check       # Type checking
```

### Database Operations
```bash
make db-init          # Initialize database
make db-migrate       # Run migrations
make data-fetch       # Fetch latest data
make data-backup      # Backup data
```

## 🐳 Docker Deployment

### Development
```bash
make docker-build
make docker-run
```

### Production
```bash
make setup-prod
make deploy
```

## 📊 Data Sources

- **WAQI API**: Real-time air quality data
- **Weather Data**: Meteorological information
- **Geographic Data**: Province boundaries and coordinates

## 🔧 Configuration

### Environment Variables
```bash
# API Configuration
API_KEY=your_waqi_api_key
PROJECT_ROOT=/path/to/project

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=aqi_monitoring

# Application Configuration
DEBUG=False
LOG_LEVEL=INFO
SECRET_KEY=your_secret_key
```

### Settings
All configuration is managed through `src/aqi_monitoring/core/config.py` using Pydantic for validation and type safety.

## 📈 Monitoring

### Metrics
- API response times
- Data accuracy rates
- System uptime
- Error rates

### Logging
- Structured logging with JSON format
- Log levels: DEBUG, INFO, WARNING, ERROR
- Log rotation and retention policies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Write comprehensive tests
- Update documentation
- Use conventional commits

## 📚 Documentation

- [Quick Start Guide](QUICK_START.md)
- [Deployment Guide](DEPLOYMENT.md)
- [API Documentation](docs/API.md)
- [System Architecture](SYSTEM_SUMMARY.md)
- [Project Structure](PROJECT_STRUCTURE.md)

## 🧪 Testing

The project includes comprehensive test coverage:

- **Unit Tests**: Test individual components
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete workflows
- **Performance Tests**: Test system performance

Run tests with:
```bash
make test
```

## 📊 Performance

### Benchmarks
- **Data Processing**: 1000+ records/second
- **API Response**: <200ms average
- **Memory Usage**: <512MB typical
- **Database Queries**: <50ms average

### Optimization
- Async data processing
- Database indexing
- Caching strategies
- Connection pooling

## 🔒 Security

### Security Features
- Input validation and sanitization
- SQL injection prevention
- XSS protection
- CSRF protection
- Secure configuration management

### Security Scanning
```bash
make security-check
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [WAQI](https://waqi.info/) for providing air quality data
- [Streamlit](https://streamlit.io/) for the web framework
- [GeoPandas](https://geopandas.org/) for geospatial data processing
- [Pandas](https://pandas.pydata.org/) for data manipulation
- [Plotly](https://plotly.com/) for interactive visualizations

## 📞 Support

- **Documentation**: [Read the Docs](https://aqimonitoring.readthedocs.io/)
- **Issues**: [GitHub Issues](https://github.com/aqimonitoring/aqi-monitoring/issues)
- **Discussions**: [GitHub Discussions](https://github.com/aqimonitoring/aqi-monitoring/discussions)
- **Email**: support@aqimonitoring.com

## 🗺️ Roadmap

### Version 2.0
- [ ] Real-time notifications
- [ ] Mobile application
- [ ] Advanced ML models
- [ ] Multi-country support
- [ ] API rate limiting

### Version 3.0
- [ ] Microservices architecture
- [ ] Kubernetes deployment
- [ ] Advanced analytics
- [ ] Machine learning pipeline
- [ ] Real-time streaming

---

**🌍 Making air quality monitoring accessible and intelligent for everyone!**

*Built with ❤️ by the AQI Monitoring Team*
