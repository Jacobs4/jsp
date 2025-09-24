
from django.shortcuts import render
from django.http import HttpResponse


def search_page(request):
	return render(request, 'search/jsp.html', {'results': None})


def search_results(request):
	import os
	query = request.GET.get('q', '')
	results = []
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
	return render(request, 'search/jsp.html', {'query': query, 'results': results})
