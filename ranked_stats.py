from riotwatcher import LolWatcher, ApiError


class RankedStats():
    def __init__(self, api_token, region):
        self.engine = LolWatcher(api_token)
        self.region = region

    def fetch_stats(self, summoner_name):
        try:
            response = self.engine.summoner.by_name(self.region, summoner_name)
            ranked_stats = self.engine.league.by_summoner(self.region, response['id'])
            return ranked_stats
        except ApiError as err:
            if err.response.status_code == 429:
                print('We should retry in {} seconds.'.format(err.headers['Retry-After']))
                print('this retry-after is handled by default by the RiotWatcher library')
                print('future requests wait until the retry-after time passes')
            elif err.response.status_code == 404:
                print('Summoner with that ridiculous name not found.')
            else:
                raise

        
