import requests
import threading
import signal
import sys
from urllib.parse import urljoin

found_directories = []
total_directories = 0
scanned_count = 0


def check_directory(base_url, directory):
    url = urljoin(base_url, directory)
    response = requests.get(url)
    if response.status_code == 200:
        print(f"[+] Directory found: {url}")
        return url
    return None


def scan_directories(base_url, directories):
    global scanned_count
    global found_directories
    total = len(directories)

    threads = []
    for directory in directories:
        thread = threading.Thread(
            target=check_directory, args=(base_url, directory))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print()
    return found_directories


def read_directories_from_file(filename):
    try:
        with open(filename, 'r') as file:
            directories = [line.strip()
                           for line in file.readlines() if line.strip()]
            return directories
    except FileNotFoundError:
        print(f"File {filename} tidak ditemukan.")
        return []


def signal_handler(sig, frame):
    print("\nScanning interrupted.")
    print(f"Total directories scanned: {scanned_count}")
    print(f"Directories found: {len(found_directories)}")

    with open('found_directories.txt', 'w') as f:
        for directory in found_directories:
            f.write(f"{directory}\n")

    print("Found directories saved to 'found_directories.txt'.")
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    base_url = input("Masukkan URL website yang ingin di-scan: ")

    directories = read_directories_from_file('dirWebList.txt')
    total_directories = len(directories)

    print(f"Scanning direktori pada {base_url}...")
    found_dirs = scan_directories(base_url, directories)

    print("\nHasil scan:")
    for dir in found_dirs:
        print(dir)

    print(f"\nTotal direktori ditemukan: {len(found_dirs)}")

    with open('found_directories.txt', 'w') as f:
        for directory in found_dirs:
            f.write(f"{directory}\n")

    print("Found directories saved to 'found_directories.txt'.")
