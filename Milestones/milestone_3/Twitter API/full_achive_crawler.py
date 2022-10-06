from datetime import datetime
from pprint import pprint
import logging
from time import sleep
import requests
from dateutil.relativedelta import relativedelta


AUTH_CONFIG = {
    'bearer_token': 'XXX',
}

GENERAL_CONFIG = {
    'search_endpoint': 'https://api.twitter.com/2/tweets/search/all',
    'base_date': datetime(2021, 11, 1),
    'months_to_fetch': 15,
    'write': True,
    'print': False,
    'output_path': 'outputs',
    'file_name': 'tweets_vaccines',
    'extension': 'json',
    'max_tweets_per_file': 20000,
    'max_tweets_to_fetch': 100000,
}

API_CONFIG_MASKS = {
    'query': '(#covid OR #masks ) mask -is:retweet lang:en -sale -is:verified -is:nullcast -available -shop -#gaming -premium -#nft -#soft -#sale -#giveaway -#handmade -#fashion lang:en',
    'tweet.fields': 'author_id,created_at',
    'max_results': 500,
}

API_CONFIG_VACCINES = {
    'query': '(#covid OR #vaccine OR #CovidIsNotOver) covid vaccine -is:retweet lang:en -sale -is:verified -is:nullcast -available -shop -#gaming  -#nft  -#giveaway -#TedCruz -#submarines -discount -online -@YouTube -news -tracker -#china -#russia -#ukraine -watch -book -miramar -@GeorgiaOnline1 -#terrorism',
    'tweet.fields': 'author_id,created_at',
    'max_results': 500,
}
API_CONFIG = API_CONFIG_VACCINES

class SearchApiWrapper:
    def __init__(self, parser: DataParser, http_client: TwitterHttpClient, writer: DataWriterFactory):
        # self.writer = writer
        self.parser = parser
        self.http_client = http_client
        self.writer = writer

    def fetch(self, params):
        tweets = []
        iterations = 1

        try:
        # Load first request
            print('Loading first batch')
            tweets, next_token = self._fetch(params)
            fetched_tweets = len(tweets)

            while next_token and fetched_tweets < GENERAL_CONFIG['max_tweets_to_fetch']:
                if iterations >= 300:
                    print('Sleeping 15m to avoid reaching API limits')
                    sleep(60 * 10)
                    iterations = 0
                sleep(1)
                iterations += 1

                # Loads next batch
                print(f'Loading batch {iterations}')
                new_tweets, next_token = self._fetch(params, next_token)
                tweets = [*tweets, *new_tweets]
                fetched_tweets += len(new_tweets)
                print(f'Batch complete - {len(new_tweets)} tweets loaded')
                print(f'Total loaded: {fetched_tweets}/{GENERAL_CONFIG["max_tweets_to_fetch"]}')
                if not next_token:
                    print('Data load complete - no next page')

                if GENERAL_CONFIG['print']:
                    pprint(new_tweets)

                # Stores data when/if
                if GENERAL_CONFIG['write'] and len(tweets) >= GENERAL_CONFIG['max_tweets_per_file']:
                    print(f'Length of tweets in memory {len(tweets)} - writing')
                    self._write(tweets)
                    tweets = []
            else:
                if tweets:
                    print(f'Execution complete, writing last {len(tweets)} tweets')
                    self._write(tweets)

        except Exception as e:
            print(e)
            self._write(tweets)

        finally:
            print(f'Completed in {iterations} API calls')
            return iterations

    def _fetch(self, params, next_token=None):
        request_params = {
            **params,
            'next_token': next_token,
        } if next_token else params
        data = self.http_client.request(
            endpoint=GENERAL_CONFIG['search_endpoint'],
            params=request_params,
            auth_dict=AUTH_CONFIG,
        )
        return self.parser.parse(data)

    def _write(self, data):
        self.writer.write_new(data)


class TwitterHttpClient:
    def request(self, endpoint, auth_dict, method="GET", params={}):
        """
        Aiohttp fetch request wrapper
        """

        def bearer_oauth(r):
            """
            Method required by bearer token authentication.
            """

            r.headers['Authorization'] = f'Bearer {auth_dict["bearer_token"]}'
            r.headers['User-Agent'] = 'v2FullArchiveSearchPython'
            return r

        resp = requests.request(method=method, url=endpoint, auth=bearer_oauth, params=params)

        if resp.status_code != 200:
            print('Unable to get data')
            print("RH Call failed: {}: {}".format(resp.status_code, resp.json()))

            # Raise the appropriate exception
            raise HTTPClientException()
        return resp.json()

class DataParser:
    def parse(self, response):
        data = response.get('data', [])
        tweets = [self._parse_tweet(entry) for entry in data]
        return tweets, response.get('meta', {}).get('next_token')

    def _parse_tweet(self, tweet):
        return {
            # add other fields here
            'author_id': tweet.get('author_id'),
            'created_at': tweet.get('created_at'),
            'id': tweet.get('id'),
            'text': tweet.get('text'),
        }

class DataWriterFactory:
    class _DataWriter:
        def __init__(self, file_name):
            self.file = open(file_name, "w")

        def write(self, data):
            json.dump(data, self.file)

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.file.close()

    def __init__(self, path, file_name, extension):
        self.written_files = 0
        self.path = path
        self.file_name = file_name
        self.extension = extension

    def write_new(self, data):
        self._DataWriter(f'{self.path}/{self.file_name}_{self.written_files}.{self.extension}').write(data)
        self.written_files += 1


# main part

if __name__ == "__main__":
    iterations = 0
    base_date = GENERAL_CONFIG['base_date']
    base_date = base_date.replace(tzinfo=pytz.UTC)
    dates = [
        base_date + relativedelta(months=i) for i in range(GENERAL_CONFIG['months_to_fetch'])
    ]
    for dt in dates:
        if iterations >= 300:
            print('Sleeping 15m to avoid reaching API limits')
            sleep(60*10)
            iterations = 0
        sleep(1)
        print('\n-----------------------')
        print(f'Loading data for date: {dt}')
        api_wrapper = SearchApiWrapper(
            parser=DataParser(),
            http_client=TwitterHttpClient(),
            writer=DataWriterFactory(
                GENERAL_CONFIG['output_path'],
                f'{GENERAL_CONFIG["file_name"]}_{dt.strftime("%B")}_{dt.strftime("%Y")}',
                GENERAL_CONFIG['extension'],
            ),
        )

        iterations += api_wrapper.fetch({
            **API_CONFIG,
            'start_time': dt.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'end_time': (dt + relativedelta(months=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
        })