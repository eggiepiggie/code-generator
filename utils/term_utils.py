import resources.cli_styles as cs

def printt(text = "", colour = cs.DEFAULT):
	print("{}{}".format(colour, text))

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