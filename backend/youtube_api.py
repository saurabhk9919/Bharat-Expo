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
    DEVELOPER_KEY = os.getenv("YOUTUBE_API_KEY")  # Ensure this key is properly set

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY
    )

    request = youtube.playlistItems().list(
        part="snippet",
        playlistId="PLKnIA16_RmvYuZauWaPlRTC54KxSNLtNn",  # Update playlistId as needed
        maxResults=83  # Number of videos from the playlist
    )
    response = request.execute()

    # Debugging: Check response type and content
    print("Response data type:", type(response))
    print("Response content:", response)

    # Write response to JSON for backup
    try:
        with open('youtube_api.json', 'a') as f:
            json.dump(response, f, indent=4)
        print("Data appended successfully to youtube_api.json")

        with open('data.txt', 'a') as f:  # Append mode
            for item in response['items']:
                f.write(item['snippet']['title'] + '\n')
        print("Data appended successfully to data.txt")
    except Exception as e:
        print(f"Error writing data to file: {e}")

    # Extract and flatten relevant fields from response['items']
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

        # Create a DataFrame from the data
        df = pd.DataFrame(data)

        # Write to CSV in append mode, without overwriting existing data
        csv_file = 'youtube_api.csv'
        if os.path.isfile(csv_file):
            # Append mode; do not write header if the file already exists
            df.to_csv(csv_file, mode='a', header=False, index=False)
        else:
            # File does not exist, write with header
            df.to_csv(csv_file, index=False)
        
        print("Data appended successfully to youtube_api.csv")
    else:
        print("No items found in response.")

if __name__ == "__main__":
    main()