"""
Utilities for working with monoalphabetic ciphers.
Includes tools for cracking several well-known ciphers.
"""

import string
import operator
import collections
from fractions import gcd

import util
import freq

#################################
# GENERIC MONOALPHABETIC CIPHER #
#################################

def encrypt_substitution(plaintext, dictionary):
    """
    Encrypt a plaintext using a substitution cipher.

    Args:
        plaintext: the text to encrypt.
        dictionary: the replacement table for symbols in the plaintext.

    Returns:
        the plaintext encrypted using the replacement dictionary specified.
    """
    alphabet = dictionary.keys()
    return "".join(map(lambda c: dictionary[c] if c in alphabet else c, plaintext))

def decrypt_substitution(ciphertext, dictionary):
    """
    Decrypts a ciphertext using a substitution cipher.

    Args:
        ciphertext: the ciphertext to decrypt.
        dictionay: the replacement table for symbols in the ciphertext.
                   WILL BE INVERTED, so specify the one that was used for encryption.

    Returns:
        the ciphertext decrypted using the replacement dictionary specified.
    """
    inverse = {v: k for k,v in dictionary.items()}
    return encrypt_substitution(ciphertext, inverse)

def crack_substitution(ciphertext, frequencies=freq.english):
    """ #TODO: Create a hill-climbing frequency-based cracker for substitution ciphers. """
    pass

def generic_crack(ciphertext, candidates, frequencies=freq.english, alphabet=string.uppercase):
    distances = []
    for candidate in candidates:
        trial = encrypt_substitution(ciphertext, candidate)
        candidate_freq = freq.text(trial, alphabet)
        distances.append(util.squared_differences(candidate_freq, frequencies))
    guess = distances.index(min(distances))
    return (candidates[guess], encrypt_substitution(ciphertext, candidates[guess]))

def crack_shift(ciphertext, alphabet=string.uppercase, frequencies=freq.english):
    """
    Crack a Shift-cipher using squared differences between frequency distributions.

    Args:
        ciphertext: the ciphertext to crack.
        alphabet: the alphabet of symbols that the ciphertext consists of.
                  symbols not in the alphabet will be ignored.
        frequencies: the target frequency distribution to compare against when cracking.

    Returns:
        a tuple (k, p) consisting of the shift amount and the plaintext of the broken cipher.
    """
    candidates = [shift_dict(i, alphabet) for i in range(len(alphabet))]
    (dictionary, plaintext) = generic_crack(ciphertext, candidates, frequencies, alphabet)
    shift = (key for key,value in dictionary.items() if value == alphabet[0]).next()
    return (alphabet.index(shift), plaintext)

def crack_affine(ciphertext, alphabet=string.uppercase, frequencies=freq.english):
    """
    Crack an Affine-cipher using squared differences between frequency distributions.

    Args:
        ciphertext: the ciphertext to crack.
        alphabet: the alphabet of symbols that the ciphertext consists of.
                  symbols not in the alphabet will be ignored.
        frequencies: the target frequency distribution to compare against when cracking.

    Returns:
        #TODO: Return a tuple with the key, format (key, plaintext)
        the plaintext of the broken cipher.
    """
    n = len(alphabet)
    invertible = [i for i in range(n) if gcd(i,n) == 1]
    keys = [(a,b) for a in invertible for b in range(n)]
    candidates = [affine_dict(k) for k in keys]
    return generic_crack(ciphertext, candidates, frequencies)

############################
# SPECIFIC IMPLEMENTATIONS #
############################

#TODO: Rewrite monoalphabetic ciphers for speed instead of code reuse.

def shift_dict(shift=3, alphabet=string.uppercase):
    """
    Generate a Shift-cipher dictionary for use as a generic substitution cipher.

    Args:
        shift: the shift to apply to symbols in the alphabet.
        alphabet: an alphabet of symbols that the plaintext consists of.

    Returns:
        a dictionary ready for use with the encrypt_substitution method.
    """
    return affine_dict((1,shift), alphabet)

def affine_dict(key, alphabet=string.uppercase):
    """
    Generate a Affine-cipher dictionary for use as a generic substitution cipher.

    Args:
        key: the Affine-cipher key specified in the format (a, b).
             the a-component must have a multiplicative inverse mod len(alphabet)
        alphabet: an alphabet of symbols that the plaintext consists of.

    Returns:
        a dictionary ready for use with the encrypt_substitution method.
    """
    (a, b) = key
    n = len(alphabet)
    return {alphabet[i]: alphabet[(a * i + b) % n] for i in range(n)}

def atbash_dict(alphabet=string.uppercase):
    """
    Generate a Atbash-cipher dictionary for use as a generic substitution cipher.

    Args:
        alphabet: an alphabet of symbols that the plaintext consists of.

    Returns:
        a dictionary ready for use with the encrypt_substitution method.
    """
    n = len(alphabet)
    return affine_dict((n - 1, n - 1), alphabet)

def encrypt_shift(plaintext, key, alphabet=string.uppercase):
    """
    Encrypt a text using a Shift-cipher.

    Args:
        plaintext: the text to encrypt.
        key: the shift to apply to the symbols in the text.
        alphabet: the alphabet of symbols that the cipher is defined over.
                  symbols not in the alphabet will be ignored.
    """
    return encrypt_substitution(plaintext, shift_dict(key, alphabet))

def decrypt_affine(ciphertext, key, alphabet=string.uppercase):
    """
    Encrypt a text using an Affine-cipher.

    Args:
        plaintext: the text to encrypt.
        key: the key to use for the cipher, in the format (a,b)
             the a-component must have a multiplicative inverse mod len(alphabet)
        alphabet: the alphabet of symbols that the cipher is defined over.
                  symbols not in the alphabet will be ignored.
    """
    return decrypt_substitution(ciphertext, affine_dict(key, alphabet))
