
from utils.social_sites.reddit import RedditAPI
from utils.sentiment_analyzer import ChatGPTSentimentAnalyzer
class RedditService:
    
    def fetch_hot_posts(self, topic):
        comments = RedditAPI().fetch_hot_posts(topic)
        # comments = [comment for post in posts for comment in post.comments.list()]
        classified_comments = ChatGPTSentimentAnalyzer().classify_comments_with_gpt3(comments)
        summary = self.summarize_results(classified_comments)
        return {"comments": comments, "summary": summary}

    
    def summarize_results(self, classified_comments):
        summary = {
            'in_favor': {'total': 0, 'arguments': {}},
            'against': {'total': 0, 'arguments': {}},
            'neutral': 0
        }

        def identify_arguments(comments):
            arguments = {}
            for comment in comments:
                doc = comment
                if doc in arguments:
                    arguments[doc].append(comment)
                else:
                    arguments[doc] = [comment]
            return arguments

        # In favor comments
        in_favor_comments = classified_comments['in_favor']
        summary['in_favor']['total'] = len(in_favor_comments)
        summary['in_favor']['arguments'] = identify_arguments(in_favor_comments)

        # Against comments
        against_comments = classified_comments['against']
        summary['against']['total'] = len(against_comments)
        summary['against']['arguments'] = identify_arguments(against_comments)

        # Neutral comments
        summary['neutral'] = len(classified_comments['neutral'])

        return summary