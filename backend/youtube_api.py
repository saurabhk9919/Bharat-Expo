import os
import json
from dotenv import load_dotenv
import googleapiclient.discovery
import pandas as pd

load_dotenv()

def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.getenv("YOUTUBE_API_KEY")  # Make sure this key is properly set

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY
    )

    request = youtube.playlistItems().list(
        part="snippet",
        # playlistId="PLKnIA16_RmvYuZauWaPlRTC54KxSNLtNn",
        playlistId="PLF_7kfnwLFCE-Ez19Bpn-pmE7wjBmx7Ix",
        maxResults=14            # For the number of videos from the playlist
    )
    response = request.execute()

    # Debugging: Check response type and content
    print("Response data type:", type(response))
    print("Response content:", response)

    # Try writing to the JSON file
    try:
        with open('youtube_api.json', 'a') as f:
            json.dump(response, f, indent=4)
        print("Data written successfully to youtube_api.json")

        with open('data.txt', 'w') as f:
            for item in response['items']:
                f.write(item['snippet']['title'] + '\n')
        print("Data written successfully to data.txt")
    except Exception as e:
        print(f"Error writing data to file: {e}")

    # Extract and flatten the relevant fields from response['items']
    if 'items' in response:
        data = []
        for item in response['items']:
            snippet = item.get('snippet', {})
            data.append({
                'title': snippet.get('title', ''),
                'description': snippet.get('description', ''),
                'publishedAt': snippet.get('publishedAt', ''),
                'channelTitle': snippet.get('channelTitle', ''),
                'videoId': snippet.get('resourceId', {}).get('videoId', '')
            })

        # Create a DataFrame and write to CSV
        df = pd.DataFrame(data)
        df.to_csv('youtube_api.csv', index=False)
        print("Data written successfully to youtube_api.csv")
    else:
        print("No items found in response.")

if __name__ == "__main__":
    main()