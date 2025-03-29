import os
import subprocess
import yaml
from time import sleep

# Configuration
BASE_CONFIG = {
    "browserstack": {
        "user": "<your_username>",
        "key": "<your_access_key>",
        "build": "Automated Test Suite",
        "project": "Browser Compatibility"
    },
    "baseUrl": "http://your-base-url.com",
    "run_settings": {
        "cypress": {
            "config_file": "cypress.json",
            "parallels": 6,  # Maximum parallel tests
            "npm_dependencies": {
                "cypress": "9.7.0",
                "cypress-xpath": "^1.6.2"
            }
        }
    }
}

# Define all platforms you want to test
ALL_PLATFORMS = [
    {"os": "Windows", "os_version": "10", "browser": "Chrome", "browser_version": "latest"},
    {"os": "Windows", "os_version": "10", "browser": "Firefox", "browser_version": "latest"},
    {"os": "Windows", "os_version": "10", "browser": "Edge", "browser_version": "latest"},
    {"os": "Windows", "os_version": "11", "browser": "Chrome", "browser_version": "latest"},
    {"os": "Windows", "os_version": "11", "browser": "Firefox", "browser_version": "latest"},
    {"os": "Windows", "os_version": "11", "browser": "Edge", "browser_version": "latest"},
    {"os": "OS X", "os_version": "Ventura", "browser": "Chrome", "browser_version": "latest"},
    {"os": "OS X", "os_version": "Ventura", "browser": "Firefox", "browser_version": "latest"},
    {"os": "OS X", "os_version": "Ventura", "browser": "Safari", "browser_version": "latest"},
    {"os": "OS X", "os_version": "Monterey", "browser": "Chrome", "browser_version": "latest"},
    {"os": "OS X", "os_version": "Monterey", "browser": "Firefox", "browser_version": "latest"},
    {"os": "OS X", "os_version": "Monterey", "browser": "Safari", "browser_version": "latest"},
    # Add more platforms as needed
]


def generate_config(platforms):
    """Generate a YAML config file with the given platforms"""
    config = BASE_CONFIG.copy()
    config["browserstack"]["run_settings"]["cypress"]["browsers"] = platforms
    return config


def save_config(config, filename="browserstack.yml"):
    """Save the config to a YAML file"""
    with open(filename, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)


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


def main():
    print("Starting automated BrowserStack test execution")

    # Split all platforms into chunks of 6
    platform_chunks = list(chunk_platforms(ALL_PLATFORMS, 6))

    for i, chunk in enumerate(platform_chunks, 1):
        print(f"\nRunning batch {i} of {len(platform_chunks)}")
        print("Platforms in this batch:")
        for platform in chunk:
            print(f"- {platform['os']} {platform['os_version']} - {platform['browser']} {platform['browser_version']}")

        # Generate and save config
        config = generate_config(chunk)
        save_config(config)

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
    main()