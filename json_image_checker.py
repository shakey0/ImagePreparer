import os, json

cat = "amber"
new_image_folder_path = os.path.expanduser(f"~/Pictures/cats/{cat}/ready_photos")
json_path = os.path.expanduser(f"~/Pictures/cats/{cat}/{cat}.json")

files = os.listdir(new_image_folder_path)

photos_in_json = []
with open(json_path, 'r') as f:
    data = json.load(f)
    albums = data['albums']
    for album in albums:
        photos_in_json.extend(album['photos'])

# Check if all photos in the JSON file are in the folder
print("\nChecking if all photos in the JSON file are in the folder...")
for photo in photos_in_json:
    if photo['name'] not in files:
        print(f"Photo {photo['name']} is missing from the folder.")
    else:
        print(f"OKAY: {photo['name']}")

# Check if all photos in the folder are in the JSON file
print("\nChecking if all photos in the folder are in the JSON file...")
for file in files:
    if file not in [photo['name'] for photo in photos_in_json]:
        print(f"Photo {file} is not in the JSON file.")
    else:
        print(f"OKAY: {file}")
