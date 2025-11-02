from flask import Flask, render_template, send_from_directory, request, redirect
from PIL import Image
from image_converter import compress_image
from sanitize_filename import sanitize_filename
import os, shutil

app = Flask(__name__)

image_extensions = (".jpg", ".JPG", ".jpeg", ".png", ".PNG", ".webp", ".WEBP", ".bmp", ".BMP")

cat = "sophie"
convert_images = True  # Set to False if you only want renaming without conversion

image_folder_path = os.path.expanduser(f"~/RouteOfReason/MySuperSite/persistent_disk/cats/{cat}/photos")
new_image_folder_path = os.path.expanduser(f"~/RouteOfReason/MySuperSite/persistent_disk/cats/{cat}/renamed_photos")

def get_first_image():
    files = os.listdir(image_folder_path)
    image_files = [file for file in files if file.lower().endswith(image_extensions)]
    if image_files:
        return image_files[0]
    return None

@app.route('/')
def hello_images():
    first_image = get_first_image()
    if first_image:
        return render_template('index.html', image_name=first_image, convert_mode=convert_images)
    else:
        return "No images found in the folder."
    
@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(image_folder_path, filename)

@app.route('/process', methods=['POST'])
def process_image():
    first_image = get_first_image()
    if not first_image:
        return "No images found in the folder."
    
    new_filename = request.form.get('name')
    image_path = os.path.join(image_folder_path, first_image)
    new_filename = sanitize_filename(cat + ' ' + new_filename)
    
    if convert_images:
        new_image_path = os.path.join(new_image_folder_path, new_filename)
        image = Image.open(image_path)
        converted_image, stats = compress_image(image, max_size_kb=200, return_report=True)
        converted_image.save(new_image_path, format='WebP', quality=100)
        for msg in stats['log']:
            print(msg)
    else:
        original_ext = os.path.splitext(first_image)[1]
        if not new_filename.lower().endswith(image_extensions):
            new_filename += original_ext
        new_image_path = os.path.join(new_image_folder_path, new_filename)
        shutil.copy2(image_path, new_image_path)

    os.remove(image_path)
    return redirect('/')

@app.route('/remove', methods=['POST'])
def remove_image():
    first_image = get_first_image()
    if not first_image:
        return "No images found in the folder."
    
    image_path = os.path.join(image_folder_path, first_image)
    os.remove(image_path)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
