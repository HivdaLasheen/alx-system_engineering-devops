#!/usr/bin/python3
"""Retrieves employee TODO list progress from a REST API."""

import requests
import sys


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./0-gather_data_from_an_API.py <employee_id>")
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
        base_url = "https://jsonplaceholder.typicode.com"

        # Fetch user data
        user_response = requests.get(f"{base_url}/users/{employee_id}")
        user_data = user_response.json()
        employee_name = user_data.get("name", "Unknown")

        # Fetch TODO list data for the user
        todos_response = requests.get(f"{base_url}/todos?userId={employee_id}")
        todos_data = todos_response.json()

        # Calculate task completion
        completed_tasks = [task for task in todos_data if task.get("completed")]
        num_completed = len(completed_tasks)
        total_tasks = len(todos_data)

        # Display summary
        print(f"Employee {employee_name} is done with tasks ({num_completed}/{total_tasks}):")

        # Display completed task titles
        for task in completed_tasks:
            print(f"\t {task.get('title')}")
    except (requests.exceptions.RequestException, ValueError):
        print(f"Error: Failed to retrieve data for employee ID {employee_id}")
        sys.exit(1)
