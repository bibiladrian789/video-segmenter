import os
from moviepy.editor import VideoFileClip

# This code is suitable for splitting long-duration videos into multiple shorter-duration 
# videos throughout the entire original video duration (Example: A 1-hour CCTV video becomes multiple 1-minute CCTV videos).


# Input and output folders
input_folder = "../VideoDatasetsRaw/VideoDatasetsNight"   # Replace with the input folder (the input is all video inside one folder)
output_folder = "../VideoMinutes_Night" # Replace with the output folder (the output is all video from the input and saved to one folder)

# Loop over all files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".mp4"):  # Check if the file is an mp4 video file
        # Extract timestamp and camera ID from filename
        print('Proses Video:', filename)
        timestamp, camera_id = filename[:-4].split("_")
        year, month, day, hour = timestamp[:4], timestamp[4:6], timestamp[6:8], timestamp[8:10]

        # Open video file
        video_path = os.path.join(input_folder, filename)

        # Create output folder for current video
        output_video_folder = os.path.join(output_folder, timestamp)
        os.makedirs(output_video_folder, exist_ok=True)

        # Load video clip
        video_clip = VideoFileClip(video_path)

        # Set clip duration to 1 minute
        clip_duration = 60

        # Calculate the total number of minutes in the video
        total_minutes = int(video_clip.duration // clip_duration)

        # Loop over all minutes in the video
        for current_minute in range(total_minutes):
            # Set start and end times for current minute
            start_time = current_minute * clip_duration
            end_time = start_time + clip_duration

            # Set output filename for current minute
            output_filename = f"{year}{month}{day}{hour}{current_minute:02d}_{camera_id}.mp4"  # Replace with the desire output file name
            output_path = os.path.join(output_video_folder, output_filename)

            # If the output file already exists, skip this minute
            if os.path.exists(output_path):
                print('Path exist')
                continue

            # Extract video segment for current minute and save as a new video
            minute_clip = video_clip.subclip(start_time, end_time)
            minute_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
            print('Video has been extracted:', output_filename)

        # Close the video clip
        video_clip.close()