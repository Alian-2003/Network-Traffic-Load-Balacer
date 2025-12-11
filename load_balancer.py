"""
Enhanced Distributed Load Balancer with CORS Support
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os
import time
import threading
from collections import defaultdict
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for dashboard

# Load Balancer Configuration
LB_ID = os.getenv('LB_ID', 'load_balancer_1')
LB_PORT = int(os.getenv('LB_PORT', 9000))
ALGORITHM = os.getenv('ALGORITHM', 'round_robin')

# Backend servers configuration
BACKEND_SERVERS = [
    {'id': 'backend_1', 'url': 'http://localhost:5001', 'weight': 3},
    {'id': 'backend_2', 'url': 'http://localhost:5002', 'weight': 2},
    {'id': 'backend_3', 'url': 'http://localhost:5003', 'weight': 1},
]

# Track server health and metrics
server_health = {server['id']: True for server in BACKEND_SERVERS}
server_metrics = {
    server['id']: {
        'total_requests': 0,
        'failed_requests': 0,
        'avg_response_time': 0,
    } for server in BACKEND_SERVERS
}
active_connections = defaultdict(int)
round_robin_index = 0
request_count = 0

# Statistics
stats = {
    'total_requests': 0,
    'successful_requests': 0,
    'failed_requests': 0,
    'start_time': time.time()
}

# Request history
recent_requests = []

def health_check_worker():
    """Background thread to continuously check backend server health"""
    global server_health
    while True:
        for server in BACKEND_SERVERS:
            try:
                response = requests.get(f"{server['url']}/health", timeout=2)
                if response.status_code == 200:
                    server_health[server['id']] = True
                else:
                    server_health[server['id']] = False
            except:
                server_health[server['id']] = False
        time.sleep(5)

def get_healthy_servers():
    """Return list of healthy backend servers"""
    return [server for server in BACKEND_SERVERS if server_health[server['id']]]

def round_robin_selection():
    """Round Robin Algorithm"""
    global round_robin_index
    healthy_servers = get_healthy_servers()
    if not healthy_servers:
        return None
    server = healthy_servers[round_robin_index % len(healthy_servers)]
    round_robin_index += 1
    return server

def least_connections_selection():
    """Least Connections Algorithm"""
    healthy_servers = get_healthy_servers()
    if not healthy_servers:
        return None
    return min(healthy_servers, key=lambda s: active_connections[s['id']])

def weighted_selection():
    """Weighted Algorithm"""
    global request_count
    healthy_servers = get_healthy_servers()
    if not healthy_servers:
        return None
    weighted_list = []
    for server in healthy_servers:
        weighted_list.extend([server] * server['weight'])
    if not weighted_list:
        return None
    server = weighted_list[request_count % len(weighted_list)]
    request_count += 1
    return server

def least_response_time_selection():
    """Least Response Time Algorithm"""
    healthy_servers = get_healthy_servers()
    if not healthy_servers:
        return None
    return min(healthy_servers, key=lambda s: server_metrics[s['id']]['avg_response_time'] or 0)

def select_backend_server():
    """Select backend server based on configured algorithm"""
    if ALGORITHM == 'round_robin':
        return round_robin_selection()
    elif ALGORITHM == 'least_connections':
        return least_connections_selection()
    elif ALGORITHM == 'weighted':
        return weighted_selection()
    elif ALGORITHM == 'least_response_time':
        return least_response_time_selection()
    else:
        return round_robin_selection()

@app.route('/api/process', methods=['GET', 'POST'])
def proxy_request():
    """Main endpoint - forwards requests to backend servers"""
    stats['total_requests'] += 1
    request_start = time.time()
    
    server = select_backend_server()
    
    if not server:
        stats['failed_requests'] += 1
        return jsonify({
            'error': 'No healthy backend servers available',
            'load_balancer': LB_ID
        }), 503
    
    active_connections[server['id']] += 1
    server_metrics[server['id']]['total_requests'] += 1
    
    try:
        backend_url = f"{server['url']}/api/process"
        
        if request.method == 'GET':
            response = requests.get(backend_url, timeout=5)
        else:
            response = requests.post(backend_url, json=request.get_json(), timeout=5)
        
        response_time = time.time() - request_start
        stats['successful_requests'] += 1
        
        # Update average response time
        current_avg = server_metrics[server['id']]['avg_response_time']
        server_metrics[server['id']]['avg_response_time'] = (current_avg * 0.8) + (response_time * 0.2)
        
        # Add to recent requests
        recent_requests.append({
            'timestamp': datetime.now().isoformat(),
            'server_id': server['id'],
            'response_time': round(response_time, 3),
            'status': 'success'
        })
        
        if len(recent_requests) > 100:
            recent_requests.pop(0)
        
        response_data = response.json()
        response_data['load_balancer_id'] = LB_ID
        response_data['algorithm'] = ALGORITHM
        
        active_connections[server['id']] -= 1
        
        return jsonify(response_data), response.status_code
    
    except Exception as e:
        active_connections[server['id']] -= 1
        stats['failed_requests'] += 1
        server_metrics[server['id']]['failed_requests'] += 1
        
        return jsonify({
            'error': str(e),
            'server': server['id'],
            'load_balancer': LB_ID
        }), 500

@app.route('/status', methods=['GET'])
def get_status():
    """Get load balancer status and backend health"""
    return jsonify({
        'load_balancer_id': LB_ID,
        'algorithm': ALGORITHM,
        'uptime': round(time.time() - stats['start_time'], 2),
        'statistics': stats,
        'backend_servers': [
            {
                'id': server['id'],
                'url': server['url'],
                'healthy': server_health[server['id']],
                'active_connections': active_connections[server['id']],
                'weight': server['weight'],
                'total_requests': server_metrics[server['id']]['total_requests'],
                'failed_requests': server_metrics[server['id']]['failed_requests'],
                'avg_response_time': round(server_metrics[server['id']]['avg_response_time'], 3)
            }
            for server in BACKEND_SERVERS
        ],
        'recent_requests': recent_requests[-20:]
    }), 200

@app.route('/health', methods=['GET'])
def health():
    """Load balancer health check"""
    return jsonify({
        'status': 'healthy',
        'load_balancer_id': LB_ID
    }), 200

@app.route('/algorithm', methods=['POST'])
def change_algorithm():
    """Change load balancing algorithm at runtime"""
    global ALGORITHM
    data = request.get_json() or {}
    new_algorithm = data.get('algorithm')
    
    valid_algorithms = ['round_robin', 'least_connections', 'weighted', 'least_response_time']
    
    if new_algorithm in valid_algorithms:
        ALGORITHM = new_algorithm
        return jsonify({
            'message': f'Algorithm changed to {new_algorithm}',
            'current': new_algorithm
        }), 200
    else:
        return jsonify({
            'error': 'Invalid algorithm',
            'valid_options': valid_algorithms
        }), 400

@app.route('/reset', methods=['POST'])
def reset_stats():
    """Reset all statistics"""
    global stats, recent_requests, server_metrics
    
    stats = {
        'total_requests': 0,
        'successful_requests': 0,
        'failed_requests': 0,
        'start_time': time.time()
    }
    
    recent_requests.clear()
    
    for server_id in server_metrics:
        server_metrics[server_id] = {
            'total_requests': 0,
            'failed_requests': 0,
            'avg_response_time': 0
        }
    
    return jsonify({'message': 'Statistics reset successfully'}), 200

if __name__ == '__main__':
    print("\n" + "="*70)
    print(f"  Load Balancer: {LB_ID}")
    print("="*70)
    print(f"  Port: {LB_PORT}")
    print(f"  Algorithm: {ALGORITHM}")
    print(f"  Backend Servers: {len(BACKEND_SERVERS)}")
    for server in BACKEND_SERVERS:
        print(f"    - {server['id']}: {server['url']} (weight: {server['weight']})")
    print("="*70 + "\n")
    
    health_thread = threading.Thread(target=health_check_worker, daemon=True)
    health_thread.start()
    
    app.run(host='0.0.0.0', port=LB_PORT, debug=False)