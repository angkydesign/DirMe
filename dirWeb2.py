import requests
from urllib.parse import urljoin
import concurrent.futures


def check_directory(base_url, directory):
    url = urljoin(base_url, directory)
    response = requests.get(url)
    if response.status_code == 200:
        print(f"[+] Directory found: {url}")
        return url
    return None


def scan_directories(base_url, directories, max_threads=10):
    found_directories = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_dir = {executor.submit(
            check_directory, base_url, directory): directory for directory in directories}
        for future in concurrent.futures.as_completed(future_to_dir):
            result = future.result()
            if result:
                found_directories.append(result)

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


if __name__ == "__main__":
    base_url = input("Masukkan URL website yang ingin di-scan: ")

    directories = read_directories_from_file('dirWebList.txt')

    print(f"Scanning direktori pada {base_url}...")
    found_dirs = scan_directories(base_url, directories)

    print("\nHasil scan:")
    for dir in found_dirs:
        print(dir)

    print(f"\nTotal direktori ditemukan: {len(found_dirs)}")
