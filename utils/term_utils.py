from utils.io_utils import load_json
import resources.cli_styles as cs


def printt(text = "", colour = cs.DEFAULT):
	print("{}{}".format(colour, convert_tabs_to_spaces(text)))

def printt_red(text):
	printt(text, cs.RED)

def printt_light_cyan(text):
	printt(text, cs.LIGHT_CYAN)

# ===============================================
#  Methods for severity log printout to terminal
# ===============================================
def printt_critical(text):
	printt("CRITICAL: " + text, cs.DARK_RED)

def printt_error(text):
	printt("ERROR: " + text, cs.RED)

def printt_warning(text):
	printt("WARNING: " + text, cs.ORANGE)

def convert_tabs_to_spaces(text):
	text = text.replace("\t", "    ")
	return text

def apply_syntax_colorization(text, language = None):
	if not language:
		return

	db_schema = load_json("resources/language-syntax/python-syntax.json")

	keywords = db_schema["keywords"]
	ops = db_schema["operators"]
	braces = db_schema["braces"]

	for op in ops:
		text = text.replace(op, "{}{}{}".format(cs.PASTEL_PURPLE, op, cs.DEFAULT))

	for key in keywords:
		text = text.replace(key, "{}{}{}".format(cs.PASTEL_PINK, key, cs.DEFAULT))

	return text