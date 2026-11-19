import numpy as np
from PIL import Image
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip

def _crop_and_resize_pad(image, height=480, width=720):
    if not isinstance(image, Image.Image):
        image = Image.fromarray(image)
    image = np.array(image.convert("RGB"))
    image_height, image_width, _ = image.shape
    if image_height / image_width < height / width:
        pad = int((((height / width) * image_width) - image_height) / 2.)
        padded_image = np.ones((image_height + pad * 2, image_width, 3), dtype=np.uint8) * 255
        # padded_image = np.zeros((image_height + pad * 2, image_width, 3), dtype=np.uint8)
        padded_image[pad:pad+image_height, :] = image
        image = Image.fromarray(padded_image).resize((width, height))
    else:
        pad = int((((width / height) * image_height) - image_width) / 2.)
        padded_image = np.ones((image_height, image_width + pad * 2, 3), dtype=np.uint8) * 255
        # padded_image = np.zeros((image_height, image_width + pad * 2, 3), dtype=np.uint8) 
        padded_image[:, pad:pad+image_width] = image
        image = Image.fromarray(padded_image).resize((width, height))
    return image 


def _crop_and_resize(image, height=512, width=512):
    image = np.array(image)
    image_height, image_width, _ = image.shape
    if image_height / image_width < height / width:
        croped_width = int(image_height / height * width)
        left = (image_width - croped_width) // 2
        image = image[:, left: left+croped_width]
        image = Image.fromarray(image).resize((width, height))
    else:
        croped_height = int(image_width/width*height)
        top = (image_height - croped_height) // 2
        image = image[top:top+croped_height, :]
        image = Image.fromarray(image).resize((width, height))

    return image
    

def write_mp4(video_path, samples, fps=14, audio_bitrate="192k"):
    clip = ImageSequenceClip(samples, fps=fps)
    clip.write_videofile(video_path, audio_codec="aac", audio_bitrate=audio_bitrate, 
                         ffmpeg_params=["-crf", "18", "-preset", "slow"])
