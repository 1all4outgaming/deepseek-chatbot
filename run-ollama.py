import subprocess
import os
import time

def install_and_serve_ollama():
    """Installs and starts Ollama using the provided command."""

    try:
        # Run the installation command
        install_process = subprocess.Popen(
            ["curl", "-fsSL", "https://ollama.com/install.sh"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        install_script = install_process.communicate()[0]  # Get the script content

        # Execute the downloaded script using bash.  shell=True is generally discouraged
        # for security reasons, but in this specific case, we're piping the output
        # of curl directly to sh, which is effectively what the original command did.
        # It's important to understand the risks of executing arbitrary scripts.
        install_execution = subprocess.Popen(
            ["sh"],  # Use sh to execute the script
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        install_execution.communicate(input=install_script)

        if install_execution.returncode != 0:
            print(f"Ollama installation failed:\n{install_execution.stderr.decode()}")
            return  # Exit if installation fails

        print("Ollama installation successful.")

        # Start Ollama serve in the background.
        # Using shell=True here is acceptable because we are running a single, 
        # well-defined command and not processing user input.
        serve_process = subprocess.Popen(
            "ollama serve",
            shell=True, # Necessary for backgrounding with &
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        print("Ollama server started in the background.")


        # Option 1:  Wait a bit to let the server start (simplest but not most robust)
        time.sleep(5)  # Adjust as needed.  5 seconds might not be enough on slower machines.
        print("Assuming Ollama server is running.  Check logs if you have issues.")

        # Option 2 (More robust): Check if the server is running (more complex).
        # This involves checking the ollama process.  We can improve this
        # by checking if the port is open, but that's more involved.

        # Example using ps (might not be available on all systems).
        # You'd need to parse the output to find the ollama process.
        # You can improve this by using `pgrep` instead of `ps aux | grep`
        # ps_check = subprocess.run("ps aux | grep ollama", shell=True, capture_output=True, text=True)
        # print(ps_check.stdout) 

        # A more robust solution would involve checking the port that ollama uses.

    except FileNotFoundError:
        print("Error: curl or sh not found. Make sure they are installed.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    install_and_serve_ollama()
