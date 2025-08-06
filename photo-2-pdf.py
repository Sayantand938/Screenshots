import os
from PIL import Image
import time # Used for sorting by creation time

def convert_pngs_to_pdf():
    """
    Converts all PNG files in the current directory to a single PDF,
    ordered by creation time (oldest first), and then deletes the PNGs.
    """
    output_pdf_filename = "questions.pdf"
    current_directory = os.getcwd()
    
    print(f"🔍 Searching for PNG files in: {current_directory}")

    png_files_info = []
    for filename in os.listdir(current_directory):
        if filename.lower().endswith(".png"):
            filepath = os.path.join(current_directory, filename)
            try:
                # Get creation time (ctime) of the file
                creation_time = os.path.getctime(filepath)
                png_files_info.append((creation_time, filepath))
            except OSError as e:
                print(f"⚠️ Could not get creation time for {filename}: {e}")
                continue

    if not png_files_info:
        print("❌ No PNG files found in the current directory. No PDF will be created.")
        return

    # Sort files by creation time (oldest to newest)
    png_files_info.sort()
    sorted_png_filepaths = [info[1] for info in png_files_info]

    print(f"✅ Found {len(sorted_png_filepaths)} PNG files. Converting to PDF...")
    
    images = []
    try:
        for filepath in sorted_png_filepaths:
            img = Image.open(filepath)
            # Convert image to RGB if it's not, as PDF typically prefers RGB
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            elif img.mode == 'P': # Handle paletted images
                img = img.convert('RGB')
            images.append(img)

        if images:
            # Save the first image, then append the rest
            images[0].save(
                output_pdf_filename,
                save_all=True,
                append_images=images[1:],
                resolution=100.0 # Adjust resolution for PDF output if needed
            )
            print(f"🎉 Successfully created '{output_pdf_filename}'!")

            # Delete original PNG files
            print("🗑️ Deleting original PNG files...")
            for filepath in sorted_png_filepaths:
                try:
                    os.remove(filepath)
                    print(f"   Deleted: {os.path.basename(filepath)}")
                except OSError as e:
                    print(f"   ⚠️ Error deleting {os.path.basename(filepath)}: {e}")
            print("Cleanup complete.")
        else:
            print("⚠️ No valid images were processed for PDF creation.")

    except Exception as e:
        print(f"❌ An error occurred during PDF creation or image processing: {e}")
        print("Original PNG files were NOT deleted due to the error.")

# Run the function
if __name__ == "__main__":
    convert_pngs_to_pdf()
