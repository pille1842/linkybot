#!/usr/bin/env python3
# Linkybot v1.0.1 by /u/pille1842
# GitHub: https://github.com/pille1842/linkybot
# See README.md for setup instructions

# Needed for logging the current time in the console
import datetime
# Well... duh
import praw
# Needed to pick a random submission from a subreddit
import random
# Needed to check if links are from known image hosters
import re

class Linkybot:
    def __init__(self, name):
        self.name     = name
        self.r        = praw.Reddit(name,
                        user_agent='praw:Linkybot:1.0.1 (by /u/pille1842)')
        # You can add more commands yourself. Simply add more elements to
        # the list, like this:
        #   self.commands = [('command','subreddit','template'),('command','subreddit','template')]
        # The bot will look for command in its mentions. Command must be lower-case
        # here but can be upper-case when the bot is mentioned. Subreddit must
        # be the name of one subreddit (or more subreddits chained together with +)
        # where the bot will look at 50 hot submissions and pick one to reply with.
        # You can customize the template, the bot will replace {url} with the
        # submission URL it picked.
        self.commands = [
                            ('pig',
                             'pigifs',
                             '**Oink Oink!** [Here is a random link]({url}) from /r/pigifs')
                        ]

        # This reply is sent when the bot was mentioned but didn't recognize any
        # command.
        self.error    = "I don't know that command. Try !Pig, for example."

        # This footer is appended to all messages the bot sends.
        self.footer   = "\n\n---\n\nI am a bot. BEEP BOOP"

        self.done     = []

    def run(self):
        while True:
            try:
                for mention in self.r.inbox.mentions(limit=25):
                    if mention.fullname in self.done:
                        continue
                    # Work around a bug: mentions don't have a submission attribute
                    # (see https://redd.it/5ggfz7)
                    comment = praw.models.Comment(self.r, id=mention.id)
                    comment.refresh()
                    comment.replies.replace_more()
                    answered = False
                    for reply in comment.replies:
                        if reply.author == self.name:
                            self.log('Skipping {} because I already commented'.format(comment.fullname))
                            answered = True
                            self.done.append(comment.fullname)
                            break
                    if answered:
                        continue
                    handled = False
                    for command, subreddit, template in self.commands:
                        if '!'+command not in mention.body.lower():
                            continue
                        sub   = self.r.subreddit(subreddit)
                        posts = sub.hot(limit=50)
                        postlist = []
                        for post in posts:
                            if post.is_self:
                                continue
                            if not re.match('(http|https)://[a-z]*\.?(imgur|gfycat|giphy)\.com', post.url):
                                continue
                            postlist.append(post.url)
                        url = random.choice(postlist)
                        mention.reply(template.format(url=url)+self.footer)
                        self.log('Replied to {mention} with {link}'.format(mention=mention.fullname,link=url))
                        handled = True
                    if not handled:
                        mention.reply(self.error+self.footer)
                        self.log('Replied to {mention} with error'.format(mention=mention.fullname))
                    self.done.append(mention.fullname)
            except praw.exceptions.APIException as e:
                self.log('Got an API exception: '+e.message)
            except praw.exceptions.ClientException as e:
                self.log('Got a client exception: '+e.message)

    def log(self, message):
        now = datetime.datetime.now()
        print(now.strftime('[%Y-%m-%d %H:%M:%S]'), '<{}>'.format(self.name), message)

if __name__ == '__main__':
    # Change the parameter to match your bot's username. You must also name the
    # configuration section in praw.ini like this.
    bot = Linkybot('MyBot')
    bot.run()
