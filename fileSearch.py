import os
import re

class SearchTool:

    def __init__(self, base_path="docs", name="file_search"):
        self.name = "file_search"
        self.description = """Finds WHICH files exist in the docs folder.
USE THIS FIRST if you don't know the exact filename or if you are looking 
for a topic (e.g., 'diet', 'budget') but don't know where it is.
DO NOT use this to read the actual content of a report.""".strip()
        self.base_path = base_path

    def expand_keywords(self, query):
        words = re.findall(r"\w+", query.lower())

        #print(f"---------- inside ST,query: {query}------------\n ")

        expansions = {
            "invite": ["invited", "invitation", "guest", "attendee"],
            "invited": ["invite", "invitation", "guest"],
            "guest": ["invite", "invitation"],
            "meeting": ["schedule", "appointment"]
        }

        keywords = set(words)

        #print(f"---------- inside ST,keywords: {keywords}------------\n ")

        for w in words:
            if w in expansions:
                keywords.update(expansions[w])

        return list(keywords)

    def run(self, query: str):

        if not query:
            return {"keywords": [], "files": [], "error": "No query provided"}

        keywords = self.expand_keywords(query)

        STOPWORDS = {
        "a", "an", "the", "and", "or", "but", "if", "while",
        "of", "at", "by", "for", "with", "about", "against",
        "between", "into", "through", "during", "before",
        "after", "above", "below", "to", "from", "up", "down",
        "in", "out", "on", "off", "over", "under", "again",
        "further", "then", "once", "here", "there", "when",
        "where", "why", "how", "all", "any", "both", "each",
        "few", "more", "most", "other", "some", "such", "no",
        "nor", "not", "only", "own", "same", "so", "than",
        "too", "very", "can", "will", "just", "don", "should",
        "now", "are", "who", "what", "is", "am", "be"
        }

        filtered_keywords = [kw for kw in keywords if kw not in STOPWORDS]

        scores = {}

        for file in os.listdir(self.base_path):

            path = os.path.join(self.base_path, file)

            if not os.path.isfile(path):
                continue

            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read().lower()

                score = 0

                for kw in filtered_keywords:
                    if kw in content or kw in file.lower():
                        score += 1

                if score > 0:
                    scores[file] = score

            except:
                continue

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        

        files = [f for f, s in ranked]

        print("\n------ inside search: --- Expanded Keywords:")
        print(filtered_keywords)

        print("\nn------ inside search: --- Matching Files:")
        print(files)

        #return {
        #    "keywords": filtered_keywords,
        #    "files": files
        #}

        if len(filtered_keywords)>0:
            return f"SEARCH RESULTS: Found the following relevant files: {', '.join(files)}. You should now use file_reader to read one of these."
        else:
            return "SEARCH RESULTS: No files found for that keyword. Try a different keyword or list all files."



# ---------------- TEST MAIN ----------------
if __name__ == "__main__":

    docs_path = "docs"
    search_tool = SearchTool(docs_path)

    while True:

        query = input("\nEnter search query (or 'exit'): ")

        if query.lower() == "exit":
            break

        result = search_tool.run(query)

        print("\nExpanded Keywords:")
        print(result["keywords"])

        print("\nMatching Files:")
        print(result["files"])