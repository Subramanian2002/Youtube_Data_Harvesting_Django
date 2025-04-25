from googleapiclient.discovery import build
from isodate import parse_duration
from datetime import datetime


def get_youtube_client(api_key):
    return build('youtube', 'v3', developerKey=api_key)


def channel_info(youtube, channel_ids):
    channels = []
    request = youtube.channels().list(part='snippet,statistics,contentDetails', id=channel_ids)
    response = request.execute()
    item = response['items'][0]
    data = {
        "Channel_Name": item['snippet']['title'],
        "Channel_Id": item['id'],
        "Channel_Description": item['snippet']['description'],
        "Channel_Views": item['statistics']['viewCount'],
        "Subscription_Count": item['statistics']['subscriberCount'],
        "Playlist_Id": item['contentDetails']['relatedPlaylists']['uploads'],
        "Playlist_Name": item['snippet']['title']
    }
    channels.append(data)
    return channels


def playlist(youtube, channel_id):
    playlists = []
    next_page_token = None
    while True:
        request = youtube.playlists().list(
            part='snippet,contentDetails',
            channelId=channel_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()
        for pl in response.get('items', []):
            playlists.append({
                "channel_id": pl['snippet']['channelId'],
                "playlist_id": pl['id'],
                "playlist_name": pl['snippet']['title']
            })
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    return playlists


def video_info(youtube, channel_id):
    request = youtube.channels().list(id=channel_id, part='contentDetails')
    response = request.execute()

    playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    videos_details = []
    next_page_token = None

    while True:
        video_id_request = youtube.playlistItems().list(
            playlistId=playlist_id,
            part='snippet',
            maxResults=50,
            pageToken=next_page_token
        )
        video_id_response = video_id_request.execute()
        for item in video_id_response.get('items', []):
            try:
                video_id = item['snippet']['resourceId']['videoId']
                video_response = youtube.videos().list(
                    part='snippet,contentDetails,statistics',
                    id=video_id
                ).execute()

                if not video_response.get("items"):
                    continue

                video_data = video_response['items'][0]
                stats = video_data.get('statistics', {})
                snippet = video_data.get('snippet', {})
                content = video_data.get('contentDetails', {})

                videos_details.append({
                    "video_id": video_data['id'],
                    "channel_id": snippet.get('channelId', ''),
                    "video_name": snippet.get('title', ''),
                    "video_description": snippet.get('description', ''),
                    "video_duration": int(parse_duration(content.get('duration', 'PT0S')).total_seconds()),
                    "publishedat": datetime.strptime(snippet['publishedAt'], "%Y-%m-%dT%H:%M:%SZ"),
                    "view_count": int(stats.get('viewCount', 0)),
                    "like_count": int(stats.get('likeCount', 0)),
                    "dislike_count": max(int(stats.get('viewCount', 0)) - int(stats.get('likeCount', 0)), 0),
                    "favorite_count": int(stats.get('favoriteCount', 0)),
                    "comment_count": int(stats.get('commentCount', 0)),
                    "thumbnail": snippet.get('thumbnails', {}).get('default', {}).get('url', ''),
                    "caption": content.get('caption', 'false')
                })
            except Exception as e:
                print(f"Error in video parsing: {e}")
        next_page_token = video_id_response.get('nextPageToken')
        if not next_page_token:
            break
    return videos_details


def comment_info(youtube, video_ids):
    comments = []
    for vid in video_ids:
        try:
            response = youtube.commentThreads().list(
                part='snippet',
                videoId=vid,
                textFormat='plainText',
                maxResults=50
            ).execute()
            for item in response['items']:
                snippet = item['snippet']['topLevelComment']['snippet']
                comments.append({
                    "comment_id": item['id'],
                    "video_id": item['snippet']['videoId'],
                    "comment_text": snippet['textDisplay'],
                    "comment_author": snippet['authorDisplayName'],
                    "comment_publishedat": snippet['publishedAt']
                })
        except Exception as e:
            print(f"Error in fetching comments for {vid}: {e}")
    return comments


def fetch_all_data(api_key, channel_id):
    youtube = get_youtube_client(api_key)
    channel = channel_info(youtube, channel_id)
    playlists = playlist(youtube, channel_id)
    videos = video_info(youtube, channel_id)
    video_ids = [v['video_id'] for v in videos]
    comments = comment_info(youtube, video_ids)
    return {
        'channel_details': channel,
        'channel_playlists': playlists,
        'video_details': videos,
        'comment_details': comments
    }
