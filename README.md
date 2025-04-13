# Vigenère Cipher Cracker

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.6%2B-green)
![License](https://img.shields.io/badge/license-MIT-orange)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

An advanced cryptanalysis tool for breaking Vigenère ciphers commonly found in CTF challenges. Implements multiple attack methods including Kasiski examination and frequency analysis to automatically recover encryption keys and extract hidden flags.


## 🔍 Overview

The Vigenère cipher, a polyalphabetic substitution technique invented in the 16th century, was considered unbreakable for nearly 300 years until Friedrich Kasiski published his attack method in 1863. This tool implements modern adaptations of those techniques to rapidly solve Vigenère cipher challenges in CTFs.

## ✨ Features

- **Automated Key Length Detection**: Uses Kasiski examination and Index of Coincidence (IoC) to determine the most likely key length
- **Smart Key Recovery**: Employs frequency analysis on each column to derive the most probable key
- **Multiple Attack Strategies**: Combines several approaches to maximize success rate
- **Smart Flag Detection**: Automatically extracts potential flags based on customizable formats and context clues
- **Comprehensive Output**: Detailed analysis of decryption attempts with scoring metrics
- **Historical Key Testing**: Includes built-in testing for historically significant keys

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/kn0x0x/vigenere-cracker.git
cd vigenere-cracker

# Install requirements (if any)
pip install -r requirements.txt

# Make the script executable
chmod +x vigenere-cracker.py
```

## 📋 Usage

```bash
./vigenere-cracker.py [ciphertext or file] [options]
```

### Basic Examples

**Decrypt a ciphertext directly:**
```bash
./vigenere-cracker.py "GMCAIVQOQYMDMRAWSRLTDXGFHHAKXEWKARAXKNPMSLZANWXLXIJWAX"
```

**Decrypt from a file:**
```bash
./vigenere-cracker.py ciphertext.txt
```

### Advanced Options

**With a known key:**
```bash
./vigenere-cracker.py ciphertext.txt -k "VIGENERE"
```

**Try multiple specific keys:**
```bash
./vigenere-cracker.py ciphertext.txt -t "BELLASO,VIGENERE,KASISKI"
```

**With known key length:**
```bash
./vigenere-cracker.py ciphertext.txt -l 6
```

**Custom flag format:**
```bash
./vigenere-cracker.py ciphertext.txt -f "flag{.*?}"
```

**Save results:**
```bash
./vigenere-cracker.py ciphertext.txt -o results.txt
```

## 🛠️ Available Options

| Option | Description |
|--------|-------------|
| `-k, --key KEY` | Use a specific key for decryption |
| `-f, --flag-format FORMAT` | Set custom flag format (regex pattern, default: `texsaw{.*?}`) |
| `-t, --try-keys KEYS` | Try a comma-separated list of keys |
| `-l, --key-length LENGTH` | Specify the key length if known |
| `-o, --output FILE` | Save results to a file |
| `-v, --verbose` | Enable verbose output with detailed analysis |
| `-s, --silent` | Disable most output (useful for scripting) |

## 🔬 How It Works

### 1. Key Length Analysis
The Kasiski examination looks for repeated sequences in the ciphertext, as these have a high probability of being encrypted with the same portion of the key. The distances between these repetitions are likely to be multiples of the key length.

```
Plaintext:  ATTACKATDAWN
Key:        LEMONLEMONLE
Ciphertext: LXFOPVEFRNHR
```

Our tool calculates the greatest common divisors of these distances to identify the most probable key length.

### 2. Key Recovery
Once the key length is determined, the ciphertext is split into columns, with each column encrypted by the same letter of the key. By analyzing the frequency distribution in each column and comparing to expected English letter frequencies, we can determine the most likely shift for each position.

### 3. Flag Extraction
After decryption, the tool searches for common flag formats and contextual markers that often surround flags in CTF challenges.

## 📊 Example Output

```
[*] Read ciphertext (452 characters)
[*] Possible key lengths: [6, 3, 12, 9, 4]
[*] Trying key with length 6: SAWTEX
[+] Decrypted with key SAWTEX:
OMGHEYYOUFIGUREDOUTTHECIPHERTHEKEYWASNTTOOHARDTOFINDWASITYOUSHOULDBEVERYPROUDOFYOURSELFALLYOUHADTODOWASUSETH
EKASISKITESTTOFINDTHELENGTHOFTHEKEYTHENDIVIDETHEMESSAGEINTOSEGMENTSOFTHEKEYSIZETHENUSEALITTLEBITOFFREQUENCYA
NALYSISTOFINDTHEKEYONCEYOUHAVETHEKEYITSPRETTYSIMPLE...

[+] Found flags:
    texsaw{OMGHEYYOUFOUNDME}
```

## 📚 Cryptographic Background

The Vigenère cipher was invented by Giovan Battista Bellaso in 1553, though it is named after Blaise de Vigenère who described a stronger autokey cipher in 1586. The cipher remained unbroken for centuries and was known as "le chiffre indéchiffrable" (the indecipherable cipher).

The cipher uses a series of interwoven Caesar ciphers based on the letters of a keyword. For example, with the key "KEY":

```
Plaintext:  ATTACKATDAWN
Key:        KEYKEYKEYKEY
Ciphertext: KXEEOVATTVRU
```

Our tool leverages the inherent weaknesses of this system, particularly the repetition of the key, to recover the original message without prior knowledge of the key.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🙏 Acknowledgements

- Friedrich Kasiski for pioneering the cryptanalysis of polyalphabetic ciphers
- William F. Friedman for developing the Index of Coincidence method
- The CTF community for keeping classic ciphers relevant in modern challenges

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/kn0x0x">kn0x0x</a>
</p> 
