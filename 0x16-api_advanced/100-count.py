#!/usr/bin/python3
"""
    Recursive function that queries the Reddit API, parses the title of all hot
    articles, and prints a sorted count of given keywords (case-insensitive,
    delimited by spaces. Javascript should count as javascript, but java should
    not).
"""
import requests

def count_words(subreddit, word_list, after=None, word_count={}):
    if not word_list:
        return

    headers = {'User-Agent': 'Reddit Keyword Counter'}
    base_url = f'https://www.reddit.com/r/{subreddit}/hot.json'
    params = {'limit': 100}
    if after:
        params['after'] = after

    response = requests.get(base_url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        posts = data['data']['children']

        for post in posts:
            title = post['data']['title']
            for word in word_list:
                if title.lower().count(word.lower()):
                    if word in word_count:
                        word_count[word] += title.lower().count(word.lower())
                    else:
                        word_count[word] = title.lower().count(word.lower())

        new_after = data['data']['after']
        if new_after:
            count_words(subreddit, word_list, new_after, word_count)
        else:
            sorted_word_count = sorted(word_count.items(), key=lambda item: (-item[1], item[0]))
            for word, count in sorted_word_count:
                print(f'{word}: {count}')
    else:
        print("Subreddit not found or an error occurred.")

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print("Usage: {} <subreddit> <list of keywords>".format(sys.argv[0]))
        print("Ex: {} programming 'python java javascript'".format(sys.argv[0]))
    else:
        subreddit = sys.argv[1]
        keywords = [x.lower() for x in sys.argv[2].split()]
        count_words(subreddit, keywords)
