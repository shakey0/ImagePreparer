from flask import Flask, render_template, send_from_directory, request, redirect
from PIL import Image
from image_converter import compress_image
from sanitize_filename import sanitize_filename
import os, json

app = Flask(__name__)

image_extensions = (".jpg", ".JPG", ".jpeg", ".png", ".PNG", ".webp", ".WEBP", ".bmp", ".BMP")

cat = "sophie"
image_folder_path = os.path.expanduser(f"~/Pictures/cats/{cat}/raw_photos")
new_image_folder_path = os.path.expanduser(f"~/Pictures/cats/{cat}/ready_photos")
json_path = os.path.expanduser(f"~/Pictures/cats/{cat}/{cat}.json")

def get_first_image():
    files = os.listdir(image_folder_path)
    image_files = [file for file in files if file.lower().endswith(image_extensions)]
    if image_files:
        return image_files[0]
    return None

def get_all_album_names():
    with open(json_path, 'r') as f:
        data = json.load(f)
        albums = data['albums']
        return [album['name'] for album in albums]

@app.route('/')
def hello_images():
    first_image = get_first_image()
    album_names = get_all_album_names()
    if first_image:
        return render_template('index.html', image_name=first_image, album_names=album_names)
    else:
        return "No images found in the folder."
    
@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(image_folder_path, filename)

@app.route('/convert', methods=['POST'])
def convert_image():
    first_image = get_first_image()
    if not first_image:
        return "No images found in the folder."
    
    new_filename = request.form.get('name')
    image_path = os.path.join(image_folder_path, first_image)
    new_filename = sanitize_filename(new_filename)
    new_image_path = os.path.join(new_image_folder_path, new_filename)

    image = Image.open(image_path)
    converted_image, stats = compress_image(image, max_size_kb=200, return_report=True)
    converted_image.save(new_image_path, format='WebP', quality=100)
    for msg in stats['log']:
        print(msg)
    
    os.remove(image_path)

    album = request.form.get('album')

    with open(json_path, 'r') as f:
        data = json.load(f)
        albums = data['albums']
        
        for album_data in albums:
            if album_data['name'] == album:
                order_num = len(album_data['photos']) + 1
                album_data['photos'].append({'name': new_filename, 'order': order_num})
                break

    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)

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
