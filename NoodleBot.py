import praw
import random
import re
from praw.models import Comment

reddit = praw.Reddit('bot1')

# List of words NoodleBot will look for
KEYWORDS_IN_TITLE = ['noodle', 'ramen', 'spaghetti', 'orzo', 'ravioli', 'linguine', 'macaroni',
                     'fettuccine', 'penne', 'ziti', 'lasagna', "mac and cheese", 'rigatoni', 'pasta']

# List to store post id's
POSTS_ALREADY_RESPONDED_TO = []

# List to store author names
AUTHORS_RESPONDED_TO = []


# Function that reads lines from a text file and returns a random line's string
def bot_responses(text_file):
    with open(text_file) as f:
        lines = f.readlines()
        return random.choice(lines)


# Function that will search posts on a given subreddit for keywords within the title and respond with a catchphrase
def post_search(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)  # store the subreddit to a variable

    for submission in subreddit.new(limit=10):  # Loop through the 10 newest posts in given subreddit
        for j in KEYWORDS_IN_TITLE:  # loop through keywords to search for posts
            if submission.id in POSTS_ALREADY_RESPONDED_TO:
                break
            if re.search(j, submission.title, re.IGNORECASE):
                submission.reply(bot_responses("catchphrases.txt"))  # reply to the post with a catchphrase
                print("Noodle Bot replying to:", submission.title, ", in subreddit", subreddit)  # print to console
                POSTS_ALREADY_RESPONDED_TO.append(submission.id)  # add post id to list
                break


# function that checks inbox and responds to new comment replies and responds based on if the given author has
# replied to NoodleBot before.
def comment_reply():
    for mail in reddit.inbox.unread():  # loop through unread mail
        if isinstance(mail, Comment):  # if unread mail is a comment
            if str(mail.author) not in AUTHORS_RESPONDED_TO:  # if author to comment reply isn't stored to text file
                mail.reply(  # response to their comment reply
                    "Dear friend I am just a bot and not a smart one either so I have no words for your message. "
                    "If you truly must speak to me try messaging /u/foorast he's my creator and the reason I crave "
                    "noodles so much.")
                print("I have responded to:", mail.author)  # print to console what was done
                AUTHORS_RESPONDED_TO.append(str(mail.author))  # add authors name to the array
                mail.mark_read()  # mark the message as read
            else:
                mail.reply(bot_responses("multiple_replies.txt"))  # reply with a random response from array
                print("I have responded again to:", mail.author)  # print what happened to console
                mail.mark_read()  # mark message as read


if __name__ == "__main__":
    post_search("foodporn")
    comment_reply()
