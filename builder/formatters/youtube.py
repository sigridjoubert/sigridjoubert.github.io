import re

from .formatter import Formatter


class YoutubeFormatter(Formatter):

    def format_content(self, soup):
        for a in soup.find_all("a", href=True):
            url = a["href"]
            video_id = None

            # Match full and short YouTube URLs
            # Example: https://www.youtube.com/watch?v=VIDEO_ID
            match_watch = re.search(r"youtube\.com/watch\?v=([-\w]+)", url)
            # Example: https://youtu.be/VIDEO_ID
            match_short = re.search(r"youtu\.be/([-\w]+)", url)

            if match_watch:
                video_id = match_watch.group(1)
            elif match_short:
                video_id = match_short.group(1)

            if video_id:
                iframe_tag = soup.new_tag(
                    "iframe",
                    src=f"https://www.youtube.com/embed/{video_id}",
                    title="YouTube video player",
                    frameborder="0",
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture",
                    allowfullscreen=True,
                    **{"class": "youtube"},
                )
                a.replace_with(iframe_tag)
        return soup
