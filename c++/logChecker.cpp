
#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>

using namespace std;

const string LOG_FILE_NAME = "logs.csv";

// Function to check logs for matches
bool checkLogs(const string& email, const string& password, const string& breachDate) {
    ifstream logFile(LOG_FILE_NAME);

    if (logFile.is_open()) {
        string line;

        // Skip the header line
        getline(logFile, line);

        while (getline(logFile, line)) {
            istringstream iss(line);
            string storedEmail, storedPassword, storedBreachDate;

            if (getline(iss, storedEmail, ',') &&
                getline(iss, storedPassword, ',') &&
                getline(iss, storedBreachDate, ',')) {
                // Compare stored values with user inputs
                if (storedEmail == email && storedPassword == password && storedBreachDate == breachDate) {
                    cout << "Match found in logs.csv.\n";
                    return true;
                }
            }
        }

        logFile.close();
    }
    else {
        cout << "No logs found or error opening the log file.\n";
    }

    cout << "No match found in logs.csv.\n";
    return false;
}

// Function to store user inputs in a CSV file
void storeInLogFile(const string& email, const string& password, const string& breachDate) {
    ofstream logFile(LOG_FILE_NAME, ios::app); // Open the file in append mode

    if (logFile.is_open()) {
        // Write data to the CSV file
        logFile << email << "," << password << "," << breachDate << "\n";
        logFile.close();
        cout << "Data stored successfully in logs.csv.\n";
    }
    else {
        cout << "Error opening the log file.\n";
    }
}

int main() {
    while (true) {
        // User inputs
        string email, password, breachDate;

        // Get user inputs
        cout << "Enter Email (or enter 'exit' to exit): ";
        getline(cin, email);

        if (email == "exit") {
            break; // Exit the program if the user enters 'exit'
        }

        cout << "Enter Password: ";
        getline(cin, password);

        cout << "Enter Breach Date (YYYY-MM-dd format): ";
        getline(cin, breachDate);

        // Display user inputs
        cout << "You entered:\n";
        cout << "Email: " << email << "\n";
        cout << "Password: " << password << "\n";
        cout << "Breach Date: " << breachDate << "\n";

        // Check if the input exists in the logs, if not, store it
        if (!checkLogs(email, password, breachDate)) {
            storeInLogFile(email, password, breachDate);
        }
    }

    cout << "Exiting the program.\n";

    return 0;
}
