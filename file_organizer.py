import os
import shutil

Extension_Map = {
    '.jpg': 'Images',
    '.jpeg': 'Images',
    '.png': 'Images',
    '.gif': 'Images',
    '.pdf': 'Documents',
    '.docx': 'Documents',
    '.txt': 'Documents',
    '.mp3': 'Audio',
    '.wav': 'Audio',
    '.mp4': 'Videos',
    '.mkv': 'Videos'
}

if __name__ == "__main__":
    folder = input("Enter folder name: ")

    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)

        # Skip if it's a folder
        if os.path.isdir(file_path):
            continue

        _, ext = os.path.splitext(file)

        if ext in Extension_Map:
            folder_name = Extension_Map[ext]
            destination_folder = os.path.join(folder, folder_name)

            # Create the destination folder if it doesn't exist
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)

            # Move the file
            shutil.move(file_path, os.path.join(destination_folder, file))

    print("Files organized successfully!")
