"""
Test Client - Sends multiple requests to test the load balancer
"""
import requests
import time
from collections import Counter
import concurrent.futures

LOAD_BALANCER_URL = 'http://localhost:8001'
NUM_REQUESTS = 20

def send_request(request_num):
    """Send a single request to the load balancer"""
    try:
        start_time = time.time()
        response = requests.get(f'{LOAD_BALANCER_URL}/api/process', timeout=10)
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            return {
                'success': True,
                'server_id': data.get('server_id'),
                'response_time': round(elapsed_time, 3),
                'request_num': request_num
            }
        else:
            return {
                'success': False,
                'error': 'Non-200 status',
                'request_num': request_num
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'request_num': request_num
        }

def test_load_balancer():
    """Run load balancer tests"""
    print("\n" + "="*60)
    print(" DISTRIBUTED LOAD BALANCER - TEST SUITE")
    print("="*60)
    
    # Check load balancer status
    try:
        status_response = requests.get(f'{LOAD_BALANCER_URL}/status', timeout=5)
        if status_response.status_code == 200:
            status = status_response.json()
            print(f"\n✓ Load Balancer: {status['load_balancer_id']}")
            print(f"✓ Algorithm: {status['algorithm']}")
            print(f"✓ Uptime: {status['uptime']} seconds")
            print(f"\nBackend Servers:")
            for server in status['backend_servers']:
                health_icon = "✓" if server['healthy'] else "✗"
                print(f"  {health_icon} {server['id']} - {server['url']} (Weight: {server['weight']})")
        else:
            print("\n✗ Load balancer not responding properly")
            return
    except Exception as e:
        print(f"\n✗ Error connecting to load balancer: {e}")
        return
    
    print(f"\n" + "-"*60)
    print(f" TEST 1: Sequential Requests ({NUM_REQUESTS} requests)")
    print("-"*60)
    
    results = []
    print("\nSending requests...")
    
    for i in range(NUM_REQUESTS):
        result = send_request(i + 1)
        results.append(result)
        
        if result['success']:
            print(f"Request {i+1:2d}: {result['server_id']:12s} | Response Time: {result['response_time']:.3f}s")
        else:
            print(f"Request {i+1:2d}: FAILED - {result.get('error', 'Unknown error')}")
        
        time.sleep(0.1)  # Small delay between requests
    
    # Analyze results
    print(f"\n" + "="*60)
    print(" TEST RESULTS")
    print("="*60)
    
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print(f"\nSuccess Rate: {len(successful)}/{NUM_REQUESTS} ({len(successful)/NUM_REQUESTS*100:.1f}%)")
    print(f"Failed Requests: {len(failed)}")
    
    if successful:
        # Distribution analysis
        server_distribution = Counter(r['server_id'] for r in successful)
        print(f"\nLoad Distribution:")
        for server_id, count in sorted(server_distribution.items()):
            percentage = (count / len(successful)) * 100
            bar = "█" * int(percentage / 2)
            print(f"  {server_id:12s}: {count:2d} requests ({percentage:5.1f}%) {bar}")
        
        # Response time analysis
        response_times = [r['response_time'] for r in successful]
        avg_response_time = sum(response_times) / len(response_times)
        min_response_time = min(response_times)
        max_response_time = max(response_times)
        
        print(f"\nResponse Time Statistics:")
        print(f"  Average: {avg_response_time:.3f}s")
        print(f"  Minimum: {min_response_time:.3f}s")
        print(f"  Maximum: {max_response_time:.3f}s")
    
    # Concurrent test
    print(f"\n" + "-"*60)
    print(f" TEST 2: Concurrent Requests (10 simultaneous)")
    print("-"*60)
    
    print("\nSending concurrent requests...")
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        concurrent_results = list(executor.map(send_request, range(100, 110)))
    
    total_time = time.time() - start_time
    
    successful_concurrent = [r for r in concurrent_results if r['success']]
    print(f"\nConcurrent Test Results:")
    print(f"  Success Rate: {len(successful_concurrent)}/10")
    print(f"  Total Time: {total_time:.3f}s")
    
    if successful_concurrent:
        server_dist = Counter(r['server_id'] for r in successful_concurrent)
        print(f"  Distribution:")
        for server_id, count in sorted(server_dist.items()):
            print(f"    {server_id}: {count} requests")
    
    # Final status check
    print(f"\n" + "-"*60)
    print(" FINAL STATUS CHECK")
    print("-"*60)
    
    try:
        final_status = requests.get(f'{LOAD_BALANCER_URL}/status', timeout=5).json()
        print(f"\nLoad Balancer Statistics:")
        print(f"  Total Requests: {final_status['statistics']['total_requests']}")
        print(f"  Successful: {final_status['statistics']['successful_requests']}")
        print(f"  Failed: {final_status['statistics']['failed_requests']}")
    except Exception as e:
        print(f"Could not retrieve final status: {e}")
    
    print(f"\n" + "="*60)
    print(" TESTING COMPLETED")
    print("="*60 + "\n")

if __name__ == '__main__':
    test_load_balancer()