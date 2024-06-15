from apify_client import ApifyClient

# Initialize the ApifyClient with your Apify API token
client = ApifyClient("")

# Load URLs from the text file
urls = []
with open('reddit_urls.txt', 'r') as file:
    for line in file:
        urls.append(line.strip())

# Initialize lists to store post bodies and comment bodies
post_bodies = []

# Iterate over the URLs and scrape data using the Apify Reddit Scraper
for url in urls:
    # Prepare the Actor input
    run_input = {
        "startUrls": [{ "url": url }],
        "maxItems": 100,
        "maxPostCount": 5,
        "maxComments": 100,
        "maxCommunitiesCount": 1,
        "maxUserCount": 20,
        "scrollTimeout": 40,
        "proxy": {
            "useApifyProxy": True,
            "apifyProxyGroups": ["RESIDENTIAL"],
        },
    }

    # Run the Actor and wait for it to finish
    run = client.actor("trudax/reddit-scraper").call(run_input=run_input)

    # Fetch and print Actor results from the run's dataset (if there are any)
    print("💾 Check your data here: https://console.apify.com/storage/datasets/" + run["defaultDatasetId"])

    # Extract post body
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        post_body = item.get("body")
        post_bodies.append(post_body)
    
    # Write the scraped data to a text file after each URL
    with open('scraped_data10.txt', 'a') as file:
        file.write(f"Scraped data for URL: {url}\n")
        for post_body in post_bodies:
            file.write("%s\n" % post_body)
        file.write("\n")  # Add a newline to separate data from different URLs
        post_bodies = []  # Reset post_bodies for the next URL

print("Scraped data saved to scraped_data.txt")


