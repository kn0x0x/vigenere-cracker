# Vigenère Cipher CTF Solver

A powerful automated tool for solving Vigenère cipher challenges in CTF competitions. This script implements multiple cryptanalysis techniques to break Vigenère ciphers without requiring the key.

## Features

- **Kasiski Examination**: Automatically determines possible key lengths by analyzing repeated sequences
- **Frequency Analysis**: Uses statistical analysis to determine the most likely key
- **Multiple Key Testing**: Tests multiple key lengths and custom keys
- **Flag Detection**: Automatically extracts potential flags from decrypted text
- **Customizable Flag Format**: Supports any flag format through regular expressions
- **Comprehensive Output**: Detailed output with multiple decryption attempts and scoring

## Installation

```bash
# Clone the repository
git clone https://github.com/kn0x0x/vigenere-cracker.git
cd vigenere-solver

# Make the script executable
chmod +x vigenere-cracker.py
```

## Usage

```bash
./vigenere-cracker.py [ciphertext or file] [options]
```

### Basic Examples

Decrypt a ciphertext directly:
```bash
./vigenere-cracker.py "GMCAIVQOQYMDMRAWSRLTDXGFHHAKXEWKARAXKNPMSLZANWXLXIJWAXKIPRSRKHKNPATERXVVHRKNHLXYKN"
```

Decrypt from a file:
```bash
./vigenere-cracker.py ciphertext.txt
```

### Advanced Options

Specify a known key:
```bash
./vigenere-cracker.py ciphertext.txt -k "VIGENERE"
```

Try specific keys:
```bash
./vigenere-cracker.py ciphertext.txt -t "BELLASO,VIGENERE,KASISKI"
```

Specify key length:
```bash
./vigenere-cracker.py ciphertext.txt -l 6
```

Custom flag format:
```bash
./vigenere-cracker.py ciphertext.txt -f "flag{.*?}"
```

Save results to a file:
```bash
./vigenere-cracker.py ciphertext.txt -o results.txt
```

## Options

- `-k, --key KEY`: Use a specific key for decryption
- `-f, --flag-format FORMAT`: Set custom flag format (regex pattern, default: texsaw{.*?})
- `-t, --try-keys KEYS`: Try comma-separated list of keys
- `-l, --key-length LENGTH`: Specify the key length if known
- `-o, --output FILE`: Save results to a file

## How It Works

1. **Key Length Analysis**:
   - Identifies repeating sequences in the ciphertext
   - Calculates distances between repetitions
   - Finds common factors among these distances
   - Ranks potential key lengths by frequency

2. **Key Recovery**:
   - For each possible key length, splits ciphertext into columns
   - Performs frequency analysis on each column to determine most likely shift
   - Combines shifts to form the complete key

3. **Flag Extraction**:
   - Searches decrypted text for flag format matches
   - Looks for common flag markers (e.g., "THE FLAG IS")
   - Extracts surrounding context for potential flags

## Background

The Vigenère cipher was invented by Giovan Battista Bellaso in the 16th century but is named after Blaise de Vigenère. It remained unbroken until Friedrich Kasiski published a general method of decipherment in 1863.

The cipher uses a series of different Caesar ciphers based on the letters of a keyword, making it significantly harder to break than simple substitution ciphers.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
