import logging

from django.conf import settings
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from .base import JasprBaseView

logger = logging.getLogger(__name__)


class StaticMediaView(JasprBaseView):

    permission_classes = []

    @staticmethod
    def getData(media_url):
        data = {
            "media_url": media_url,
            "intro": {
                "poster": f"{media_url}david_diana_poster-862b7101cf13a044ba012f70cf178bf1.jpg",  #
                "dash": f"{media_url}Jaspr_Intro_Video-b02e92a886f473315f8c1155dd26813f/index.mpd",  #
                "hls": f"{media_url}Jaspr_Intro_Video-b02e92a886f473315f8c1155dd26813f/index.m3u8",  #
                "video": f"{media_url}Jaspr_Intro_Video-b02e92a886f473315f8c1155dd26813f/kiosk_720p_Jaspr_Intro_Video-b02e92a886f473315f8c1155dd26813f.mp4",  #
            },
            "expect": {
                "poster": f"{media_url}TOPHERwhatToExpectTodayVideoPoster.png",  #
                "dash": f"{media_url}Topher-_What_to_Expect_Today/index.mpd",  #
                "hls": f"{media_url}Topher-_What_to_Expect_Today/index.m3u8",  #
                "video": f"{media_url}Topher-_What_to_Expect_Today/jaspr_720p_Topher-_What_to_Expect_Today.mp4",  #
            },
            "tutorialJasper": {
                "poster": f"{media_url}Screen_Shot_2020-01-16_at_8.06.48_AM.png",  #
                "dash": f"{media_url}jasper_tutorial_/index.mpd",  #
                "hls": f"{media_url}jasper_tutorial_/index.m3u8",  #
                "video": f"{media_url}jasper_tutorial_/jaspr_720p_jasper_tutorial_.mp4",  #
            },
            "tutorialJaz": {
                "poster": f"{media_url}Screen_Shot_2020-01-16_at_8.06.48_AM.png",  #
                "dash": f"{media_url}jaz_tutorial_/index.mpd",  #
                "hls": f"{media_url}jaz_tutorial_/index.m3u8",  #
                "video": f"{media_url}jaz_tutorial_/jaspr_720p_jaz_tutorial_.mp4",  #
            },
            "nationalHotline": {
                "poster": f"{media_url}Screen_Shot_2020-06-10_at_9.20.13_AM.png",
                "hls": f"{media_url}Allie_-_ICM_-_Crisis_Line_-_What_it_is/index.m3u8",
                "dash": f"{media_url}Allie_-_ICM_-_Crisis_Line_-_What_it_is/index.mpd",
            },
            "crisisLines": {
                "poster": f"{media_url}riley_-_crisis_lines_poster_compressed.jpg",
                "video": f"{media_url}Riley_-_ICM_-_Crisis_Line_Shared_Story/kiosk_720p_Riley_-_ICM_-_Crisis_Line_Shared_Story.mp4",
                "hls": f"{media_url}Riley_-_ICM_-_Crisis_Line_Shared_Story/index.m3u8",
                "dash": f"{media_url}Riley_-_ICM_-_Crisis_Line_Shared_Story/index.mpd",
            },
            "crisisLinesExpect": {
                "poster": f"{media_url}Screen_Shot_2020-06-10_at_9.19.23_AM.png",
                "dash": f"{media_url}Allie_-_ICM_-_Crisis_Line_-_What_to_Expect/index.mpd",
                "hls": f"{media_url}Allie_-_ICM_-_Crisis_Line_-_What_to_Expect/index.m3u8",
            },
            "supportivePeople": {
                "poster": f"{media_url}Screen_Shot_2020-06-05_at_11.21.18_AM.png",
                "dash": f"{media_url}Topher_-_ICM_-_Supportive_Poeple_-_Shared_Story/index.mpd",
                "hls": f"{media_url}Topher_-_ICM_-_Supportive_Poeple_-_Shared_Story/index.m3u8",
            },
            "copingStrategies": {
                "poster": f"{media_url}Screen_Shot_2020-06-05_at_10.53.01_AM.png",
                "dash": f"{media_url}Topher_-_ICM_-_Coping_Skills_-_Basic/index.mpd",
                "hls": f"{media_url}Topher_-_ICM_-_Coping_Skills_-_Basic/index.m3u8",
            },
            "reasonsLive": {
                "poster": f"{media_url}Screen_Shot_2020-06-05_at_10.48.45_AM.png",
                "dash": f"{media_url}Kelechi_-_ICM_-_Reasons_for_Living_-_Basic/index.mpd",
                "hls": f"{media_url}Kelechi_-_ICM_-_Reasons_for_Living_-_Basic/index.m3u8",
            },
            "saferHome": {
                "poster": f"{media_url}Screen_Shot_2020-06-05_at_10.44.22_AM.png",
                "dash": f"{media_url}Topher_-_ICM_-_Making_Home_Safer_-_Basics/index.mpd",
                "hls": f"{media_url}Topher_-_ICM_-_Making_Home_Safer_-_Basics/index.m3u8",
            },
            "warningSignals": {
                "poster": f"{media_url}Screen_Shot_2020-06-05_at_10.40.30_AM.png",
                "dash": f"{media_url}Topher_-_ICM_-_No_Script_-_Early_Warning_Signs_-_.Basic/index.mpd",
                "hls": f"{media_url}Topher_-_ICM_-_No_Script_-_Early_Warning_Signs_-_.Basic/index.m3u8",
            },
        }
        return data

    def get(self, request: Request) -> Response:
        data = StaticMediaView.getData(settings.MEDIA_URL)
        return Response(
            data=data,
            status=status.HTTP_200_OK,
        )