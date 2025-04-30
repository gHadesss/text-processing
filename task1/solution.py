import re

PASSWORD_REGEXP = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\^\$\%@\#&\*\!\?].*[\^\$\%@\#&\*\!\?])(?![A-Za-z\d]*([\^\$\%@\#&\*\!\?])(\1|[A-Za-z\d])*$)(?!.*([a-zA-Z\d\^\$\%@\#&\*\!\?])\3.*$)([a-zA-Z\d\^\$\%@\#&\*\!\?]){8,}$'
COLOR_REGEXP = r'^(#(([0-9a-fA-F]{3}){1,2})|rgb\((((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]),\s?){2}(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])|((\d|[1-9]\d|100)%,\s?){2}(\d|[1-9]\d|100)%)\)|hsl\((\d|[1-9]\d|[12]\d\d|3[0-5]\d|360)(,\s?(\d|[1-9]\d|100)%){2}\))$'
EXPRESSION_REGEXP = r'(?:(?P<constant>\b(?:pi|e|sqrt2|ln2|ln10\b))|(?P<function>\b(?:sinh|cosh|tanh|coth|th|cth|sin|cos|ctg|tg|tan|cot|ln|lg|log|exp|sqrt|cbrt|abs|sign)\b)|(?P<operator>[\^\*\/\-\+])|(?P<left_parenthesis>\()|(?P<right_parenthesis>\))|(?P<variable>\b[a-zA-Z_]+[0-9a-zA-Z_]*\b)|(?P<number>\b\d+(?:\.\d+)?\b)|\s)+'
DATES_REGEXP = r'^(?:(?:0?[1-9]|[12]\d|3[01])([\.\/\-])(?:0?[13578]|1[02])\1\d{1,4}|(?:0?[1-9]|[12]\d|30)([\.\/\-])(?:0?[469]|11)\2\d{1,4}|(?:0?[1-9]|1\d|2[0-8])([\.\/\-])(?:0?2)\3\d{1,4}|\d{1,4}([\.\/\-])(?:0?[13578]|1[02])\4(?:0?[1-9]|[12]\d|3[01])|\d{1,4}([\.\/\-])(?:0?[469]|11)\5(?:0?[1-9]|[12]\d|30)|\d{1,4}([\.\/\-])(?:0?2)\6(?:0?[1-9]|1\d|2[0-8])|(?:0?[1-9]|[12]\d|3[01])\s(?:января|марта|мая|июля|августа|октября|декабря)\s\d{1,4}|(?:0?[1-9]|[12]\d|30)\s(?:апреля|июня|сентября|ноября)\s\d{1,4}|(?:0?[1-9]|1\d|2[0-8])\sфевраля\s\d{1,4}|(?:January|Jan|March|Mar|May|July|Jul|August|Aug|Oct|Dec)\s(?:0?[1-9]|[12]\d|3[01])\,\s\d{1,4}|(?:April|Apr|June|Jun|September|Sep|November|Nov)\s(?:0?[1-9]|[12]\d|30)\,\s\d{1,4}|(?:February|Feb)\s(?:0?[1-9]|1\d|2[0-8])\,\s\d{1,4}|\d{1,4}\,\s(?:January|Jan|March|Mar|May|July|Jul|August|Aug|Oct|Dec)\s(?:0?[1-9]|[12]\d|3[01])|\d{1,4}\,\s(?:April|Apr|June|Jun|September|Sep|November|Nov)\s(?:0?[1-9]|[12]\d|30)|\d{1,4}\,\s(?:February|Feb)\s(?:0?[1-9]|1\d|2[0-8]))$'

PARENTHESIS_EXAMPLE = r'(?:\(X\)|\[X\]|\{X\})*'

def parenthesis_tree(template: str, n: int) -> str:
    if n == 0:
        return template.replace('X', '')
    return parenthesis_tree(template.replace('X', PARENTHESIS_EXAMPLE), n - 1)

PARENTHESIS_REGEXP = parenthesis_tree(PARENTHESIS_EXAMPLE, 10)
SENTENCES_REGEXP = r'(?P<sentence>(\d{1,2}(?:[,.]\d)?\s+из\s+10\s*)|((?:[A-ЯA-ZЁ\"]|\d+)[^\?\.\!]*\:\s*\n*(\n*\s*\d+\.[^\.\n]*\;\s*)+(\n*\s*\d+\.[^\.\n]*[\?\.\!]))|((?:[A-ЯA-ZЁ\"]|\d+)[^\?\.\!\:]*\:\s*\n)|((?:[A-ЯA-ZЁ\"]|\d+)[^\?\.\!]*(?:\.{1,4}|\?+|\!+)?(?=\n+(?:[A-ЯA-ZЁ\"]|\d+)))|((?:\d+\.\s*)?(?:[A-ЯA-ZЁ\"]|\d+)[^\?\.\!]*(?:\.{1,4}|\?+|\!+)\"?))'
PERSONS_REGEXP = r'(?<![\.\?\!]\s)(?<!\")(?P<person>[А-ЯЁA-Z][a-zа-яё]+(?:\-[А-ЯЁA-Z]?[a-zа-яё]+)?(?:\s([А-ЯЁA-Z]\.\s?[А-ЯЁA-Z]?)|\s([А-ЯЁA-Z][a-zа-яё]+(?:\-[А-ЯЁA-Z]?[a-zа-яё]+)?))?)'
SERIES_REGEXP = r'(<td><h1\s*class="level2"><a\s*class="all"\s*href="\/series\/\d+\/">\s*(?P<name>.+)\s*<\/a>)|(<td\s*class="news"\s*colspan="2".*><h1.*>\s*Сезон\s*(?P<season>\d+)\s*<\/h1>\s*((?P<season_year>\d{4}),)?\s*эпизодов:\s*(?P<season_episodes>\d+)\s*<\/td>)|(<td\sclass="news"><b>Эпизоды:<\/b><\/td>\s*\n*\s*<td>\s*\n*\s*<table.*>\s*\n*\s*<tr>\s*\n*\s*<td\s*class="news">\s*(?P<episodes_count>\d+)\s*<\/td>)|(<span.*>Эпизод\s*(?P<episode_number>\d+)\s*<\/span><br\/>\s*\n*\s*<h1.*><b>\s*(?P<episode_name>.+)\s*<\/b><\/h1>\s*\n*\s*(<span.*>\s*(?P<episode_original_name>.*)\s*<\/span>\s*)?<\/td>\s*\n*\s*(<td.*>\s*(?P<episode_date>\d\d?\s*[а-я]*\s*\d{4})\s*<\/td>)?)'

re.compile(PASSWORD_REGEXP)
re.compile(COLOR_REGEXP)
re.compile(EXPRESSION_REGEXP)
re.compile(DATES_REGEXP)
re.compile(PARENTHESIS_REGEXP)
re.compile(SENTENCES_REGEXP)
re.compile(PERSONS_REGEXP)
re.compile(SERIES_REGEXP)
