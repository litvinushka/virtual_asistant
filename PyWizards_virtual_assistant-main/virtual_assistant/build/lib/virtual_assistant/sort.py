import os
import shutil
import zipfile
import tarfile

def extract_archive(archive_path, target_folder):
    if archive_path.endswith('.zip'):
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(target_folder)
    elif archive_path.endswith('.tar.gz') or archive_path.endswith('.tar'):
        with tarfile.open(archive_path, 'r') as tar_ref:
            tar_ref.extractall(target_folder)
    else:
        print(f"Unsupported archive format: {archive_path}")

def organize_files(folder):
    if not os.path.exists(folder):
        return "Error: Folder does not exist."
    
    file_types = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif'],
        'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', 'xls'],
        'Videos': ['.mp4', '.avi', '.mov'],
        'Music': ['.mp3', '.wav', '.flac'],
    }
    
    other_folder = os.path.join(folder, 'Other')
    if not os.path.exists(other_folder):
        os.makedirs(other_folder)
    
    archives_folder = os.path.join(folder, 'archives')
    if not os.path.exists(archives_folder):
        os.makedirs(archives_folder)
    
    for root, _, files in os.walk(folder):
        for filename in files:
            file_extension = os.path.splitext(filename)[1].lower()
            target_subfolder = None
            
            for folder_name, extensions in file_types.items():
                if file_extension in extensions:
                    target_subfolder = folder_name
                    break
            
            if target_subfolder:
                target_path = os.path.join(folder, target_subfolder, filename)
            else:
                target_path = os.path.join(other_folder, filename)
                
            source_path = os.path.join(root, filename)
            if not os.path.exists(os.path.dirname(target_path)):
                os.makedirs(os.path.dirname(target_path))
            
            shutil.move(source_path, target_path)
    
    for subfolder in os.listdir(folder):
        subfolder_path = os.path.join(folder, subfolder)
        if os.path.isdir(subfolder_path) and not os.listdir(subfolder_path):
            os.rmdir(subfolder_path)
    
    for root, _, files in os.walk(folder):
        for filename in files:
            if filename.endswith('.zip') or filename.endswith('.tar.gz') or filename.endswith('.tar') or filename.endswith('.rar'):
                archive_path = os.path.join(root, filename)
                archive_name = os.path.splitext(filename)[0]  # Get archive name without extension
                extract_folder = os.path.join(root, archive_name)
                try:
                    extract_archive(archive_path, extract_folder)
                    extracted_archive_path = os.path.join(root, archive_name)
                    moved_archive_path = os.path.join(archives_folder, filename)
                    if not os.path.exists(moved_archive_path):  # Check if destination doesn't exist
                        shutil.move(extracted_archive_path, moved_archive_path)
                    os.remove(archive_path) 
                except:
                    print("Can not proceed with unpacking. Archive is corrupted.")
    return "Sorting complete!"
