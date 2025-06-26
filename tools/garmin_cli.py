#!/usr/bin/env python3

import os
import sys
import json
import inspect
import logging
import readline  # noqa: F401
from dotenv import load_dotenv

# Add the parent directory to the path so we can import from src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.garmin.client import Garmin


def print_methods(garmin_client):
    """Print all available methods of the Garmin client."""
    methods = [
        method
        for method in dir(garmin_client)
        if callable(getattr(garmin_client, method)) and not method.startswith("_")
    ]

    print("\nAvailable Garmin methods:")
    print("=" * 40)
    for method in sorted(methods):
        method_obj = getattr(garmin_client, method)
        sig = inspect.signature(method_obj)
        print(f"{method}{sig}")
    print("=" * 40)


def parse_arguments(arg_string):
    """Parse command line arguments into args and kwargs."""
    if not arg_string.strip():
        return [], {}

    args = []
    kwargs = {}

    # Simple parsing - split by comma and check for = signs
    parts = [part.strip() for part in arg_string.split(",") if part.strip()]

    for part in parts:
        if "=" in part:
            key, value = part.split("=", 1)
            key = key.strip()
            value = value.strip()

            # Try to convert value to appropriate type
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]  # Remove quotes
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]  # Remove quotes
            elif value.lower() == "true":
                value = True
            elif value.lower() == "false":
                value = False
            elif value.lower() == "none":
                value = None
            elif value.isdigit():
                value = int(value)
            else:
                try:
                    value = float(value)
                except ValueError:
                    pass  # Keep as string

            kwargs[key] = value
        else:
            # Positional argument
            if part.startswith('"') and part.endswith('"'):
                part = part[1:-1]  # Remove quotes
            elif part.startswith("'") and part.endswith("'"):
                part = part[1:-1]  # Remove quotes
            elif part.lower() == "true":
                part = True
            elif part.lower() == "false":
                part = False
            elif part.lower() == "none":
                part = None
            elif part.isdigit():
                part = int(part)
            else:
                try:
                    part = float(part)
                except ValueError:
                    pass  # Keep as string

            args.append(part)

    return args, kwargs


def format_output(result):
    """Format the output for display."""
    if isinstance(result, (dict, list)):
        return json.dumps(result, indent=2, default=str)
    else:
        return str(result)


def main():
    # Configure logging to show debug messages
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    load_dotenv()
    email = os.getenv("GARMIN_EMAIL")
    password = os.getenv("GARMIN_PASSWORD")

    if not all([email, password]):
        print("Error: Missing required environment variables.")
        print("Please set GARMIN_EMAIL and GARMIN_PASSWORD in your .env file.")
        sys.exit(1)

    assert email is not None
    assert password is not None

    print("Connecting to Garmin Connect...")
    try:
        with Garmin(
            email=email, password=password, return_on_mfa=True
        ) as garmin_client:
            print(f"✓ Connected as {garmin_client.get_full_name()}")

            print("\n=== Garmin Connect CLI ===")
            print("Type 'help' to see available methods")
            print("Type 'quit' or 'exit' to quit")
            print("Usage: method_name arg1, arg2, kwarg1=value1")
            print("Example: get_user_summary '2024-06-14'")
            print("Example: get_activities start=0, limit=5\n")

            while True:
                try:
                    user_input = input("garmin> ").strip()

                    if user_input.lower() in ["quit", "exit"]:
                        break

                    if user_input.lower() == "help":
                        print_methods(garmin_client)
                        continue

                    if not user_input:
                        continue

                    # Parse method name and arguments
                    if "(" in user_input and user_input.endswith(")"):
                        # Handle method(args) format
                        method_name = user_input.split("(")[0].strip()
                        args_part = user_input[user_input.find("(") + 1 : -1]
                    else:
                        # Handle method args format
                        parts = user_input.split(" ", 1)
                        method_name = parts[0]
                        args_part = parts[1] if len(parts) > 1 else ""

                    if not hasattr(garmin_client, method_name):
                        print(
                            f"Error: Method '{method_name}' not found. Type 'help' to see available methods."
                        )
                        continue

                    method = getattr(garmin_client, method_name)
                    if not callable(method):
                        print(f"Error: '{method_name}' is not a method.")
                        continue

                    # Parse arguments
                    args, kwargs = parse_arguments(args_part)

                    print(
                        f"Calling {method_name}({', '.join(map(str, args))}{', ' if args and kwargs else ''}{', '.join(f'{k}={v}' for k, v in kwargs.items())})..."
                    )

                    # Call the method
                    result = method(*args, **kwargs)

                    print("Result:")
                    print(format_output(result))

                except KeyboardInterrupt:
                    print("\nUse 'quit' or 'exit' to exit.")
                except Exception as e:
                    print(f"Error: {e}")

    except Exception as e:
        print(f"Failed to connect to Garmin: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
