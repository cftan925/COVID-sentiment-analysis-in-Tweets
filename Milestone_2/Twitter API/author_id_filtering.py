from full_achive_crawler import GENERAL_CONFIG, AUTH_CONFIG, API_CONFIG
from full_achive_crawler import TwitterHttpClient
from full_achive_crawler import chunk
from full_achive_crawler import DataFilter
from full_achive_crawler import DataParser
from full_achive_crawler import FileUtils
from time import sleep
from os import listdir
from os.path import isfile, join


AUTH_CONFIG = {
    'bearer_token': 'XXX',
}

GENERAL_CONFIG = {
    'write': True,
    'print': False,
    'output_path': 'output',
    'input_path': 'input',
    'users_endpoint': "https://api.twitter.com/2/users",
}

API_CONFIG = {
    'ids': [],
    'user.fields': 'public_metrics'
}

FILTER_CONFIG = {
    'following_min': 5,
    'following_max': 1500,
    'followed_min': 5,
    'followed_max': 1500,
}

logger = logging.getLogger(__name__)

MAX_AUTHOR_API_CHUNK_SIZE = 100
MAX_CALLS_PER_15M = 250


class TwitterFilterService:
    def __init__(self, filter: DataFilter, http_client: TwitterHttpClient, file_utils: FileUtils, parser: DataParser, iterations: int):
        self.iterations = iterations
        self.filter = filter
        self.http_client = http_client
        self.file_utils = file_utils
        self.parser = parser

    def run(self):
        # Load tweets
        print(f'Loading tweets file')
        tweets = self.file_utils.load_tweets()

        # Open file & setify
        print(f'Generating set of users')
        author_ids = self.parser.get_authors_from_tweets(tweets)
        print(f'{len(author_ids)} otal users found')

        # Load each author
        print(f'Loading users metadata')
        iterations, authors = self._fetch_authors(author_ids)

        # Filter out
        print(f'Filtering out tweets not meeting users criteria')
        filtered_tweets = self.filter.filter(authors, tweets)
        print(f'Tweets filtered - {len(filtered_tweets)}/{len(tweets)} kept')

        # Write filtered
        print('Writing tweets to new file')
        self.file_utils.write_filtered(filtered_tweets)

        return iterations

    def _fetch_authors(self, author_ids):
        author_ids_chunks = list(chunk(list(author_ids), MAX_AUTHOR_API_CHUNK_SIZE))
        authors = dict()
        print(f'Authors total: {len(author_ids)} - will run {len(author_ids_chunks)} API calls')

        iterations = self.iterations

        for num, author_ids_chunk in enumerate(author_ids_chunks):
            sleep(2)
            if iterations >= MAX_CALLS_PER_15M:
                sleep(60*15)
                print('Sleeping 15 to maintain API limits')
                iterations = 0
            print(f'Running API call {num+1}/{len(author_ids_chunks)}')
            try:
                data = self.http_client.request(
                    endpoint=GENERAL_CONFIG['users_endpoint'],
                    params=self._build_params(author_ids_chunk),
                    auth_dict=AUTH_CONFIG,
                )
            except Exception as e:
                print(f'Failed to load due to expcetion {e} -- will sleep and retry')
                sleep(60*15)
                data = self.http_client.request(
                    endpoint=GENERAL_CONFIG['users_endpoint'],
                    params=self._build_params(author_ids_chunk),
                    auth_dict=AUTH_CONFIG,
                )
            authors = {**authors, **self.parser.get_authors_with_meta(data)}

        return iterations, authors

    def _build_params(self, users_list):
        return {
            **API_CONFIG,
            'ids': ','.join(users_list)
        }

    def _setify(self, tweets):
        return self.parser.get_authors_from_tweets(tweets)

MAX_CALLS_PER_15M = 200


if __name__ == "__main__":
    iterations = 0

    # Find all input files in input folder
    input_files = [f for f in listdir(GENERAL_CONFIG['input_path']) if isfile(join(GENERAL_CONFIG['input_path'], f))]

    for file_name in input_files:
        sleep(1)
        if iterations >= MAX_CALLS_PER_15M:
            sleep(60*15)
            iterations = 0

        filter_service = TwitterFilterService(
            parser=DataParser(),
            http_client=TwitterHttpClient(),
            file_utils=FileUtils(
                GENERAL_CONFIG['output_path'],
                GENERAL_CONFIG['input_path'],
                file_name,
            ),
            filter=DataFilter(),
            iterations=iterations,
        )

        iterations += filter_service.run()

# calculating corpus size

FILE_PATH = 'output'

def load_tweets(file_name):
    file_name = f'output/{file_name}'

    print(file_name)
    with open(file_name, "r") as f:
        return json.load(f)

file_names = [f for f in listdir(FILE_PATH) if isfile(join(FILE_PATH, f))]

for f in file_names:
    tweets = load_tweets(f)
    print(f'File: {f} -- Tweets: {len(tweets)}')
