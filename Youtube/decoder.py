from pytube import YouTube
import cv2
import os
from PIL import Image
import binascii


def clear(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        os.remove(file_path)


def download_video(video_id, video_name, resolution, output_path=None):
    video_url = f'https://youtube.com/watch?v={video_id}'
    yt = YouTube(video_url)
    stream = yt.streams.filter(res=resolution).first()
    stream.download(output_path=output_path, filename=video_name)


def save_frames(video_path, output_path):
    video = cv2.VideoCapture(video_path)
    frame_count = 0
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        frame_filename = os.path.join(output_path, f'#{frame_count:04d}.png')
        cv2.imwrite(frame_filename, frame)
        frame_count += 1
    video.release()
    cv2.destroyAllWindows()


def find_closest(tup):
    if tup[0] + tup[1] + tup[2] > 500:
        return (255, 255, 255)
    else:
        temp = max(tup)
        index = tup.index(temp)
        if index == 0:
            return (255, 0, 0)
        elif index == 1:
            return (0, 255, 0)
        else:
            return (0, 0, 255)


def get_color(image_folder):
    images = []
    guesses = ''
    convert = {(255, 255, 255) : '0', (255, 0, 0) : '1', (0, 255, 0) : '2', (0, 0, 255) : '3'}
    for image in os.listdir(image_folder):
        images.append(image)
    for image_path in images:
        image = Image.open(os.path.join(image_folder, image_path))
        pixels = list(image.getdata())
        dimensions = [image.width, image.height]
        for y in range(int(dimensions[1] / 10)):
            for x in range(int(dimensions[0] / 10)):
                index = (x * 10 + 4) + (y * 10 * dimensions[0]) + 4 * dimensions[0]
                try:
                    guesses += convert[find_closest(pixels[index])]
                except IndexError:
                    print(x, y)
    return guesses


def quaternary_to_hex(quaternary_data):
    hex_data = ''
    for i in range(0, len(quaternary_data), 2):
        num = int(quaternary_data[i]) * 4 + int(quaternary_data[i + 1])
        if num < 10:
            hex_data += str(num)
        else:
            convert = {10 : 'a', 11 : 'b', 12 : 'c', 13 : 'd', 14 : 'e', 15 : 'f'}
            hex_data += convert[num]
    return hex_data


def hex_to_file(hex_data, output_path):
    bytes_data = bytes.fromhex(hex_data)
    with open(output_path, 'wb') as f:
        f.write(bytes_data)
    

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


def file_to_hex(path):
    with open(path, 'rb') as f:
        data = f.read()
    hex_data = binascii.hexlify(data).decode('utf-8')
    return hex_data


real_data = file_to_hex('duotrigordle.png')
video_id = input('ID of the video: ')
output_path = input('Output path: ')
download_video(video_id, 'youtube_video.mp4', '2160p')
save_frames('youtube_video.mp4', 'frames')
os.remove('youtube_video.mp4')
quaternary_data = get_color('frames')
clear('frames')
hex_data = quaternary_to_hex(quaternary_data)
hex_to_file(hex_data, output_path)
