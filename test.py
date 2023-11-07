from gpt4free import GPT
from neo4j import GraphDatabase

# GPT-4 모델 로드
gpt = GPT()

def extract_keywords(text):
    response = gpt.generate(text)
    keywords = response.split(',')
    return keywords

class KeywordDatabase:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def add_keyword(self, keyword):
        with self._driver.session() as session:
            session.write_transaction(self._add_keyword, keyword)

    @staticmethod
    def _add_keyword(tx, keyword):
        tx.run("CREATE (k:Keyword {name: $keyword})", keyword=keyword)

# 사용 예시
db = KeywordDatabase("bolt://localhost:7687", "neo4j", "password")
keywords = extract_keywords("전문가의 메모 내용")
for keyword in keywords:
    db.add_keyword(keyword)
db.close()
