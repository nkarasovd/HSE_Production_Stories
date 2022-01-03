from typing import List

import gensim
import pyLDAvis
from gensim.models.ldamodel import LdaModel

from objects.tokenizer import Tokenizer


class LDAModel:
    def __init__(self, num_topics: int, tokenizer: Tokenizer,
                 raw_corpus: List[str], seed: int = 12345):
        self.num_topics = num_topics
        self.tokenizer = tokenizer
        self.seed = seed

        self.raw_corpus = [self.tokenizer(text) for text in raw_corpus]
        self.dicts = gensim.corpora.Dictionary(self.raw_corpus)
        self.corpus = [self.dicts.doc2bow(text) for text in self.raw_corpus]
        self.lda = LdaModel(self.corpus, self.num_topics, random_state=self.seed, id2word=self.dicts)

    def update_num_topics(self, num_topics: int):
        self.num_topics = num_topics
        self.lda = LdaModel(self.corpus, self.num_topics, random_state=self.seed, id2word=self.dicts)

    def get_vis(self):
        return pyLDAvis.gensim_models.prepare(self.lda, self.corpus, self.dicts, mds="mmds")

    def get_topics(self):
        topic_distribution = self.lda.get_document_topics(self.corpus)
        # return [sorted(x, key=lambda pair: -pair[1])[0][0] for x in topic_distribution]

        topics = []
        for x in topic_distribution:
            topics_sorted = sorted(x, key=lambda pair: -pair[1])
            if topics_sorted:
                topics.append(topics_sorted[0][0])
            else:
                topics.append(-1)

        return topics
