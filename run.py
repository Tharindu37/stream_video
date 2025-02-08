from pyngrok import ngrok
import subprocess
import time
import sys

# Function to start ngrok and Flask server
def start_ngrok_flask():
    print("Starting ngrok and Flask server...")

    # Start ngrok and get the public URL
    print("Starting ngrok...")
    try:
        # Start ngrok on port 5000 (Flask's default port)
        public_url = ngrok.connect(addr="5000", proto="http", bind_tls=True)
        print(f"Ngrok URL: {public_url}")
    except Exception as e:
        print(f"Failed to start ngrok: {e}")
        return None, None, None

    # Start Flask server
    print("Starting Flask server...")
    try:
        flask_process = subprocess.Popen(["python", "main.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        print(f"Failed to start Flask server: {e}")
        ngrok.kill()  # Stop ngrok if Flask fails to start
        return None, None, None

    print("Flask server and ngrok are up and running.")
    return flask_process, public_url

# Main function to run everything
if __name__ == "__main__":
    # Start ngrok and Flask
    flask_process, public_url = start_ngrok_flask()

    if public_url is not None:
        try:
            while True:
                # Continuously print the current ngrok URL
                print(f"Current ngrok URL: {public_url}")

                # Wait for some time before checking again (e.g., every 5 seconds)
                time.sleep(5)
        except KeyboardInterrupt:
            print("Stopping Flask and ngrok...")
            # Terminate the Flask process and stop ngrok
            flask_process.terminate()
            ngrok.kill()