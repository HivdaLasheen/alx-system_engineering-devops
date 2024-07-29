#!/usr/bin/python3
"""Retrieves all employee TODO lists and exports them to a JSON file."""

import json
import requests


if __name__ == "__main__":
    base_url = "https://jsonplaceholder.typicode.com"
    all_tasks = {}

    try:
        # Fetch all users
        users_response = requests.get(f"{base_url}/users")
        users_data = users_response.json()

        # Iterate over all users
        for user in users_data:
            user_id = user.get("id")
            username = user.get("username")

            # Fetch TODOs for the current user
            todos_response = requests.get(f"{base_url}/todos?userId={user_id}")
            todos_data = todos_response.json()

            # Create a list of tasks for the current user
            user_tasks = []
            for task in todos_data:
                task_dict = {
                    "username": username,
                    "task": task.get("title"),
                    "completed": task.get("completed")
                }
                user_tasks.append(task_dict)

            # Add the user's tasks to the overall dictionary
            all_tasks[str(user_id)] = user_tasks

        # Export all tasks to JSON file
        with open("todo_all_employees.json", "w") as jsonfile:
            json.dump(all_tasks, jsonfile)

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
