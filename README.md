# ImagePreparer

Welcome to my image preparer. This is a tool I have made to prepare images to be uploaded to a cloud service like S3. It will compress the images down to the size you specify (default is 200kb) and convert them to .webp format. It also ensures the images will appear in the correct orientations as well as ensure any transparent backgrounds are removed. On top of this, it sanitizes the image filenames and adds 12 random alphanumeric chars before the file extension to ensure the files are named uniquely.

As well as prepare the images, it also updates the JSON file with the data of the new images.

#### How it works:
1. It reads and collects all the images in the specified folder ([original images folder path specified here](https://github.com/shakey0/ImagePreparer/blob/main/app.py#L12)) and selects the first image from the folder/list.
2. It opens the JSON file ([JSON path specified here](https://github.com/shakey0/ImagePreparer/blob/main/app.py#L14)) and gets all the album names.
3. The first image and album names are sent to the client.
4. You can then name the image and select which album you want it to be in before clicking convert. (There is also a remove option to delete the image and not include it.)
5. It will then sanitize the filename [sanitize_filename.py](https://github.com/shakey0/ImagePreparer/blob/main/sanitize_filename.py) and create the new path for the image by joining the new filename with the specified folder for converted images ([converted images folder path specified here](https://github.com/shakey0/ImagePreparer/blob/main/app.py#L13)).
6. It will then compress the image and convert it to .webp format [image_converter.py](https://github.com/shakey0/ImagePreparer/blob/main/image_converter.py). A report of what `image_converter.py` did (reduce dimensions and reduce quality) will be printed to the terminal.
7. It will then save the new file to the specified folder for converted images.
8. It will then delete the original image.
9. I will then find the album you chose in the JSON file and add the image (photo) to the data for that album.
10. It will then redirect back to the original GET route (hello_images) and the whole process will repeat until the folder containing the original images is empty.

Once your have finished converting all your images, you can run [json_image_checker.py](https://github.com/shakey0/ImagePreparer/blob/main/json_image_checker.py), which will check that all the images in the specified folder for converted images are in the JSON and vice versa.

## Setup

- Customise your paths in [lines 11-14 in app.py](https://github.com/shakey0/ImagePreparer/blob/main/app.py#L11-L14) and [lines 3-5 in json_image_checker.py](https://github.com/shakey0/ImagePreparer/blob/main/json_image_checker.py#L3-L5).
- Make sure your JSON file contains an array named `albums`.
- Make sure the `albums` array in your JSON file contains at least one object with the following items:
    - `name`:string (album name)
    - `photos`:array

Run the following command to clone the repo:
```bash
git clone https://github.com/shakey0/ImagePreparer
cd ImagePreparer
```

Create your virtual environment:
```bash
pipenv install
pipenv shell
```

Install dependencies:
```bash
pip install -r requirements.txt
```
