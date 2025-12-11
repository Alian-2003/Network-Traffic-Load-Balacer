"""
Enhanced Backend Server - Handles incoming requests from the load balancer
Features: Health checks, detailed metrics, configurable response times
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import time
import random
import logging
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for dashboard

# Server configuration from environment variables
SERVER_ID = os.getenv('SERVER_ID', 'backend_default')
SERVER_PORT = int(os.getenv('SERVER_PORT', 5001))
RESPONSE_DELAY = float(os.getenv('RESPONSE_DELAY', 0.1))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Track server statistics
stats = {
    'requests_handled': 0,
    'start_time': time.time(),
    'total_processing_time': 0,
    'errors': 0,
    'last_request_time': None
}

# Request history (keep last 100)
request_history = []

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for load balancer monitoring"""
    return jsonify({
        'status': 'healthy',
        'server_id': SERVER_ID,
        'port': SERVER_PORT,
        'uptime': round(time.time() - stats['start_time'], 2),
        'requests_handled': stats['requests_handled'],
        'cpu_load': random.randint(10, 90),  # Simulated CPU load
        'memory_usage': random.randint(30, 80),  # Simulated memory usage
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/process', methods=['GET', 'POST'])
def process_request():
    """Main endpoint to process incoming requests"""
    start_time = time.time()
    stats['requests_handled'] += 1
    
    try:
        # Simulate processing time with slight variation
        processing_time = random.uniform(RESPONSE_DELAY, RESPONSE_DELAY + 0.2)
        time.sleep(processing_time)
        
        # Get request data if POST
        request_data = None
        if request.method == 'POST':
            request_data = request.get_json() or {}
        
        response_time = time.time() - start_time
        stats['total_processing_time'] += response_time
        stats['last_request_time'] = datetime.now().isoformat()
        
        # Add to history
        request_history.append({
            'request_number': stats['requests_handled'],
            'timestamp': stats['last_request_time'],
            'processing_time': round(response_time, 3),
            'method': request.method
        })
        
        # Keep only last 100 requests
        if len(request_history) > 100:
            request_history.pop(0)
        
        logger.info(f"Processed request #{stats['requests_handled']} in {response_time:.3f}s")
        
        return jsonify({
            'message': 'Request processed successfully',
            'server_id': SERVER_ID,
            'server_port': SERVER_PORT,
            'request_number': stats['requests_handled'],
            'processing_time': round(response_time, 3),
            'timestamp': stats['last_request_time'],
            'method': request.method,
            'request_data': request_data
        }), 200
        
    except Exception as e:
        stats['errors'] += 1
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'server_id': SERVER_ID,
            'details': str(e)
        }), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get detailed server statistics"""
    uptime = time.time() - stats['start_time']
    avg_processing_time = (stats['total_processing_time'] / stats['requests_handled'] 
                          if stats['requests_handled'] > 0 else 0)
    
    return jsonify({
        'server_id': SERVER_ID,
        'port': SERVER_PORT,
        'uptime': round(uptime, 2),
        'total_requests': stats['requests_handled'],
        'errors': stats['errors'],
        'avg_processing_time': round(avg_processing_time, 3),
        'requests_per_second': round(stats['requests_handled'] / uptime, 2) if uptime > 0 else 0,
        'last_request': stats['last_request_time'],
        'recent_requests': request_history[-10:]  # Last 10 requests
    }), 200

@app.route('/reset', methods=['POST'])
def reset_stats():
    """Reset server statistics"""
    stats['requests_handled'] = 0
    stats['total_processing_time'] = 0
    stats['errors'] = 0
    stats['start_time'] = time.time()
    stats['last_request_time'] = None
    request_history.clear()
    
    logger.info("Statistics reset")
    return jsonify({'message': 'Statistics reset successfully'}), 200

@app.route('/simulate-load', methods=['POST'])
def simulate_load():
    """Simulate high load on the server"""
    data = request.get_json() or {}
    duration = data.get('duration', 5)  # seconds
    
    start = time.time()
    while time.time() - start < duration:
        # Simulate CPU work
        _ = sum(i**2 for i in range(10000))
    
    return jsonify({
        'message': f'Simulated high load for {duration} seconds',
        'server_id': SERVER_ID
    }), 200

if __name__ == '__main__':
    print("\n" + "="*60)
    print(f"  Enhanced Backend Server: {SERVER_ID}")
    print("="*60)
    print(f"  Port: {SERVER_PORT}")
    print(f"  Response Delay: {RESPONSE_DELAY}s")
    print(f"  Starting at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=SERVER_PORT, debug=False)