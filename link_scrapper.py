import praw

# Authenticate with Reddit API
reddit = praw.Reddit(client_id='',
                     client_secret=',
                     user_agent=')

# Replace 'YOUR_SUBREDDIT_NAME' with the subreddit you want to fetch posts from
subreddit = reddit.subreddit('LUMS')

# Create a list to store URLs
urls = []

# Get posts from the subreddit
for submission in subreddit.new(limit=1000):  # Change 'limit' to however many posts you want to fetch
    urls.append(submission.url) 
    print("scrapped",submission.url) # Append the URL of each post to the list

# Save URLs to a text file
with open('reddit_urls.txt', 'w') as file:
    for url in urls:
        file.write("%s\n" % url)

print("URLs saved to reddit_urls.txt")
