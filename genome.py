def suffix_array1(s):
    """
    Construct the suffix array of a given string using prefix doubling.

    Args:
    s (str): The input string.

    Returns:
    list of int: The suffix array.
    """
    n = len(s)
    suffixes = [(s[i:], i) for i in range(n)]
    suffixes.sort()
    
    # Map the sorted suffixes to their original indices
    suffix_array = [suffix[1] for suffix in suffixes]
    
    k = 1
    while k < n:
        # Generate the new order of suffixes based on 2k-prefixes
        new_order = [0] * n
        new_order[suffix_array[0]] = 0
        for i in range(1, n):
            # Compare two suffixes based on their (2k)-prefixes
            if suffixes[i - 1][0][:k] == suffixes[i][0][:k]:
                new_order[suffix_array[i]] = new_order[suffix_array[i - 1]]
            else:
                new_order[suffix_array[i]] = new_order[suffix_array[i - 1]] + 1
        
        # Update the suffix array with the new order
        for i in range(n):
            suffixes[i] = (suffixes[i][0], suffix_array[i], new_order[suffix_array[i]])
        suffixes.sort()
        suffix_array = [suffix[1] for suffix in suffixes]
        
        k *= 2
    
    return suffix_array

