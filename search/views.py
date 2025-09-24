
from django.shortcuts import render
from django.http import HttpResponse


def search_page(request):
	return render(request, 'search/jsp.html', {'results': None})


def search_results(request):
	import os
	import requests
	query = request.GET.get('q', '')
	results = []
	meilisearch_results = []
	wikipedia_results = []
	duckduckgo_results = []
	opensearch_results = []
	if query:
		# OpenSearch API integration (example: demo cluster, adjust as needed)
		try:
			from opensearchpy import OpenSearch
			# Example: connect to local OpenSearch (adjust host/port as needed)
			client = OpenSearch(
				hosts=[{'host': 'localhost', 'port': 9200}],
				http_compress=True
			)
			# Example: search all indices for the query in 'content' field
			response = client.search(
				body={
					'query': {
						'multi_match': {
							'query': query,
							'fields': ['*']
						}
					}
				},
				size=5
			)
			for hit in response['hits']['hits']:
				opensearch_results.append({
					'index': hit.get('_index', ''),
					'score': hit.get('_score', 0),
					'source': hit.get('_source', {})
				})
		except Exception as e:
			opensearch_results.append({'index': '', 'score': 0, 'source': {'error': f'OpenSearch error: {e}'}})
		# Wikipedia-API Python package integration
		try:
			import wikipediaapi
			wiki_wiki = wikipediaapi.Wikipedia(
				language='en',
				user_agent='jsp-search-engine/1.0 (https://github.com/Jacobs4/jsp)'
			)
			page_py = wiki_wiki.page(query)
			if page_py.exists():
				wikipedia_results.append({
					'title': page_py.title + ' (wikipedia-api)',
					'summary': page_py.summary[0:500] + ('...' if len(page_py.summary) > 500 else ''),
					'url': page_py.fullurl
				})
			else:
				wikipedia_results.append({'title': f'No Wikipedia page found for "{query}" (wikipedia-api).', 'summary': '', 'url': ''})
		except Exception as e:
			wikipedia_results.append({'title': f'wikipedia-api error: {e}', 'summary': '', 'url': ''})
		root_dir = '/workspaces/jsp'
		file_types = ['.md', '.py']
		for subdir, _, files in os.walk(root_dir):
			# Skip virtual environment and hidden folders
			if 'venv' in subdir or '/.' in subdir:
				continue
			for file in files:
				if any(file.endswith(ext) for ext in file_types):
					file_path = os.path.join(subdir, file)
					try:
						with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
							for i, line in enumerate(f, 1):
								if query.lower() in line.lower():
									results.append(f"{file} (line {i}): {line.strip()}")
					except Exception as e:
						results.append(f"Error reading {file}: {e}")

		# Wikipedia API integration
		try:
			wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
			wiki_resp = requests.get(wiki_url, timeout=5)
			if wiki_resp.status_code == 200:
				wiki_data = wiki_resp.json()
				if 'extract' in wiki_data:
					wikipedia_results.append({
						'title': wiki_data.get('title', query),
						'summary': wiki_data['extract'],
						'url': wiki_data.get('content_urls', {}).get('desktop', {}).get('page', '')
					})
				else:
					wikipedia_results.append({'title': 'No Wikipedia summary found.', 'summary': '', 'url': ''})
			else:
				wikipedia_results.append({'title': 'Wikipedia API error', 'summary': '', 'url': ''})
		except Exception as e:
			wikipedia_results.append({'title': f'Wikipedia API error: {e}', 'summary': '', 'url': ''})

		# DuckDuckGo Instant Answer API integration
		try:
			ddg_url = "https://api.duckduckgo.com/"
			params = {'q': query, 'format': 'json', 'no_html': 1, 'skip_disambig': 1}
			ddg_resp = requests.get(ddg_url, params=params, timeout=5)
			if ddg_resp.status_code == 200:
				ddg_data = ddg_resp.json()
				if ddg_data.get('AbstractText'):
					duckduckgo_results.append({
						'heading': ddg_data.get('Heading', query),
						'abstract': ddg_data['AbstractText'],
						'url': ddg_data.get('AbstractURL', '')
					})
				else:
					duckduckgo_results.append({'heading': 'No DuckDuckGo instant answer found.', 'abstract': '', 'url': ''})
			else:
				duckduckgo_results.append({'heading': 'DuckDuckGo API error', 'abstract': '', 'url': ''})
		except Exception as e:
			duckduckgo_results.append({'heading': f'DuckDuckGo API error: {e}', 'abstract': '', 'url': ''})
		# Meilisearch API integration
		try:
			import meilisearch
			client = meilisearch.Client('http://127.0.0.1:7700', '0a6e572506c52ab0bd6195921575d23092b7f0c284ab4ac86d12346c33057f99')
			# Example: search in 'documents' index, adjust as needed
			search_result = client.index('documents').search(query, {'limit': 5})
			for hit in search_result.get('hits', []):
				meilisearch_results.append(hit)
		except Exception as e:
			meilisearch_results.append({'error': f'Meilisearch error: {e}'})

	return render(request, 'search/jsp.html', {
		'query': query,
		'results': results,
		'meilisearch_results': meilisearch_results,
		'wikipedia_results': wikipedia_results,
		'duckduckgo_results': duckduckgo_results,
		'opensearch_results': opensearch_results,
	})
