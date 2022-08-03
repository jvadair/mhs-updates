import twint
from pyndb import PYNDatabase
import json
import os, sys

class HideOutput:  # with HiddenPrints(): ...
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout
# Credit to Alexander C for the above code

def user(username: str, retries=1) -> dict:
    # Configure
    c = twint.Config()
    c.Username = username
    c.Limit = 10
    # c.Store_object = True
    c.Store_json = True
    c.Output = "TwitterRaw.json"
    # You will have to parse each line since each one is a separate json object

    # Run
    with HideOutput():
        twint.run.Search(c)

    # json parsing
    output = {}
    try:
        with open('TwitterRaw.json', 'r') as twOutput:
            for line in twOutput.readlines():
                data = dict(json.loads(line))
                ID = data.pop('id')
                output[str(ID)] = data
        os.remove('TwitterRaw.json')
    except:  # Tries until it works
        print(f'Failed to fetch twitter posts for {username}. Retry attempt #{retries}...')
        return user(username, retries=retries+1)
    return output

    # return c.Store_object_tweets_list


# # get by last few days version
# def user(username: str, days_amount=7) -> PYNDatabase:
#     # Configure
#     c = twint.Config()
#     c.Username = username
#     # c.Limit = 10
#     c.Store_json = True

#     today = DT.date.today()
#     week_ago = today - DT.timedelta(days=days_amount)
#     c.Since = week_ago.strftime("%Y-%m-%d")
#     c.Output = "TwitterRaw.json"
#     # You will have to parse each line since each one is a separate json object