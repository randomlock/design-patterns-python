import enum
import os
from abc import ABC, abstractmethod

import requests

"""
Adapter Pattern

- Provides a structure way to make incompatible but related object to collaborate
- Example - If you are using multiple different API to upload video. You can use an adapter and use
it as single source of uploading video
"""


# Example - You provided an API to upload video to either youtube or dailymotion. To upload to
# youtube you need to add image attachment as well. To upload to dailymotion you will need to pre
# process the video to make it compatible with it. So we have to source to upload video and they
# have different requirement. So we made an adapter for both of them which implement a common method
# to upload video. If new sources are added which have different API, we can easily create a new
# Adapter for it.


class VideoSource(enum.Enum):
    youtube = 1
    dailymotion = 2


class UploadVideo(ABC):

    @abstractmethod
    def upload(self, video):
        pass


class Youtube:

    def extract_photo_from_video(self, video):
        # Do some processing
        print('Extracting photo from video')
        return video

    def upload_youtube_video(self, video, display_image):

        print('Uploading youtube video')
        return video


class DailyMotion:

    def pre_process_video(self, video):
        print('Pre processing video before uploading')
        return video

    def upload_dailymotion_video(self, video):
        print('Uploading dailymotion Video')
        return video


class DailyMotionAdapter(DailyMotion, UploadVideo):

    def upload(self, video):
        processed_video = self.pre_process_video(video)
        self.upload_dailymotion_video(processed_video)


class YoutubeAdapter(Youtube, UploadVideo):

    def upload(self, video):
        photo = self.extract_photo_from_video(video)
        self.upload_youtube_video(video, photo)


def get_video_adapter(source):
    mapping = {
        VideoSource.dailymotion: DailyMotionAdapter(),
        VideoSource.youtube: YoutubeAdapter(),
    }
    return mapping.get(source)


if __name__ == '__main__':

    video_source = os.environ.get('video_source', VideoSource.dailymotion)
    adapter = get_video_adapter(video_source)
    adapter.upload(None)

    video_source = VideoSource.youtube
    adapter = get_video_adapter(video_source)
    adapter.upload(None)


"""
Output
Pre processing video before uploading
Uploading dailymotion Video
Extracting photo from video
Uploading youtube video
"""