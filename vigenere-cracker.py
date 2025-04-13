#!/usr/bin/env python3
"""
Vigenère Cipher CTF Solver
--------------------------
Automated Vigenère cipher decoder for CTF challenges
Features:
- Frequency analysis to find key length using Kasiski method
- Automatic key analysis based on letter frequency
- Test with special keys (customizable)
- Find flags in decrypted text with customizable format
"""

import re
import argparse
from collections import Counter
import math
import itertools

def vigenere_decrypt(ciphertext, key):
    """Decrypt Vigenère with a known key"""
    plaintext = ''
    key_length = len(key)
    
    for i, char in enumerate(ciphertext):
        if not char.isalpha():
            plaintext += char
            continue
            
        # Handle uppercase and lowercase
        if char.isupper():
            shift = ord('A')
        else:
            shift = ord('a')
            
        # Get corresponding key character
        key_char = key[i % key_length]
        if key_char.isupper():
            key_shift = ord('A')
        else:
            key_shift = ord('a')
            
        # Apply Vigenère decryption formula
        p = (ord(char) - shift - (ord(key_char) - key_shift)) % 26 + shift
        plaintext += chr(p)
        
    return plaintext

def find_key_length(ciphertext, max_length=20):
    """Find possible key length using Kasiski method"""
    # Find repeating sequences
    counts = {}
    for length in range(3, 12):  # Look for sequences of length 3-11 characters
        for i in range(len(ciphertext) - length):
            seq = ciphertext[i:i+length]
            if ciphertext.count(seq) > 1:
                distances = []
                pos = -1
                while True:
                    pos = ciphertext.find(seq, pos + 1)
                    if pos == -1:
                        break
                    distances.append(pos)
                
                for i in range(1, len(distances)):
                    dist = distances[i] - distances[i-1]
                    if dist in counts:
                        counts[dist] += 1
                    else:
                        counts[dist] = 1
    
    # Find most common factors
    factors = {}
    for dist, count in counts.items():
        for i in range(2, min(dist, max_length + 1)):
            if dist % i == 0:
                if i in factors:
                    factors[i] += count
                else:
                    factors[i] = count
    
    # Sort factors by frequency
    sorted_factors = sorted(factors.items(), key=lambda x: x[1], reverse=True)
    
    return [length for length, _ in sorted_factors[:5]]

def calculate_ioc(text):
    """Calculate Index of Coincidence"""
    n = len(text)
    if n <= 1:
        return 0
    
    freq = Counter(text)
    sum_freqs = sum(f * (f-1) for f in freq.values())
    return sum_freqs / (n * (n-1))

def score_text(text):
    """Score text based on English letter frequency"""
    # English letter frequency
    eng_freq = {
        'E': 12.02, 'T': 9.10, 'A': 8.12, 'O': 7.68, 'I': 7.31, 'N': 6.95, 'S': 6.28, 'R': 6.02, 'H': 5.92, 'D': 4.32,
        'L': 3.98, 'U': 2.88, 'C': 2.71, 'M': 2.61, 'F': 2.30, 'Y': 2.11, 'W': 2.09, 'G': 2.03, 'P': 1.82, 'B': 1.49,
        'V': 1.11, 'K': 0.69, 'X': 0.17, 'Q': 0.11, 'J': 0.10, 'Z': 0.07
    }
    
    # Count letter occurrences
    letter_count = Counter(c.upper() for c in text if c.isalpha())
    total_letters = sum(letter_count.values())
    
    if total_letters == 0:
        return float('inf')
    
    # Normalize frequencies
    text_freq = {letter: (count / total_letters) * 100 for letter, count in letter_count.items()}
    
    # Calculate deviation score (lower is better)
    score = 0
    for letter, freq in eng_freq.items():
        score += abs(freq - text_freq.get(letter, 0))
    
    # Check for common English words
    common_words = ['THE', 'AND', 'THAT', 'HAVE', 'FOR', 'NOT', 'WITH', 'YOU', 'THIS', 'BUT']
    word_count = 0
    for word in common_words:
        word_count += text.upper().count(word)
    
    # Combine frequency score and word count
    return score - (word_count * 5)  # Lower score is better

def find_key(ciphertext, key_length):
    """Find key based on key length"""
    key = ''
    
    for i in range(key_length):
        # Extract characters at the same key position
        chars = ciphertext[i::key_length]
        
        # Try each possible shift and score
        best_score = float('inf')
        best_shift = None
        
        for shift in range(26):
            # Decrypt segment with this shift
            decrypted = ''.join([chr((ord(c.upper()) - ord('A') - shift) % 26 + ord('A')) for c in chars if c.isalpha()])
            
            # Score the result
            score = score_text(decrypted)
            
            if score < best_score:
                best_score = score
                best_shift = shift
        
        # Add best shift to key
        key += chr(best_shift + ord('A'))
    
    return key

def find_flags(text, pattern='texsaw{.*?}', case_insensitive=True):
    """Find flags in text"""
    if case_insensitive:
        flags = re.findall(pattern, text, re.IGNORECASE)
    else:
        flags = re.findall(pattern, text)
    return flags

def extract_potential_flags(plaintext, flag_format='texsaw{.*?}'):
    """Extract potential flags from decrypted text"""
    # Find by flag format
    flags = find_flags(plaintext, flag_format)
    
    # Find phrases that might contain flags
    flag_markers = ['THE FLAG IS', 'FLAG IS', 'FLAG:', 'THE FLAG:', 'FLAG =', 'FLAG = ']
    potential_flags = []
    
    for marker in flag_markers:
        idx = plaintext.upper().find(marker)
        if idx != -1:
            # Get 100 characters after marker
            context = plaintext[idx:idx+len(marker)+100]
            potential_flags.append(context)
    
    return flags, potential_flags

def create_flag(content, format_str='texsaw{{{0}}}'):
    """Create flag from content"""
    return format_str.format(content)

def main():
    parser = argparse.ArgumentParser(description='Vigenère Cipher CTF Solver')
    parser.add_argument('ciphertext', help='Ciphertext to decrypt or path to file containing ciphertext')
    parser.add_argument('-k', '--key', help='Known key (if available)')
    parser.add_argument('-f', '--flag-format', default='texsaw{.*?}', help='Flag format (regex, default: texsaw{.*?})')
    parser.add_argument('-t', '--try-keys', help='Try specific keys (comma-separated)')
    parser.add_argument('-l', '--key-length', type=int, help='Fixed key length (if known)')
    parser.add_argument('-o', '--output', help='Output file to save results')
    args = parser.parse_args()
    
    try:
        # Read ciphertext
        if args.ciphertext.endswith('.txt') or '/' in args.ciphertext:
            with open(args.ciphertext, 'r') as f:
                ciphertext = f.read().strip()
        else:
            ciphertext = args.ciphertext
    except:
        ciphertext = args.ciphertext
    
    print(f'[*] Read ciphertext ({len(ciphertext)} characters)')
    
    results = []
    
    # If key is known, use it directly
    if args.key:
        key = args.key.upper()
        print(f'[*] Using known key: {key}')
        plaintext = vigenere_decrypt(ciphertext, key)
        flags, potential_flags = extract_potential_flags(plaintext, args.flag_format)
        
        output = f'[+] Decrypted with key {key}:\n'
        output += f'{plaintext[:200]}...\n\n'
        
        if flags:
            output += '[+] Found flags:\n'
            for flag in flags:
                output += f'    {flag}\n'
        
        if potential_flags:
            output += '[+] Potential flags:\n'
            for flag in potential_flags:
                output += f'    {flag}\n'
        
        results.append(output)
    else:
        # Find possible key lengths
        if args.key_length:
            possible_lengths = [args.key_length]
            print(f'[*] Using known key length: {args.key_length}')
        else:
            possible_lengths = find_key_length(ciphertext)
            print(f'[*] Possible key lengths: {possible_lengths}')
        
        # Try each key length
        for length in possible_lengths:
            key = find_key(ciphertext, length)
            print(f'[*] Trying key with length {length}: {key}')
            plaintext = vigenere_decrypt(ciphertext, key)
            flags, potential_flags = extract_potential_flags(plaintext, args.flag_format)
            
            output = f'[+] Decrypted with key {key}:\n'
            output += f'{plaintext[:200]}...\n\n'
            
            if flags:
                output += '[+] Found flags:\n'
                for flag in flags:
                    output += f'    {flag}\n'
            
            if potential_flags:
                output += '[+] Potential flags:\n'
                for flag in potential_flags:
                    output += f'    {flag}\n'
            
            results.append(output)
    
    # Try suggested keys
    if args.try_keys:
        suggested_keys = [k.strip().upper() for k in args.try_keys.split(',')]
        print(f'[*] Trying suggested keys: {suggested_keys}')
        
        for key in suggested_keys:
            plaintext = vigenere_decrypt(ciphertext, key)
            flags, potential_flags = extract_potential_flags(plaintext, args.flag_format)
            
            output = f'[+] Decrypted with key {key}:\n'
            output += f'{plaintext[:200]}...\n\n'
            
            if flags:
                output += '[+] Found flags:\n'
                for flag in flags:
                    output += f'    {flag}\n'
            
            if potential_flags:
                output += '[+] Potential flags:\n'
                for flag in potential_flags:
                    output += f'    {flag}\n'
            
            results.append(output)
    
    # Print results
    for result in results:
        print('\n' + '='*50 + '\n')
        print(result)
    
    # Save results if needed
    if args.output:
        with open(args.output, 'w') as f:
            for result in results:
                f.write(result + '\n' + '='*50 + '\n')
        print(f'[*] Saved results to {args.output}')

if __name__ == '__main__':
    main()
