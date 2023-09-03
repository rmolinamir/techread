import re
from math import ceil


class ArticleReadTimeEngine:
    @staticmethod
    def estimate_reading_time(article, words_per_minute=250, seconds_per_image=10, seconds_per_tag=2) -> int:
        word_count_title = ArticleReadTimeEngine._word_count(article.title)
        word_count_body = ArticleReadTimeEngine._word_count(article.body)
        word_count_description = ArticleReadTimeEngine._word_count(article.description)

        total_word_count = word_count_title + word_count_body + word_count_description

        reading_time = total_word_count / words_per_minute

        if article.banner_image:
            reading_time += seconds_per_image / 60

        tag_count = article.tags.count()
        reading_time += tag_count * seconds_per_tag / 60

        return ceil(reading_time)

    @staticmethod
    def _word_count(text: str) -> int:
        words = re.findall(r"\w+", text)
        num_words = len(words)
        return num_words
