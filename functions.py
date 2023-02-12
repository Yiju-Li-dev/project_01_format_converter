import os


def convert_avi_to_mp4(input_dir, output_dir):
    commands = []
    ordering = 1
    for filename in os.listdir(input_dir):
        if filename.endswith(".avi"):
            input_file = input_dir + '\\'+ filename
            output_file = output_dir + '\\'+ str(ordering) + '.mp4'
            ordering += 1
            command = [
                "ffmpeg",
                "-i", input_file,
                "-c:v", "h264_nvenc",
                "-preset", "p1",
                output_file
            ]
            commands.append(command)
    return commands