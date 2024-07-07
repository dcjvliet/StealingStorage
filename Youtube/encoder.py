import binascii
from PIL import Image
import imageio.v2 as imageio
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import ffmpeg


def quaternify(hex_data):
    quaternary_data = ''
    for char in hex_data:
        try:
            char = int(char)
        except ValueError: 
            hex_base_ten = {'a' : 10, 'b' : 11, 'c' : 12, 'd' : 13, 'e' : 14, 'f' : 15}
            char = hex_base_ten[char.lower()]
        quaternary_data += str(char // 4)
        quaternary_data += str(char % 4)
    return quaternary_data


def clear(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        os.remove(file_path)


def file_to_hex(path):
    with open(path, 'rb') as f:
        data = f.read()
    hex_data = binascii.hexlify(data).decode('utf-8')
    return hex_data


def hex_to_color(quaternary_data, resolution):
    convert = {'0' : (255, 255, 255), '1' : (255, 0, 0), '2' : (0, 255, 0), '3' : (0, 0, 255)}
    images = []
    pixel_colors = []
    for char in quaternary_data:
        pixel_colors.append(convert[char])
    if len(pixel_colors) < int(resolution[0] / 5) * int(resolution[1] / 5):
        image = Image.new('RGB', resolution)
        for y in range(int(resolution[1] / 5)):
            for x in range(int(resolution[0] / 5)):
                try:
                    for dy in range(3):
                        for dx in range(3):
                            image.putpixel((x * 5 + 1 + dx, y * 5 + 1 + dy), pixel_colors[x + y * int(resolution[0] / 5)])
                except IndexError:
                    break
        images.append(image)
        return images
    else:
        i = 0
        while i * int(resolution[0] / 5) * int(resolution[1] / 5) < len(pixel_colors):
            image = Image.new('RGB', resolution)
            for y in range(int(resolution[1] / 5)):
                for x in range(int(resolution[0] / 5)):
                    try:
                        for dy in range(3):
                            for dx in range(3):
                                image.putpixel((x * 5 + 1 + dx, y * 5 + 1 + dy), pixel_colors[i * int(resolution[0] / 5) * int(resolution[1] / 5)  + (x + y * int(resolution[0] / 5))])
                    except IndexError:
                        break
            images.append(image)
            i += 1
        return images


def image_to_video(input_folder, output_path, fps):
    images = os.listdir(input_folder)
    image_list = []
    for image in images:
        img_path = os.path.join(input_folder, image)
        img = imageio.imread(img_path)
        image_list.append(img)
    imageio.mimsave(output_path, image_list, fps=fps)


def hd_to_4k(input_folder, output_folder):
    images = os.listdir(input_folder)
    for i in range(len(images)):
        image_path = os.path.join(input_folder, images[i])
        output_path = f'{output_folder}/#{i:04d}.png'
        (ffmpeg
         .input(image_path)
         .filter('scale', 3840, 2160)
         .output(output_path)
         .run())


CLIENT_SECRETS_FILE = 'client_secrets.json'
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"


def get_authenticated_service():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def upload_video(youtube, title, description, tags, category_id, privacy_status, video_file):
    body=dict(
        snippet=dict(
            title=title,
            description=description,
            tags=tags,
            categoryId=category_id
        ),
        status=dict(
            privacyStatus=privacy_status
        )
    )

    # Call the API's videos.insert method to create and upload the video.
    insert_request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=googleapiclient.http.MediaFileUpload(video_file, chunksize=-1, resumable=True)
    )

    response = None
    while response is None:
        status, response = insert_request.next_chunk()
        if 'id' in response:
            print("Video id '%s' was successfully uploaded." % response['id'])
        elif 'error' in response:
            print("An error occurred: %s" % response['error'])
            break


file_path = input('Path to the file: ')
fps = float(input('Video fps: '))
hex_data = file_to_hex(file_path)
quaternary_data = quaternify(hex_data)
images = hex_to_color(quaternary_data, (1920, 1080))
for i in range(len(images)):
    images[i].save(f'temp/#{i:04d}.png')
hd_to_4k('temp' ,'images')
clear('temp')
image_to_video('images', 'final_video.mp4', fps)

youtube = get_authenticated_service()
try:
    upload_video(youtube, file_path, 'Just a test.', None, None, 'unlisted', 'final_video.mp4')
except googleapiclient.errors.ResumableUploadError:
    print('API quota reached.')

clear('images')
os.remove('final_video.mp4')
