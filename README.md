# Network-Traffic-Load-Balacer

# Distributed Load Balancer System

A production-ready, intelligent load balancing solution built with Python Flask that distributes HTTP traffic across multiple backend servers with real-time monitoring and multiple routing algorithms.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🚀 Features

### Core Capabilities
- **4 Load Balancing Algorithms**: Round Robin, Least Connections, Weighted Distribution, and Least Response Time
- **Automatic Health Monitoring**: Continuous health checks with automatic failover
- **Real-time Dashboard**: Beautiful, minimalist web interface with live metrics
- **High Availability**: Sub-second failover detection and recovery
- **Performance Tracking**: Comprehensive metrics and analytics
- **Dynamic Algorithm Switching**: Change routing strategies without restart

### Technical Highlights
- ✅ CORS-enabled for cross-origin requests
- ✅ Concurrent request handling with connection tracking
- ✅ Response time monitoring and optimization
- ✅ Request history logging (last 100 requests)
- ✅ RESTful API for programmatic control
- ✅ Zero-downtime configuration changes

## 📊 Dashboard Preview

The dashboard provides real-time visibility into:
- Total requests and success rates
- Individual server health status
- Request distribution charts
- Response time analytics
- Active connection monitoring

## 🏗️ Architecture

```
┌─────────────┐
│   Clients   │
└──────┬──────┘
       │
       ▼
┌──────────────────────┐
│   Load Balancer      │  Port 9000
│   (load_balancer.py) │
└──────┬───────────────┘
       │
       ├──────────┬──────────┬
       ▼          ▼          ▼  
   ┌────────┐ ┌────────┐ ┌────────┐
   │Backend1│ │Backend2│ │Backend3│
   │Port    │ │Port    │ │Port    │
   │5001    │ │5002    │ │5003    │
   └────────┘ └────────┘ └────────┘
```

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/load-balancer.git
cd load-balancer
```

2. **Install dependencies**
```bash
pip install flask flask-cors requests
```

3. **Start the system**
```bash
# Windows
start_all.bat

# Manual start (any OS)
python Backend_server.py  # Run 3 times with different ports
python load_balancer.py
```

4. **Open the dashboard**
```bash
# Open Dashboard.html in your browser
# Access: http://localhost:9000
```

## 📖 Quick Start Guide

### Start Complete System
```bash
start_all.bat
```
Launches all 3 backend servers and the load balancer on port 9000.

### Send Test Requests
```bash
# Via curl
curl http://localhost:9000/api/process

# Via dashboard
Open Dashboard.html → Click "Send 10" button
```

### Change Algorithm
```bash
curl -X POST http://localhost:9000/algorithm \
  -H "Content-Type: application/json" \
  -d '{"algorithm": "least_connections"}'
```

### Check Status
```bash
curl http://localhost:9000/status
```

## 🎯 Load Balancing Algorithms

| Algorithm               | Best For                    | Distribution            |
|-------------------------|-----------------------------|-------------------------|
| **Round Robin**         | Equal-capacity servers      | 33% / 33% / 33%         |
| **Least Connections**   | Varying request complexity  | Dynamic                 |
| **Weighted**            | Different server capacities | 50% / 33% / 17% (3:2:1) |
| **Least Response Time** | Performance optimization    | Performance-based       |

## 📡 API Reference

### Main Endpoints

**Process Request**
```http
GET/POST /api/process
```

**Get Status**
```http
GET /status
```

**Health Check**
```http
GET /health
```

**Change Algorithm**
```http
POST /algorithm
Content-Type: application/json

{
  "algorithm": "round_robin" | "least_connections" | "weighted" | "least_response_time"
}
```

**Reset Statistics**
```http
POST /reset
```

## 🧪 Testing

Run the included test suite:
```bash
python test_client.py
```

Tests include:
- Sequential request handling
- Concurrent request processing
- Load distribution verification
- Response time analysis

## 🐛 Troubleshooting

**Port already in use**
```bash
netstat -ano | findstr :9000
taskkill /PID [PID] /F
```

**Dashboard not connecting**
- Verify load balancer is running
- Check browser console (F12) for errors
- Ensure port 9000 is accessible

**Backend servers unhealthy**
```bash
curl http://localhost:5001/health
curl http://localhost:5002/health
curl http://localhost:5003/health
```

## 📁 Project Structure

```
load-balancer/
├── load_balancer.py       # Main load balancer
├── Backend_server.py      # Backend server code
├── Dashboard.html         # Web monitoring interface
├── test_client.py         # Testing suite
├── start_all.bat          # Complete system launcher
├── start_backends.bat     # Backend servers launcher
├── start_loadbalancer.bat # Load balancer launcher
└── Documentation.docx     # Complete documentation
```

## 🚀 Use Cases

- **Microservices Architecture**: Distribute traffic across service instances
- **High-Traffic Applications**: Handle thousands of concurrent requests
- **Development & Testing**: Test distributed system behavior
- **Learning & Education**: Understand load balancing concepts
- **API Gateway**: Route API requests to backend services

## 🔮 Future Enhancements

- [ ] SSL/TLS support
- [ ] Docker containerization
- [ ] Kubernetes integration
- [ ] Database persistence
- [ ] Authentication & rate limiting
- [ ] WebSocket support
- [ ] Auto-scaling capabilities
- [ ] Prometheus metrics export

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👨‍💻 Author

Alian Rafiq
Cyc07820

⭐ **Star this repo** if you find it helpful!

📧 **Questions?** Open an issue or contact [alianrafiq2003@gmail.com](mailto:alianrafiq2003@gmail.com) [cyc0istic782@gmail.com](mailto:cyc0istic782@gmail.com)
