import praw
import os
import csv
import sys


def create_subreddit_list():
    # --- Reddit API Authentication ---
    # Ensure your environment variables are set for authentication
    try:
        reddit = praw.Reddit(
            client_id=os.getenv("client_id"),
            client_secret=os.getenv("client_secret"),
            password=os.getenv("password"),
            user_agent="testscript by u/yourusername",
            username=os.getenv("username"),
        )
        # Validate authentication
        print(f"Successfully authenticated as u/{reddit.user.me()}")
    except Exception as e:
        print(f"Authentication failed: {e}")
        print("Please ensure your environment variables (client_id, client_secret, password, username) are set correctly.")
        sys.exit()

    # --- Configuration ---
    search_keywords = ["robotics", "robot", "robots", "humanoid"]
    csv_file_name = "subreddits.csv"

    # --- Check if file already exists ---
    if os.path.exists(csv_file_name):
        print(f"\nError: Output file '{csv_file_name}' already exists.")
        print("Halting script to prevent overwriting. Please move or delete the file if you wish to run a new search.")
        return

    # --- Searching for Subreddits ---
    # Use a dictionary to store unique subreddit names and their links
    found_subreddits = {}
    print("\nSearching for subreddits...")
    for keyword in search_keywords:
        print(f"Searching for '{keyword}'...")
        # Search for subreddits matching the keyword
        for subreddit in reddit.subreddits.search(keyword):
            # Construct the full URL
            subreddit_url = f"https://www.reddit.com/r/{subreddit.display_name}"
            # Add the name and URL to the dictionary. Duplicates are automatically handled.
            found_subreddits[subreddit.display_name] = subreddit_url

    print(f"\nFound {len(found_subreddits)} unique subreddits.")

    # --- Saving to CSV ---
    print(f"Saving subreddits to {csv_file_name}...")
    try:
        with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Write the new header row with two columns
            writer.writerow(["Subreddit", "Link"])
            
            # Sort the results alphabetically by subreddit name before writing
            for name, link in sorted(found_subreddits.items()):
                # Write the name and the link to the CSV
                writer.writerow([name, link])
                
        print("Done!")
    except IOError as e:
        print(f"\nError writing to file: {e}")
        sys.exit()


if __name__ == "__main__":
    create_subreddit_list()