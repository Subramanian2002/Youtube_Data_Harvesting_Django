import pymongo
import psycopg2
from django.conf import settings
from datetime import datetime

def export_single_channel_to_postgres(channel_id):
    mongo_uri = settings.MONGO_URI
    client = pymongo.MongoClient(mongo_uri)
    db = client["YTH"]
    collection = db["channel_data"]
    record = collection.find_one({"channel_details.0.Channel_Id": channel_id})

    if not record:
        return False

    conn = psycopg2.connect(
        host=settings.POSTGRES["host"],
        port=settings.POSTGRES["port"],
        database=settings.POSTGRES["database"],
        user=settings.POSTGRES["user"],
        password=settings.POSTGRES["password"]
    )
    cursor = conn.cursor()

    # Check if already exists
    cursor.execute("SELECT 1 FROM channels WHERE channel_id = %s", (channel_id,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return False  # Already exists

    # Reuse same insert logic
    ch = record["channel_details"][0]
    cursor.execute("""
        INSERT INTO channels(channel_id, channel_name, channel_views, channel_description, channel_subscription_count)
        VALUES(%s, %s, %s, %s, %s)
    """, (
        ch["Channel_Id"],
        ch["Channel_Name"],
        int(ch["Channel_Views"]),
        ch["Channel_Description"],
        int(ch["Subscription_Count"])
    ))

    for pl in record["channel_playlists"]:
        cursor.execute("INSERT INTO playlist(playlist_id, channel_id, playlist_name) VALUES (%s, %s, %s)",
                       (pl["playlist_id"], pl["channel_id"], pl["playlist_name"]))

    for vid in record["video_details"]:
        cursor.execute("""
            INSERT INTO videos(video_id, channel_id, video_name, video_description, published_date,
                               view_count, like_count, favorite_count, comment_count, video_duration,
                               thumbnail, caption_satatus)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            vid["video_id"], vid["channel_id"], vid["video_name"], vid["video_description"],
            vid["publishedat"], int(vid["view_count"]), int(vid["like_count"]),
            int(vid["favorite_count"]), int(vid["comment_count"]), vid["video_duration"],
            vid["thumbnail"], vid["caption"]
        ))

    for com in record["comment_details"]:
        cursor.execute("""
            INSERT INTO comments(comment_id, video_id, comment_text, comment_author, comment_published_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            com["comment_id"], com["video_id"], com["comment_text"],
            com["comment_author"], datetime.strptime(com["comment_publishedat"], "%Y-%m-%dT%H:%M:%SZ")
        ))

    conn.commit()
    cursor.close()
    conn.close()
    return True
