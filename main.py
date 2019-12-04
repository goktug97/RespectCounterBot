#!/usr/bin/env python

import re
import time
import sys

import praw

reddit = praw.Reddit('respectcounterbot')
subreddits = [
    '2meirl4meirl',
    'donthelpjustfilm',
    'garlicbreadmemes',
    'gifs',
    'greentext',
    'gifsthatkeepongiving',
    'hitanimals',
    'holdmyfeedingtube',
    'instantkarma',
    'justfuckmyshitup',
    'prequelmemes',
    'nononono',
    'rareinsults',
    'trebuchetmemes',
    'unexpected',
    'watchpeopledieinside',
    'wellthatsucks',
    'whatcouldgowrong',
    'programmerhumor',
    'respectbottest',
    'murderedbywords',
    'suicidebywords',
    'memes',
    'me_irl',
    'funny']

for subreddit_name in subreddits:
    subreddit = reddit.subreddit(subreddit_name)
    for submission in subreddit.hot(limit=50):
        submission.comments.replace_more(limit=0)
        comments = submission.comments
        bot_comment = None
        old_respect = 0
        for comment in comments:
            if (author:=comment.author) is not None:
                author_name = author.name
                if 'RespectCounterBot'== author_name:
                    bot_comment = comment
                    try:
                        old_respect = int(bot_comment.body.split(' ')[2])
                    except IndexError:
                        # This should never happen
                        pass
                    break
        respect = 0
        for comment in comments.list() :
            body = comment.body
            body = body.lower()
            if body.startswith('f') and body.endswith('f') and len(body) == 1:
                respect += comment.score

        reply = f"Total Respect: {respect} \n\n"
        reply = f"{reply}I'm just a simple bot trying to make my way in the universe.\n\n"
        reply = f"{reply}^Source ^Code: ^https://github.com/goktug97/RespectCounterBot\n"
        while True:
            try:
                if respect > 10 and respect != old_respect:
                    if bot_comment is None:
                        submission.reply(reply)
                    else:
                        bot_comment.edit(reply)
                print(f'{reply}Link: {submission.permalink}')
                break
            except praw.exceptions.APIException as exception:
                msg = exception.message.lower()
                search = re.search(r'\b(minutes)\b', msg)
                minutes = int(msg[search.start()-2]) + 1
                wait = time.time() + minutes*60
                while True:
                    remaining = wait - time.time()
                    if remaining < 0:
                        break
                    else:
                        sys.stdout.write('\x1b[2K')
                        print(f'Limit Remaining Time:{remaining}', end='\r')
                        time.sleep(1)
