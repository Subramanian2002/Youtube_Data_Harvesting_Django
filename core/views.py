from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from .forms import ChannelForm
from .utils import fetch_all_data
from .sql_export import export_single_channel_to_postgres
import pymongo
from .sql_queries import SQL_QUERY_LIST
import psycopg2


def index(request):
    form = ChannelForm()
    data = None
    query_results = None
    columns = None
    selected_key = None

    # Connect to MongoDB
    mongo_uri = settings.MONGO_URI
    client = pymongo.MongoClient(mongo_uri,serverSelectionTimeoutMS=5000)
    db = client["YTH"]
    collection = db["channel_data"]

    # Dropdown channels from MongoDB
    all_channels = collection.find()
    channel_options = [
        {
            "name": ch["channel_details"][0]["Channel_Name"],
            "id": ch["channel_details"][0]["Channel_Id"]
        }
        for ch in all_channels
    ]

    # Handle channel fetch
    if request.method == "POST" and request.POST.get("action") == "fetch_channel":
        form = ChannelForm(request.POST)
        if form.is_valid():
            channel_id = form.cleaned_data['channel_id']
            if not channel_id:
                messages.warning(request, "Please enter a valid Channel ID.")
            else:
                existing = collection.find_one({"channel_details.Channel_Id": channel_id})
                if existing:
                    messages.info(request, "This channel already exists in MongoDB.")
                    data = existing
                else:
                    api_key = settings.API_KEY
                    data = fetch_all_data(api_key, channel_id)
                    if data:
                        collection.insert_one(data)
                        messages.success(request, "Channel data successfully fetched and stored in MongoDB.")
                    else:
                        messages.error(request, "Failed to fetch data. Please check the Channel ID or API Key.")

    # Handle SQL query selection
    if request.method == "POST" and request.POST.get("action") == "run_query":
        selected_key = request.POST.get("query_id")
        if selected_key in SQL_QUERY_LIST:
            query = SQL_QUERY_LIST[selected_key]["query"]

            conn = psycopg2.connect(
                host=settings.POSTGRES["host"],
                port=settings.POSTGRES["port"],
                database=settings.POSTGRES["database"],
                user=settings.POSTGRES["user"],
                password=settings.POSTGRES["password"]
            )
            cursor = conn.cursor()
            cursor.execute(query)
            query_results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            cursor.close()
            conn.close()

    return render(request, 'core/index.html', {
        'form': form,
        'data': data,
        'channel_options': channel_options,
        'query_list': SQL_QUERY_LIST,
        'selected_key': selected_key,
        'results': query_results,
        'columns': columns,
    })


# ✅ Export a selected channel from MongoDB to PostgreSQL
def export_selected_channel(request):
    if request.method == "POST":
        channel_id = request.POST.get("selected_channel")
        if channel_id:
            export_single_channel_to_postgres(channel_id)
            messages.success(request, "Selected channel data successfully exported to PostgreSQL.")
        else:
            messages.error(request, "No channel selected.")
    return redirect("index")


def sql_query_view(request):
    results = None
    selected_key = None

    if request.method == "POST":
        selected_key = request.POST.get("query_id")
        if selected_key in SQL_QUERY_LIST:
            sql = SQL_QUERY_LIST[selected_key]["query"]

            conn = psycopg2.connect(
                host=settings.POSTGRES["host"],
                port=settings.POSTGRES["port"],
                database=settings.POSTGRES["database"],
                user=settings.POSTGRES["user"],
                password=settings.POSTGRES["password"]
            )
            cursor = conn.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            cursor.close()
            conn.close()

            return render(request, "core/sql_query.html", {
                "query_list": SQL_QUERY_LIST,
                "selected_key": selected_key,
                "results": results,
                "columns": columns
            })

    return render(request, "core/sql_query.html", {
        "query_list": SQL_QUERY_LIST,
        "selected_key": selected_key
    })
