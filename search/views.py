
from django.shortcuts import render
from django.http import HttpResponse


def search_page(request):
	return render(request, 'search/jsp.html', {'results': None})


def search_results(request):
	import os
	import requests
	query = request.GET.get('q', '')
	results = []
	youtube_results = []
	if query:
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

		# YouTube Data API integration
		try:
			api_key = "AIzaSyCeL3KjoBgHJvplyX62GYRD6tIhcsG9mtc"
			yt_url = "https://www.googleapis.com/youtube/v3/search"
			params = {
				'part': 'snippet',
				'q': query,
				'type': 'video',
				'maxResults': 3,
				'key': api_key
			}
			yt_resp = requests.get(yt_url, params=params, timeout=5)
			if yt_resp.status_code == 200:
				yt_data = yt_resp.json()
				for item in yt_data.get('items', []):
					video_id = item['id']['videoId']
					title = item['snippet']['title']
					url = f"https://www.youtube.com/watch?v={video_id}"
					youtube_results.append({'title': title, 'url': url})
			else:
				youtube_results.append({'title': 'YouTube API error', 'url': ''})
		except Exception as e:
			youtube_results.append({'title': f'YouTube API error: {e}', 'url': ''})

	return render(request, 'search/jsp.html', {'query': query, 'results': results, 'youtube_results': youtube_results})
