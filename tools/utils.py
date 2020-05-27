import re  # Import the regular expression library
import json

EXCLUDED_WORDS = [
    "a", "an", "the",  # Articles
    "and", "but", "or", "by", "nor", "yet", "so",  # Conjunctions
    "about", "above", "across", "after", "against", "along", "among", "around", "at", "before",  # Prepositions
    "behind", "between", "beyond", "but", "by", "concerning", "despite", "down", "during",
    "except", "following", "for", "from", "in", "including", "into", "like", "near", "of",
    "off", "on", "out", "over", "plus", "since", "through", "throughout", "to", "towards",
    "under", "until", "up", "upon", "with", "within", "without"
]

SPECIAL_WORDS = [
    "_ARG_0_", "_ARG_1_", "_ARG_2_", "_ARG_3_", "_ARG_4_", "_ARG_5_", "_ARG_6_", "_ARG_7_", "_ARG_8_", "_ARG_9_"
]


def is_mixed_case(word):
    return any(c.islower() for c in word) and any(c.isupper() for c in word)


def get_capitalized_title(initial_title: str) -> str:
    """
    Take a string and return it in a fashion that follows proper title case guidelines

    Source: http://guidohenkel.com/2018/08/title-case-creation-python-csharp/
    """

    out_string = ""
    fragments = re.split(r'(\".*?\")|(\'.*?\')|(“.*?”)|(‘.*?’)',
                         initial_title)  # Extract titles in quotation marks from string

    for fragment in fragments:  # Treat and re-assemble all fragments
        if fragment:  # skip empty matches generated by the OR in regex
            frag_string = ""
            tokens = fragment.split()  # Break string into individual words

            if tokens:

                for word in tokens:  # Check each word

                    if word not in SPECIAL_WORDS:
                        punct = word[-1]  # Check for trailing punctuation mark
                        if punct.isalpha():
                            punct = ""
                        else:
                            word = word[:-1]
                    else:
                        punct = ""

                    if word in SPECIAL_WORDS:
                        frag_string += word + punct + " "  # do nothing
                    elif word.lower() in EXCLUDED_WORDS:
                        frag_string += word.lower() + punct + " "  # make it lowercase
                    elif word.isupper() or is_mixed_case(word):
                        frag_string += word + punct + " "  # do nothing
                    elif word and word[0] == '"' and word[-1] == '"':  # Check for quoted words
                        frag_string += word + punct + " "  # do nothing
                    else:
                        frag_string += word.capitalize() + punct + " "  # capitalize it

                cap = 1
                if not frag_string[0].isalpha():
                    cap = 2

                if frag_string[0] == '"' and frag_string[-2] == '"':  # Check for quoted words
                    out_string += frag_string.strip() + " "
                else:
                    out_string += (frag_string[:cap].upper() + frag_string[cap:]).strip() + " "

    return (out_string[:1].upper() + out_string[1:]).strip()  # Capitalize first letter and strip trailing space

def results_file_to_dict(f):
    """
    Takes a file pointer to a JS/JSON results file and returns a dict

    :param f: file pointer
    :return: dict()
    """

    json_payload = f.readlines()
    json_payload.pop(0)
    json_payload = ''.join(json_payload)
    json_file = json.loads(json_payload)
    return json_file
