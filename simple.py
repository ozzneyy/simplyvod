import sys
from vod_recovery import twitch_recover

def website_video_recovery(url):
    link = twitch_recover(url)
    return link

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python simple.py <twitch_vod_url>")
        sys.exit(1)

    url = sys.argv[1].strip()
    link = website_video_recovery(url)
    if link:
        print(f"Found URL: {link}")
    else:
        print("Unable to find the M3U8 URL.")