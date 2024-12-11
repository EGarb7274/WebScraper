import praw
import re
import os
#This code will disguise the user when they want to insert their password
#import getpass

#secret_word = getpass.getpass(prompt="Enter your secret word: ")
#print(secret_word)

#Reddit takes theee paramaters clientID, Client_serivce, and user_agent Gotta figure out how to get these

reddit = praw.Reddit(
    client_id = "iYPjt2p4rrYeJsToM71vDA",
    client_secret = "qTiJfavOyzdq08y7XzCYlhwUbd39tg",
    user_agent = "my-app_by_u/Ok_Dealer1880",
    username = "Ok_Dealer1880",
    password = "#Yev818gar12",
)
subreddit = reddit.subreddit("WatchExchange")
prices = set()

while(True):
    mode = int(
        input("Would you like to search for a watch within a range (1), or search for sold listings of a watch? (2): "))
    if mode == 1:
        lookingPrice = int(input("Enter the price you'd like to look around: "))
        if lookingPrice >= 1000:
            lowerBound = (lookingPrice // 1000) * 1000
            upperBound = (lowerBound + 1000) - 1
        else:
            lowerBound = (lookingPrice // 100) * 100
            upperBound = (lowerBound + 100) - 1
        postFlair = str(f"${lowerBound}-${upperBound}")
        print("\n")
        break
    elif mode == 2:
        postFlair = "Sold"
        print("\n")
        break
    else:
        print("Incorrect value, enter either 1 or 2")

keyword = str(input("Enter the watch you would like to research: "))
for post in subreddit.search(keyword, sort="new", limit = 30):
    if post.link_flair_text == postFlair:
        print("Title - ", post.title)
        print("URL - ", post.url)
        fullUrl = f"https://www.reddit.com{post.permalink}"

        #grabs all the comments from their repsective posts and puts them into a txt file
        post.comments.replace_more(limit=None)
        all_comments = post.comments.list()
        autoMod_comments = [comment for comment in all_comments if comment.author and comment.author.name == "AutoModerator"]
        with open('example.txt', 'a', encoding='utf-8') as file:
            if len(autoMod_comments) >= 3:
                secondComment = autoMod_comments[1]
                thirdComment = autoMod_comments[2]
                file.write(thirdComment.body.replace(",", ""))
            else:
                secondComment = autoMod_comments[1]
            file.write(secondComment.body.replace(",", ""))

#Seraches the txt file searching for lines with a certain pattern
with open('example.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
    price_pattern = re.compile(r"\$(\d+(\.\d{1,2})?)")
    for line in lines:
        price_match = price_pattern.search(line)
        if price_match:
            price = price_match.group(1)
            prices.add(price)
#sorted(prices)
print("All prices found:", prices)

length = len(prices)
total = 0
avgPrice = 0
for item in prices:
    total += float(item)
avgPrice = total / length
sorted(prices)
print(f"\nThe average price for this watch is ${round(avgPrice, 2)} \nThe lowest price offered for this watch was $prices[0]")

os.remove('example.txt')

