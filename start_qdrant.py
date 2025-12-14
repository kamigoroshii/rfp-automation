"""
Start Qdrant using Docker if not already running
"""
import subprocess
import socket
import time
import sys

def is_port_open(host='localhost', port=6333):
    """Check if Qdrant port is open"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def check_docker():
    """Check if Docker is available"""
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def start_qdrant():
    """Start Qdrant using Docker"""
    print("🔍 Checking Qdrant status...")
    
    # Check if already running
    if is_port_open():
        print("✅ Qdrant is already running on port 6333")
        return True
    
    print("⚠️  Qdrant is not running")
    
    # Check Docker
    if not check_docker():
        print("\n❌ Docker is not installed or not in PATH")
        print("\nTo use RAG features, you need to:")
        print("1. Install Docker Desktop: https://www.docker.com/products/docker-desktop")
        print("2. Start Docker Desktop")
        print("3. Run this script again")
        return False
    
    print("\n🚀 Starting Qdrant with Docker...")
    print("Command: docker run -d -p 6333:6333 -v ./qdrant_storage:/qdrant/storage qdrant/qdrant")
    
    try:
        # Check if container already exists
        check_cmd = ['docker', 'ps', '-a', '--filter', 'name=qdrant', '--format', '{{.Names}}']
        result = subprocess.run(check_cmd, capture_output=True, text=True)
        
        if 'qdrant' in result.stdout:
            print("📦 Qdrant container exists, starting it...")
            subprocess.run(['docker', 'start', 'qdrant'], check=True)
        else:
            print("📦 Creating new Qdrant container...")
            subprocess.run([
                'docker', 'run', '-d',
                '--name', 'qdrant',
                '-p', '6333:6333',
                '-v', './qdrant_storage:/qdrant/storage',
                'qdrant/qdrant'
            ], check=True)
        
        # Wait for Qdrant to start
        print("\n⏳ Waiting for Qdrant to be ready...")
        for i in range(30):
            if is_port_open():
                print(f"\n✅ Qdrant is now running on http://localhost:6333")
                print("📊 Dashboard: http://localhost:6333/dashboard")
                return True
            time.sleep(1)
            print(".", end="", flush=True)
        
        print("\n⚠️  Qdrant started but not responding on port 6333")
        print("Check Docker logs: docker logs qdrant")
        return False
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error starting Qdrant: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = start_qdrant()
    sys.exit(0 if success else 1)
