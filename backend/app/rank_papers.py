# vector embedding list of papers with abstracts, and urls for access as identifier 
from sentence_transformers import SentenceTransformer 
from sentence_transformers import CrossEncoder 
from sklearn.metrics.pairwise import cosine_similarity

class embedding_model:
    def __init__(self, query_text, number_ranked_papers=10):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")
        self.query = query_text
        self.query_embedding = self._embed(query_text)
        self.number_ranked_papers = number_ranked_papers
        self.papers = None

    def rank_papers(self, papers):
        self.papers = papers
        if not papers or len(papers) == 0:
            return []
        top_papers = self._rank_by_similarity()

        scores = self.reranker.predict([(self.query, paper['abstract']) for paper in top_papers]) 
        # returns numpy array of relevance scores for each paper in top_papers. Higher score = more relevant.
        scored_papers = list(zip(scores,top_papers))
        scored_papers.sort(key= lambda x: x[0], reverse=True) # sort by relevance score, highest first
        return [paper for score, paper in scored_papers[:self.number_ranked_papers]] # return top N papers based on relevance score

    def _embed(self, text):
        return self.model.encode(text)
    
    def _rank_by_similarity(self):
        paper_embeddings = [self._embed(self.papers[i]['abstract']) for i in range(len(self.papers))]
        # cosine_similarity returns a 2D matrix of shape (num_queries, num_papers).
        # Since we only have ONE query, the result looks like: [[s1, s2, s3, ...]].
        # We use [0] to extract the first row so we get a simple 1D array of similarity scores.
        similarities = cosine_similarity([self.query_embedding], paper_embeddings)[0]
        ranked_indices = similarities.argsort()[::-1][:self.number_ranked_papers] # get top papers
        return [self.papers[i] for i in ranked_indices]