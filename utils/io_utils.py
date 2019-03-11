import json

def load_json(file_url):
	"""Loads file as JSON, closing the file resource after completion."""
	try:
		with open(file_url) as f:
			json_content = json.load(f)
	except FileNotFoundError as fnf_error:
		print("Error: Could not load JSON.", fnf_error)

	return json_content