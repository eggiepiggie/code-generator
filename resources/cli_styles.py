"""
	To help prettify the help command prompt.
	Colour References: https://misc.flogisoft.com/bash/tip_colors_and_formatting
"""
DEFAULT = "\033[0;39;40m"

# Default colour set to terminal.
RED = "\033[0;31;40m"
GREEN = "\033[0;32;40m"
YELLOW = "\033[0;33;40m"
BLUE = "\033[0;34;40m"
MAGENTA = "\033[0;35;40m"
CYAN = "\033[0;36;40m"
LIGHT_GRAY = "\033[0;37;40m"
DARK_GRAY = "\033[0;90;40m"
LIGHT_RED = "\033[0;91;40m"
LIGHT_GREEN = "\033[0;92;40m"
LIGHT_YELLOW = "\033[0;93;40m"
LIGHT_BLUE = "\033[0;94;40m"
LIGHT_MAGENTA = "\033[0;95;40m"
LIGHT_CYAN = "\033[0;96;40m"
WHITE = "\033[0;97;40m"

"""
  256 Default Base Colour Definition

  To print text with a specific colour, replace DDD with the appropriate number 
  that corresponds to your desired colour.
"""
BASE_256 = "\033[38;5;DDDm"

# Eggie defined colour set.
ORANGE = "\033[38;5;202m"
LIGHT_PINK = "\033[38;5;204m"
LIGHT_ORANGE = "\033[38;5;214m"
DARK_RED = "\033[38;5;88m"

# Pastel Colour Set.
PASTEL_PINK = "\033[38;5;218m"
PASTEL_PURPLE = "\033[38;5;177m"
PASTEL_BLUE = "\033[38;5;80m"
PASTEL_GREEN = "\033[38;5;120m"