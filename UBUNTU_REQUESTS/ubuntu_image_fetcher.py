import requests
import os
import hashlib
from urllib.parse import urlparse

def is_safe_image(response):
    """Check if the downloaded content is a safe image type."""
    content_type = response.headers.get("Content-Type", "")
    return content_type.startswith("image/")

def generate_filename(url, response):
    """Extract filename from URL or create one from hash if missing."""
    parsed = urlparse(url)
    filename = os.path.basename(parsed.path)

    if not filename or "." not in filename:
        # Generate fallback name using hash
        ext = response.headers.get("Content-Type", "").split("/")[-1]
        return f"downloaded_image.{ext if ext else 'jpg'}"
    return filename

def is_duplicate(content):
    """Check if image content hash already exists to avoid duplicates."""
    file_hash = hashlib.sha256(content).hexdigest()
    hash_path = os.path.join("Fetched_Images", f"{file_hash}.hash")

    if os.path.exists(hash_path):
        return True, hash_path
    else:
        with open(hash_path, "w") as f:
            f.write("")  # Mark as seen
        return False, hash_path

def main():
    print("\nWelcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web")
    print("Ubuntu Principle: 'I am because we are'\n")

    # Multiple URL support
    url_input = input("Enter one or more image URLs (comma-separated): ")
    urls = [u.strip() for u in url_input.split(",") if u.strip()]

    # Prepare directory
    os.makedirs("Fetched_Images", exist_ok=True)

    for url in urls:
        print(f"\nConnecting to: {url}")
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Safety: verify content-type
            if not is_safe_image(response):
                print("✗ Unsafe file type detected. Skipping.")
                continue

            # Duplicate check
            duplicate, hashpath = is_duplicate(response.content)
            if duplicate:
                print("✓ Duplicate image detected — already downloaded. Skipping.")
                continue

            # Determine filename
            filename = generate_filename(url, response)
            filepath = os.path.join("Fetched_Images", filename)

            # Save image
            with open(filepath, "wb") as f:
                f.write(response.content)

            print(f"✓ Successfully fetched: {filename}")
            print(f"✓ Saved to: {filepath}")
            print("✓ Content-Type:", response.headers.get("Content-Type", "unknown"))
            print("✓ Content-Length:", response.headers.get("Content-Length", "unknown"))

        except requests.exceptions.RequestException as e:
            print(f"✗ Connection error: {e}")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")

    print("\nConnection strengthened. Community enriched.\n")

if __name__ == "__main__":
    main()
