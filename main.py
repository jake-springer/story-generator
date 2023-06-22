from datetime import datetime 
import json
import secrets
from instagrapi import Client
from PIL import Image, ImageDraw, ImageFont
import os
import textwrap

#---------------------------------------------------------------

username = secrets.USERNAME
password = secrets.PASSWORD

#---------------------------------------------------------------

post = True

data_file = "data.json"
img_dir = "story_images"

base_img = "black.png"
# img_font_family = "FreeMono.tff"
img_font_family = "/usr/share/fonts-hack/Hack-Regular.ttf"
img_font_size = 46
text_x_pos = 10
text_y_pos = 200
font_color = (255,255,255)

max_char_len = 37

#---------------------------------------------------------------

# client = Client()
# client.login(username, password)
# client.photo_upload_to_story(img, cap)

#---------------------------------------------------------------

def load_json():
    with open(data_file, 'r') as file:
        return json.load(file)

def save_json(data):
    with open(data_file, 'w') as file:
        file.write(json.dumps(data, indent=4))


def get_now(): 
    now = datetime.now()
    d_format = "%m/%d/%y"
    t_format = "%H:%M:%S"
    d = now.strftime(d_format)
    t = now.strftime(t_format)
    return (d,t)

#---------------------------------------------------------------

def get_img_id():
    data = load_json()
    last_used = data["last_img_id"]
    new = last_used + 1
    data["last_img_id"] = new
    save_json(data)
    return new


def create_img(text):
    new_id = get_img_id()
    formatted = ""
    wrapped = textwrap.wrap(text, width=max_char_len)
    for w in wrapped:
        formatted += w
        formatted += '\n'

    formatted += f'\n\n{get_now()[1]}\nIMG ID: {str(new_id)}'
    
    print("[>] Creating image")
    img = Image.open(base_img)
    i1 = ImageDraw.Draw(img)
    img_font = ImageFont.truetype(img_font_family, img_font_size)
    i1.text(
        (
            text_x_pos,
            text_y_pos
        ),
        formatted,
        font=img_font,
        fill=font_color
    )
    new_img_file = f"story_img_{str(new_id)}.jpeg"
    new_img_path = os.path.join(img_dir, new_img_file)
    img.save(new_img_path)
    print("[>] Saved new image --> " + new_img_path)
    return new_img_path
    
    

def main(text):
    story_img = create_img(text)
    if post:
        client = Client()
        print("[>] Connecting to client")
        client.login(username, password)
        print("[>] Uploading story")
        client.photo_upload_to_story(story_img)
        print("[>] Completed")
    

text = "Puffins are any of three species of small alcids (auks) in the bird genus Fratercula. These are pelagic seabirds that feed primarily by diving in the water. They breed in large colonies on coastal cliffs or offshore islands, nesting in crevices among rocks or in burrows in the soil. Two species, the tufted puffin and horned puffin, are found in the North Pacific Ocean, while the Atlantic puffin is found in the North Atlantic Ocean. "

main(text)