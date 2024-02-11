

def numer_formatter(number):

    format_souls_eggs = '{:_.0f}'.format(number)
    print(format_souls_eggs)

    suffixes = {

        1_000: 'K (Thousand)',               # Thousand
        1_000_000: 'M (Million)',           # Million
        1_000_000_000: 'B (Billion)',       # Billion
        1_000_000_000_000: 'T (Trillion)',   # Trillion
        1_000_000_000_000_000: 'q (Quadrillion)',   # Quadrillion
        1_000_000_000_000_000_000: 'Q (Quintillion)',   # Quintillion
        1_000_000_000_000_000_000_000: 's (Sextillion)',   # Sextillion
        1_000_000_000_000_000_000_000_000: 'S (Septillion)',   # Septillion
        1_000_000_000_000_000_000_000_000_000: 'O (Octillion)',   # Octillion
        1_000_000_000_000_000_000_000_000_000_000: 'N (Nonillion)',   # Nonillion
        1_000_000_000_000_000_000_000_000_000_000_000: 'D (Decillion)'   # Decillion

    }

    for divisor, suffix in sorted(suffixes.items(), reverse=True):
        if number >= divisor:
            return f"{number / divisor:,.3f}{suffix}"
    
    return str(number)