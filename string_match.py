def match(first, second):
    # If we reach at the end of both strings, we are done
    if len(first) == 0 and len(second) == 0:
        return True

    # Make sure that the characters after '*' are present
    # in second string. This function assumes that the first
    # string will not contain two consecutive '*'
    if len(first) > 1 and first[0] == '*' and  len(second) == 0:
        return False

    # If the first string contains '?', or current characters
    # of both strings match
    if (len(first) > 1 and first[0] == '?') or (len(first) != 0
        and len(second) !=0 and first[0] == second[0]):
        return match(first[1:],second[1:]);

    # If there is *, then there are two possibilities
    # a) We consider current character of second string
    # b) We ignore current character of second string.
    if len(first) !=0 and first[0] == '*':
        return match(first[1:],second) or match(first,second[1:])

    return False
