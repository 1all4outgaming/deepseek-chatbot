import os
import subprocess

# Function to check if SSH key exists
def check_ssh_key():
    ssh_dir = os.path.expanduser('~/.ssh')
    private_key = os.path.join(ssh_dir, 'id_rsa')
    
    # Check if private key already exists
    if os.path.exists(private_key):
        print("SSH key already exists. Skipping generation.")
        return private_key
    else:
        return generate_ssh_key()

# Function to generate an SSH key
def generate_ssh_key():
    ssh_dir = os.path.expanduser('~/.ssh')
    # Ensure the .ssh directory exists
    os.makedirs(ssh_dir, exist_ok=True)
    
    private_key_path = os.path.join(ssh_dir, 'id_rsa')
    
    # Run the ssh-keygen command to generate a new SSH key pair
    print("Generating SSH key...")
    subprocess.run(['ssh-keygen', '-t', 'rsa', '-b', '2048', '-f', private_key_path, '-N', ''], check=True)
    
    print(f"SSH key generated at {private_key_path}")
    return private_key_path

# Function to run the SSH tunneling command (on port 11434)
def run_ssh_tunnel():
    print("Starting the SSH tunnel command on port 11434...")
    # Command to establish SSH tunnel to localhost.run, hosting on port 11434
    subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', os.path.expanduser('~/.ssh/id_rsa'), '-R', '80:localhost:11434', 'localhost.run'], check=True)

if __name__ == "__main__":
    # Step 1: Check or generate SSH key
    check_ssh_key()
    
    # Step 2: Run the SSH tunnel command to host on port 11434
    run_ssh_tunnel()
