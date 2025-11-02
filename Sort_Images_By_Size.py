import os
import cv2
import shutil

def get_folder_for_size(max_dim):
    """Return the appropriate folder name based on max dimension."""
    if 0 <= max_dim <= 10:
        return "10px"
    elif 11 <= max_dim <= 50:
        return "50px"
    elif 51 <= max_dim <= 100:
        return "100px"
    elif 101 <= max_dim <= 150:
        return "200px"
    elif max_dim >= 151:  # everything 151px and above → 300px folder
        return "300px"


def main():
    input_folder = input("Enter input folder path (where images are stored): ").strip('"')
    output_folder = input("Enter output folder path (where sorted images will go): ").strip('"')

    # Validate input
    if not os.path.exists(input_folder):
        print("❌ Input folder not found.")
        return

    # Create output folders if they don't exist
    categories = ["10px", "50px", "100px", "200px", "300px"]
    for category in categories:
        os.makedirs(os.path.join(output_folder, category), exist_ok=True)

    count = 0
    skipped = 0

    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)

        # Skip non-files (like directories)
        if not os.path.isfile(file_path):
            continue

        # Read image
        img = cv2.imread(file_path)
        if img is None:
            skipped += 1
            continue

        height, width = img.shape[:2]
        max_dim = max(height, width)

        # Determine target folder
        folder_name = get_folder_for_size(max_dim)
        if folder_name:
            target_path = os.path.join(output_folder, folder_name, filename)
            shutil.move(file_path, target_path)
            count += 1
        else:
            skipped += 1

        # Progress log every 500 files
        if count % 500 == 0 and count > 0:
            print(f"✅ Processed {count} images...")

    print(f"\n✅ Done! Moved {count} images. Skipped {skipped} files.")

if __name__ == "__main__":
    main()
