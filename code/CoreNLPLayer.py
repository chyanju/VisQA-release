import nltk
import nltk.parse.corenlp as cnlp
import nltk.parse.stanford as snlp
import urllib.parse


class QueryParser:
	CORENLP_SERVER = "http://localhost:9000"

	def __init__(self):
		self.parser = cnlp.CoreNLPParser(url = self.CORENLP_SERVER)
		self.dependency_parser = cnlp.CoreNLPDependencyParser(url = self.CORENLP_SERVER)
		self.cache = {}

	def syntactic_parse(self, query):
		print("# Syntactic Debug: {}".format(query))
		if query in self.cache and "syntactic" in self.cache[query]:
			return self.cache[query]["syntactic"]
		# syntactic_parse_tree = next(self.parser.parse_text(query))
		syntactic_parse_tree = next(self.parser.parse_text(urllib.parse.quote(query)))
		if not (query in self.cache):
			self.cache[query] = {}
		self.cache[query]["syntactic"] = syntactic_parse_tree
		return syntactic_parse_tree

	def dependency_parse(self, query):
		print("# Dependency Debug: {}".format(query))
		if query in self.cache and "dependency" in self.cache[query]:
			return self.cache[query]["dependency"]
		# dependency_parse_tree = next(self.dependency_parser.parse_text(query))
		dependency_parse_tree = next(self.dependency_parser.parse_text(urllib.parse.quote(query)))
		if not (query in self.cache):
			self.cache[query] = {}
		self.cache[query]["dependency"] = dependency_parse_tree
		return dependency_parse_tree