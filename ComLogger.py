import serial
import time
import argparse
import signal
import sys

# Global variable to keep track of the running state
running = True

def signal_handler(sig, frame):
    global running
    print("\nGracefully shutting down the script...")
    running = False

def log_serial_data(com_port, baud_rate):
    global running
    try:
        # Open the serial connection
        with serial.Serial(com_port, baud_rate, timeout=1) as ser:
            print(f"Logging data from {com_port} at {baud_rate} baud rate")
            
            # Create or append to a log file with a timestamp
            log_file_name = f"serial_log_{time.strftime('%Y%m%d_%H%M%S')}.txt"
            with open(log_file_name, 'a') as log_file:
                
                while running:
                    # Read data from the serial port
                    if ser.in_waiting > 0:
                        data = ser.readline().decode('utf-8').strip()
                        
                        # Log the data
                        print(f"Data: {data}")
                        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {data}\n")
                        
                        # Flush the file to ensure it's written to disk
                        log_file.flush()

    except serial.SerialException as e:
        print(f"Error opening or reading from serial port: {e}")
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt detected. Exiting...")
    finally:
        print("Serial connection closed. Exiting program.")

if __name__ == "__main__":
    # Set up argument parsing with flags -s for COM port and -b for baud rate
    parser = argparse.ArgumentParser(description="Log data from a serial port.")
    parser.add_argument("-s", "--serial", required=True, help="COM port (e.g., COM3 or /dev/ttyUSB0)")
    parser.add_argument("-b", "--baud", type=int, required=True, help="Baud rate (e.g., 9600)")
    
    # Parse the command-line arguments
    args = parser.parse_args()
    
    # Register the signal handler to gracefully handle Ctrl+C (SIGINT)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Call the log_serial_data function with parsed arguments
    log_serial_data(args.serial, args.baud)
