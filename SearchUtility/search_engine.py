import json

from Settings import data_path


class SearchEngine(object):
    """
    Search engine for book search
    """

    def __init__(self):
        """
        load the data to memory, to speed up search
        need to see performance with more data
        """
        with open(data_path + '/data.json', 'r') as jsonfile:
            self.records = json.load(jsonfile)

    def search_for(self, keywords, max_items):
        """
        Search for the given keywords
        :param keywords: list of keywords
        :param max_items: max results to return
        :return:
        """
        query_result = {}
        scores = {}

        # score all books for the given query
        for record in self.records['summaries']:
            score = self.run_algo_on(record['summary'], keywords)
            scores[(record['summary'], record['id'])] = score

        # sort the score to pick best ones
        sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        ret = json.dumps((dict(dict(sorted_scores[:max_items]).keys())))
        return ret

    def run_algo_on(self, record, keywords):
        normalizer = 50  # to normalize the result, this can be decreased once algo is optimized to remove stopwords
        base_score = sum(1 for val in keywords.split() if val in record)  # matches of words in record

        additional_score = sum(1 for val in record.split() if val in keywords)  # count of words

        final_score = base_score + (additional_score / normalizer)  # simple algorithm

        return final_score
