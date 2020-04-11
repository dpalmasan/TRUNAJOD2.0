# -*- coding: utf-8 -*-
"""Syllabizer module.

This syllabizator is for spanish texts. It is based on
http://sramatic.tripod.com/silabas.html

And based on mabodo's implementation: https://github.com/mabodo/sibilizador

* Strong vowels are ``a-e-o``
* Weak vowels are ``i-u``

The following rules are applied:

+----------------+------------------------------------------------------------+
| Rule           | Description                                                |
+================+============================================================+
| v              | The smallest syllabe is formed by one vowel.               |
+----------------+------------------------------------------------------------+
| V+ - V+        | Two vowels are separated if both are strong vowels.        |
+----------------+------------------------------------------------------------+
| V-V+ and V-V-  | Two vowels are not separated if one is strong and the other|
+----------------+------------------------------------------------------------+
|                | is weak nor if both are weak.                              |
| CV             | Most common syllable in Spanish is the one that has a      |
+----------------+------------------------------------------------------------+
|                | consonant and a vowel.                                     |
| C-C            | Two consonants joined are usually separated.               |
+----------------+------------------------------------------------------------+
| CC/C = l,r     | Two join consonants are maintained joint if the second is  |
|                | an l or r.                                                 |
+----------------+------------------------------------------------------------+
| CC/ = ch,ll,rr | Two consonants are joined if they represent the sounds ch, |
|                | ll,rr.                                                     |
+----------------+------------------------------------------------------------+
| C-CC           | If three consonants are joined, the first one is separated |
|                | from the rest.                                             |
+----------------+------------------------------------------------------------+
| CC-C/CsC       | In the situation of three joined consonants, the first two |
|                | are separated from the last one if the one in the middle   |
+----------------+------------------------------------------------------------+
|                | is an s.                                                   |
| CC-CC          | If four consonants are joined, they are halved.            |
+----------------+------------------------------------------------------------+
"""

STRONG_VOWELS = {'a', 'á', 'e', 'é', 'o', 'ó', 'í', 'ú'}
WEAK_VOWELS = {'i', 'u'}
RULES = [('VV', 1), ('cccc', 2), ('xcc', 1), ('ccx', 2), ('csc', 2), ('xc', 1),
         ('cc', 1), ('vcc', 2), ('Vcc', 2), ('sc', 1), ('cs', 1), ('Vc', 1),
         ('vc', 1), ('Vs', 1), ('vs', 1), ('vxv', 1), ('VxV', 1), ('vxV',
                                                                   1), ('Vxv',
                                                                        1)]


class CharLine(object):
    """Auxiliary object to set char types on a word.

    A word string is processed and converted into a char sequence,
    consisting on consonants, vowels that are used to apply rules
    for syllabizing Spanish words. This is a helper class used by
    the Syllabizator class and it is unlikely the user will need
    to explicitly instanitate an object of this class.
    """

    def __init__(self, word):
        """Charline constructor.

        :param word: Word to be processed.
        :type word: string
        """
        self.word = word
        charline = [(char, self.char_type(char)) for char in word]
        self.type_line = ''.join(chartype for _, chartype in charline)

    @staticmethod
    def char_type(char):
        """Get char type (vowel, consonant, etc).

        This method checks a ``char`` type based on syllabization rules.
        If the ``char`` is in ``STRONG_VOWELS`` this returns ``'V'``. If the
        ``char`` is in ``WEAK_VOWELS`` it will return ``'v'``. If the ``char``
        is an ``'x'`` or ``'s'`` it will return ``'x'`` and ``'s'``
        respectively. Otherwise it will return ``'c'`` representing a
        consonant.

        :param char: Char from were to get the type
        :type char: string
        :return: Char type
        :rtype: string
        """
        if char in STRONG_VOWELS:
            return 'V'
        if char in WEAK_VOWELS:
            return 'v'

        # c stands for consonant
        return char if char in {"x", "s"} else "c"

    def find(self, finder):
        """Find string occurrence in the type representation.

        :param finder: String to be searched
        :type finder: string
        :return: Position of occurrence of the finder
        :rtype: int
        """
        return self.type_line.find(finder)

    def split(self, pos, where):
        """Split the object into two Charline objects.

        :param pos: Start position of the split
        :type pos: int
        :param where: End position of the split
        :type where: int
        :return: Tuple with two charlines split
        :rtype: Tuple (CharLine, CharLine)
        """
        return (CharLine(self.word[0:pos + where]),
                CharLine(self.word[pos + where:]))

    def split_by(self, finder, where):
        """Split charline by `finder` occurrence on `type_char`.

        :param finder: Type char string
        :type finder: string
        :param where: End position to look for.
        :type where: int
        :return: Split of two charlines based on match.
        :rtype: Tuple (CharLine, CharLine)
        """
        split_point = self.find(finder)
        if split_point != -1:
            chl1, chl2 = self.split(split_point, where)
            return chl1, chl2
        return self, None

    def __str__(self):
        """Implement string representation of a CharLine object.

        :return: <word:char_types>
        :rtype: string
        """
        return '<' + self.word + ':' + self.type_line + '>'

    def __repr__(self):
        """Implement representation of a CharLine object.

        :return: <word:char_types>
        :rtype: string
        """
        return '<' + repr(self.word) + ':' + self.type_line + '>'

    def __eq__(self, other):
        """Equal operator implementation.

        :param other: CharLine to be compared to.
        :type other: CharLine
        :return: True if the ``words`` match, False otherwise
        :rtype: bool
        """
        return self.word == other.word


class Syllabizer(object):
    """Syllabizer class to process syllables from a word.

    It has methods that take a word split it into syllables using different
    rules. This class is mainly used for counting syllables.
    """

    @staticmethod
    def split(chars):
        """Split CharLine into syllabes.

        :param chars: Word to be syllabized
        :type chars: CharLine
        :return: Syllabes
        :rtype: List [CharLine]
        """
        for split_rule, where in RULES:
            first, second = chars.split_by(split_rule, where)
            if second:
                if (first.type_line in {'c', 's', 'x', 'cs'}
                        or second.type_line in {'c', 's', 'x', 'cs'}):
                    continue
                if first.type_line[-1] == 'c' and second.word[0] in {'l', 'r'}:
                    continue
                if first.word[-1] == 'l' and second.word[-1] == 'l':
                    continue
                if first.word[-1] == 'r' and second.word[-1] == 'r':
                    continue
                if first.word[-1] == 'c' and second.word[-1] == 'h':
                    continue
                return Syllabizer.split(first) + Syllabizer.split(second)
        return [chars]

    @staticmethod
    def number_of_syllables(word):
        """Return number of sillables of a word.

        :param word: Word to be processed
        :type word: string
        :return: Syllable count for the word.
        :rtype: int
        """
        charline = CharLine(word)
        return len(Syllabizer.split(charline))
