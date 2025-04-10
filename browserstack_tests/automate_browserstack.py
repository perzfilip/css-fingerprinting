import json
import os
import random
import subprocess
from datetime import datetime
from pprint import pprint

import yaml
from time import sleep
import config


def generate_config(platforms, output_file="browserstack.yml", build_name="Autotest"):
    """Generate a YAML config file with the given platforms"""
    data = {
        "userName": config.BROWSERSTACK_USERNAME,
        "accessKey": config.BROWSERSTACK_ACCESS_KEY,
        "platforms": platforms,
        "browserstackLocal": True,
        "buildName": build_name,
        "projectName": "CSS Fingerprinting",
        "buildIdentifier": "#${BUILD_NUMBER}",
        "source": "python-browserstack:sample-sdk:v1.0",
        "debug": False,
        "networkLogs": False,
        "consoleLogs": "errors",
        "idleTimeout": 120
    }

    with open(output_file, "w") as file:
        yaml.dump(data, file, default_flow_style=False)

    print(f"YAML file '{output_file}' generated successfully.")


def run_tests():
    """Run the BrowserStack tests and wait for completion"""
    cmd = "browserstack-sdk python browserstack_tests.py"
    process = subprocess.Popen(cmd, shell=True)
    process.wait()
    return process.returncode


def chunk_platforms(platforms, chunk_size=6):
    """Split platforms into chunks of specified size"""
    for i in range(0, len(platforms), chunk_size):
        yield platforms[i:i + chunk_size]


def get_random_platforms(number_of_platforms, file='browsers_cleaned_3.json'):
    try:
        with open(file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            random_platforms = random.sample(data, number_of_platforms)

            for platform in random_platforms:
                keys_to_remove = []
                for key, value in platform.items():
                    if value is None:
                        keys_to_remove.append(key)
                for key in keys_to_remove:
                    del platform[key]

            return random_platforms
    except Exception as e:
        print(f"Error reading JSON file: {e}")


def main(number_of_platforms=100):
    print("Starting automated BrowserStack test execution")

    # check if the webpage is running
    try:
        response = subprocess.check_output(["curl", "-Is", "http://localhost:5000"])
        if b"200 OK" not in response:
            raise Exception("Webpage is not running")
    except subprocess.CalledProcessError:
        print("Error: Webpage is not running. Please start the local server.")
        return

    # choose randomly given number of platforms from the scripts/outputs/browsres.json file
    platforms = get_random_platforms(number_of_platforms)

    # Split all platforms into chunks of 6
    platform_chunks = list(chunk_platforms(platforms, 6))

    test_name = f"Autotest {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    for i, chunk in enumerate(platform_chunks, 1):
        print(f"\nRunning batch {i} of {len(platform_chunks)}")
        print("Platforms in this batch:")
        pprint(chunk)

        # Generate and save config
        generate_config(chunk, build_name=test_name)

        # Run tests
        print("Starting test execution...")

        return_code = run_tests()

        if return_code != 0:
            print(f"Warning: Test batch {i} returned non-zero exit code: {return_code}")

        print(f"Completed batch {i}")

        # Small delay between batches
        if i < len(platform_chunks):
            print("Preparing next batch...")
            sleep(5)

    print("\nAll test batches completed!")


if __name__ == "__main__":
    main(1000)
