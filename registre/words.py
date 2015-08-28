import itertools

UNIQUE_CHAR = "$"

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) 
        for r in range(len(s)+1)[::-1])

def common_substring_table(s1, s2):
    table = [[0] * (1 + len(s2)) for i in xrange(1 + len(s1))]
    for row in xrange(1, 1 + len(s1)):
        for col in xrange(1, 1 + len(s2)):
            if s1[row - 1] == s2[col - 1]:
                table[row][col] = table[row - 1][col - 1] + 1
            else:
                table[row][col] = 0
    return table

def lookup_substrings(s1, s2, table, minlength):
    substrings = []
    for row in xrange(1, 1 + len(s1)):
        for col in xrange(1, 1 + len(s2)):
            if table[row][col] >= minlength:
                length = table[row][col]
                s = s1[row - length : row]
                substrings.append(s)
    return substrings

def longest_common_substring(s1, s2):
    lcstab = common_substring_table(s1, s2)
    maxlen = max([max(lcstab[r]) for r in range(len(lcstab))])
    return lookup_substrings(s1, s2, lcstab, maxlen)

def all_common_substrings(words, minlen):
    n = len(words)
    all_substrings = set()
    for i in range(n):
        for j in range(i+1, n):
            word1 = words[i]
            word2 = words[j]
            lcstab = common_substring_table(word1, word2)
            substrings = lookup_substrings(word1, word2, lcstab, minlen)
            for s in substrings:
                all_substrings.add(tuple(s)) 
    common_substrings = set()
    for substring in all_substrings:
        in_all_words = True
        for word in words:
            word_str = UNIQUE_CHAR.join(word)
            substring_str = UNIQUE_CHAR.join(substring)
            if not substring_str in word_str:
                in_all_words = False
        if in_all_words:
            common_substrings.add(substring)
    return common_substrings
