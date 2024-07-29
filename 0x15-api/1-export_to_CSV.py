#!/usr/bin/python3
"""Retrieves employee TODO list progress and exports it to JSON."""

import json
import requests
import sys


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./2-export_to_JSON.py <employee_id>")
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
        base_url = "https://jsonplaceholder.typicode.com"

        # Fetch user data
        user_response = requests.get(f"{base_url}/users/{employee_id}")
        user_data = user_response.json()
        username = user_data.get("username", "Unknown")

        # Fetch TODO list data for the user
        todos_response = requests.get(f"{base_url}/todos?userId={employee_id}")
        todos_data = todos_response.json()

        # Create a list of task dictionaries
        tasks = []
        for task in todos_data:
            task_dict = {
                "task": task.get("title"),
                "completed": task.get("completed"),
                "username": username
            }
            tasks.append(task_dict)

        # Create the JSON structure
        data = {str(employee_id): tasks}

        # Export to JSON file
        filename = f"{employee_id}.json"
        with open(filename, 'w') as jsonfile:
            json.dump(data, jsonfile)

    except (requests.exceptions.RequestException, ValueError):
        print(f"Error: Failed to retrieve data for employee ID {employee_id}")
        sys.exit(1)
