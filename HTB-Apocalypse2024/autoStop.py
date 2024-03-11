from colorama import Fore
import socket

# Define the IP address and port to connect to
IP_ADDRESS = "94.237.53.58"
PORT = 47075

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set a larger socket buffer size
s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8192)

# Connect to the netcat session
s.connect((IP_ADDRESS, PORT))

# Set a timeout for the socket (e.g., 20 seconds)
s.settimeout(3)

# Function to determine the correct response for each scenario
def get_response(scenarios):
    response = []
    for scenario in scenarios:
        if scenario == "PHREAK":
            response.append("DROP")
        elif scenario == "GORGE":
            response.append("STOP")
        elif scenario == "FIRE":
            response.append("ROLL")
    return "-".join(response)

# Flag to indicate if the game has started
game_started = False

# Counter for prompts and responses
counter = 0

# Main loop to continuously read input and respond
while True:
    try:
        data = s.recv(1024).decode("utf-8")
        if not data:
            break
        print(data.strip())  # Print the prompt
        counter += 1  # Increment the counter for each prompt
        print("Prompt/Response Counter:", counter)
        if "Are you ready? (y/n)" in data and not game_started:
            s.send(b"y\n")  # Respond 'y' to start the game
            game_started = True  # Set the flag to indicate that the game has started
        elif game_started and "What do you do?" in data:
            # Split the received data by lines
            lines = data.strip().split("\n")
            print("Received lines:", lines)
            
            # Check if the last line contains only the prompt
            if len(lines) == 1 and "What do you do?" in lines[0]:
                # If so, ask the user locally for the response
                user_response = input("---------->  ")
                print("Local response:", user_response.upper())
                draft = user_response.upper().split(" ")
                respArray = []
                for i in draft:
                    respArray.append(i)
                user_final_response = "-".join(respArray)
                try:
                    s.sendall((user_final_response + "\n").encode("utf-8"))  # Send the user's response
                except socket.error as e:
                    print("Error occurred during transmission:", e)
                    # Implement retransmission logic here if necessary
            else:
                # If the last line doesn't contain only the prompt, process it as usual
                
                # Check if the last line contains the prompt
                if "What do you do?" in lines[-1]:
                    # If so, the prompt data is in the line before the last
                    prompt_data = lines[-2]
                    #print("Prompt data:", prompt_data)
                    
                else:
                    # If the last line doesn't contain the prompt, use it as the prompt data
                    prompt_data = lines[-1]
                    #print("Prompt data:", prompt_data)
                  
                
                # Extract scenario sequence from the prompt data
                scenario_sequence = prompt_data.split(", ")
                #print("Scenario_sequence:", scenario_sequence)
                
                # Get the response based on the scenario sequence
                response = get_response(scenario_sequence)
                print(f"{Fore.YELLOW}{response}{Fore.WHITE}")  # Print the response
                try:
                    s.sendall((response + "\n").encode("utf-8"))  # Send response with newline
                except socket.error as e:
                    print("Error occurred during transmission:", e)
                    # Implement retransmission logic here if necessary
    except socket.timeout:
        print("Timeout occurred. Exiting the script.")
        break

# Close the connection
s.close()

