SQL_QUERY_LIST = {
    "1": {
        "label": "1) What are the names of all the videos and their corresponding channels?",
        "query": """SELECT c.channel_name, v.video_name 
                    FROM channels c 
                    INNER JOIN videos v ON c.channel_id = v.channel_id;"""
    },
    "2": {
        "label": "2) Which channels have the most number of videos, and how many videos do they have?",
        "query": """SELECT c.channel_name, COUNT(v.video_id) AS video_count 
                    FROM channels c
                    INNER JOIN videos v ON c.channel_id = v.channel_id 
                    GROUP BY c.channel_name 
                    ORDER BY video_count DESC 
                    LIMIT 1;"""
    },
    "3": {
        "label": "3) What are the top 10 most viewed videos and their respective channels?",
        "query": """SELECT c.channel_name, v.video_name, v.view_count 
                    FROM videos v 
                    INNER JOIN channels c ON c.channel_id = v.channel_id 
                    ORDER BY v.view_count DESC 
                    LIMIT 10;"""
    },
    "4": {
        "label": "4) How many comments were made on each video, and what are their corresponding video names?",
        "query": "SELECT video_name, comment_count FROM videos;"
    },
    "5": {
        "label": "5) Which videos have the highest number of likes, and what are their corresponding channel names?",
        "query": """SELECT c.channel_name, v.video_name, v.like_count 
                    FROM videos v 
                    INNER JOIN channels c ON v.channel_id = c.channel_id 
                    ORDER BY v.like_count DESC 
                    LIMIT 10;"""
    },
    "6": {
        "label": "6) What is the total number of likes and what are their corresponding video names?",
        "query": "SELECT video_name, like_count FROM videos;"
    },
    "7": {
        "label": "7) What is the total number of views for each channel?",
        "query": """SELECT channel_name, channel_views 
                    FROM channels 
                    ORDER BY channel_views DESC;"""
    },
    "8": {
        "label": "8) Which channels have published videos in the year 2022?",
        "query": """SELECT DISTINCT c.channel_name 
                    FROM channels c 
                    INNER JOIN videos v ON c.channel_id = v.channel_id 
                    WHERE EXTRACT(YEAR FROM v.published_date) = 2022;"""
    },
    "9": {
        "label": "9) What is the average duration of all videos in each channel?",
        "query": """SELECT c.channel_name, AVG(v.video_duration) AS avg_duration 
                    FROM channels c 
                    INNER JOIN videos v ON c.channel_id = v.channel_id 
                    GROUP BY c.channel_name 
                    ORDER BY avg_duration DESC;"""
    },
    "10": {
        "label": "10) Which videos have the highest number of comments?",
        "query": """SELECT v.video_name, v.comment_count, c.channel_name 
                    FROM channels c 
                    INNER JOIN videos v ON c.channel_id = v.channel_id 
                    ORDER BY v.comment_count DESC 
                    LIMIT 10;"""
    }
}
