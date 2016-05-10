# -*- coding: utf-8 -*-

import re


class Segment:
    """
    Store a representation of text segment.
    """
    def __init__(self, text, in_tag):
        self.text = text
        self.inTag = in_tag

    def __str__(self):
        return '"Segment{text="' + self.text + '"'+', inTag=' + str(self.inTag).lower()+'}";'


def separate_printer(text):
    """Print output of the separate() function.

        Args:
            text: input text.

        Examples:
        >>> separate_printer("<ABC>Ala</ABC> ma <ABC> kota<ABC> a</ABC> kot </ABC> ma Ale")
        {"Segment{text="<ABC>Ala</ABC>", inTag=true}";
        "Segment{text=" ma ", inTag=false}";
        "Segment{text="<ABC> kota<ABC> a</ABC> kot </ABC>", inTag=true}";
        "Segment{text=" ma Ale", inTag=false}";
        }

        >>> separate_printer("<ABC>Ala")
        {"Segment{text="<ABC>Ala", inTag=false}";
        }

        >>> separate_printer("<ABC>Ala</ABC>")
        {"Segment{text="<ABC>Ala</ABC>", inTag=true}";
        }

        >>> separate_printer("</ABC>Ala")
        {"Segment{text="</ABC>Ala", inTag=false}";
        }

        >>> separate_printer("Ala <ABC> kota<ABC> a</ABC> kot")
        {"Segment{text="Ala ", inTag=false}";
        "Segment{text="<ABC> kota<ABC> a</ABC>", inTag=true}";
        "Segment{text=" kot", inTag=false}";
        }

        >>> separate_printer("</ABC>Ala<ABC>")
        {"Segment{text="</ABC>Ala<ABC>", inTag=false}";
        }

        >>> separate_printer("a </ABC>Ala<ABC> b")
        {"Segment{text="a </ABC>Ala<ABC> b", inTag=false}";
        }

        >>> separate_printer("")
        {}

    """

    print("{", end='')
    for segment in separate(text):
        print(segment)
    print("}")


def separate(text):
    """Split text based on "<ABC>" and "</ABC>" tags.

        Args:
            text: input text.

        Returns:
            List of Segment objects.

    """
    open_tag = "<ABC>"
    close_tag = "</ABC>"
    pattern_begin = "("+open_tag+")"
    pattern_end = "("+close_tag+")"
    pattern_begin_or_end = "("+pattern_begin+"|"+pattern_end+")"

    output_list = []
    level = 0
    position = 0
    mo = None

    for mo in re.finditer(pattern_begin_or_end, text):
        if mo.group(0) == open_tag:
            level += 1
            if level == 1:
                if position != mo.start() and text.find(close_tag, mo.end()) != -1:
                    output_list.append(Segment(text[position:mo.start()], False))
                    position = mo.start()
        elif mo.group(0) == close_tag:
            if level == 1:
                output_list.append(Segment(text[position:mo.end()], True))
                position = mo.end()
            if level > 0:
                level -= 1

    if mo and mo.group(0) == close_tag and level != 0:
        output_list.append(Segment(text[position:mo.end()], True))
        position = mo.end()

    if position != len(text):
        output_list.append(Segment(text[position:], False))

    return output_list


if __name__ == "__main__":
    import doctest
    doctest.testmod()
