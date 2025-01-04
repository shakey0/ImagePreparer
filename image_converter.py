from PIL import Image, ImageOps
from io import BytesIO

def compress_image(input_image, max_size_kb=200, return_report=False):

    def get_file_size_or_compress(img, new_quality=None):
        buffer = BytesIO()
        img.save(buffer, format='WebP', quality=new_quality or 100)
        buffer.seek(0, 2)
        size_bytes = buffer.tell()
        buffer.seek(0)
        compressed_img = Image.open(buffer)
        compressed_img.load()

        buffer.close()
        if new_quality:
            return compressed_img
        return size_bytes / 1024

    def log_status(msg, stats):
        stats['log'].append(msg)

    stats = {
        'original_size': None,
        'original_dimensions': None,
        'final_size': None,
        'final_dimensions': None,
        'final_quality': None,
        'size_change_kb': None,
        'size_change_percent': None,
        'log': []
    }

    if isinstance(input_image, str):
        try:
            with open(input_image, 'rb') as f:
                f.seek(0, 2)
                initial_size = f.tell() / 1024
                f.seek(0)
                image = Image.open(f)
                image.load()
        except Exception as e:
            raise ValueError(f"Error opening image file: {e}")
    else:
        image = input_image.copy()
        initial_size = get_file_size_or_compress(image)

    try:
        image = ImageOps.exif_transpose(image)
    except:
        pass

    if image.mode == 'RGBA':
        background = Image.new('RGB', image.size, (255, 255, 255))
        background.paste(image, mask=image.split()[3])
        image = background

    original_dimensions = image.size
    stats['original_size'] = initial_size
    stats['original_dimensions'] = original_dimensions
    log_status(f"Input image size: {initial_size}KB", stats)
    log_status(f"Original dimensions: {original_dimensions[0]}x{original_dimensions[1]}", stats)

    if initial_size <= max_size_kb:
        log_status("Image already under target size. Converting to WebP.", stats)
        stats.update({
            'final_size': initial_size,
            'final_dimensions': original_dimensions,
            'final_quality': 100,
            'size_change_kb': 0,
            'size_change_percent': 0
        })
        return (image, stats) if return_report else image

    if image.width > 1920 or image.height > 1080:
        log_status("Image exceeds 1920x1080, resizing...", stats)
        image.thumbnail((1920, 1080), Image.Resampling.LANCZOS)
        current_size = get_file_size_or_compress(image)
        log_status(f"Resized to: {image.width}x{image.height}", stats)

        if current_size <= max_size_kb:
            stats.update({
                'final_size': current_size,
                'final_dimensions': image.size,
                'final_quality': 95,
                'size_change_kb': current_size - initial_size,
                'size_change_percent': ((current_size - initial_size) / initial_size) * 100
            })
            return (image, stats) if return_report else image

    quality = 95
    while quality > 10:
        image = get_file_size_or_compress(image, new_quality=quality)
        current_size = get_file_size_or_compress(image)
        log_status(f"Size at start of loop: {current_size}KB", stats)

        if current_size <= max_size_kb:
            break

        # Reduce dimensions by 5%
        current_width, current_height = image.size
        new_width = int(current_width * 0.95)
        new_height = int(current_height * 0.95)

        # Don't resize if images would become too small
        if new_width < 600 or new_height < 600:
            break

        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        log_status(f"Resized to: {new_width}x{new_height}", stats)

        # Try current quality with new size
        current_size = get_file_size_or_compress(image)
        log_status(f"Size after resize: {current_size}KB", stats)

        if current_size > max_size_kb:
            log_status(f"Quality {quality} too high, trying lower...", stats)
            quality -= 5

    final_size = get_file_size_or_compress(image)

    stats.update({
        'final_size': final_size,
        'final_dimensions': image.size,
        'final_quality': quality,
        'size_change_kb': final_size - initial_size,
        'size_change_percent': ((final_size - initial_size) / initial_size) * 100
    })

    log_status("\nFinal results:", stats)
    log_status(f"Original dimensions: {original_dimensions[0]}x{original_dimensions[1]}", stats)
    log_status(f"Final dimensions: {image.width}x{image.height}", stats)
    log_status(f"Input size: {initial_size}KB", stats)
    log_status(f"Output size: {final_size}KB", stats)
    log_status(f"Size change: {stats['size_change_kb']}KB ({stats['size_change_percent']}%)", stats)
    log_status(f"Final quality: {quality}", stats)

    return (image, stats) if return_report else image
