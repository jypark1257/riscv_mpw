#!/usr/bin/env python3
"""
RISC-V BIOS.HEX Memory Splitter
Reads a specified .hex file and splits it into:
- imem_0.mem, imem_1.mem, imem_2.mem, imem_3.mem (IMEM)
- dmem_0.mem, dmem_1.mem, dmem_2.mem, dmem_3.mem (DMEM)
"""

import re
import os
import sys
from typing import List, Tuple

def clean_hex_input(hex_input: str) -> str:
    """Clean and validate hex input"""
    cleaned = re.sub(r'[^0-9a-fA-F]', '', hex_input)
    return cleaned.upper()

def hex_to_words(hex_string: str) -> List[str]:
    """Convert hex string to list of 32-bit words (8 hex chars each)"""
    words = []
    if len(hex_string) % 8 != 0:
        hex_string = hex_string.ljust((len(hex_string) + 7) // 8 * 8, '0')
    
    for i in range(0, len(hex_string), 8):
        word = hex_string[i:i+8]
        if len(word) == 8:
            words.append(word)
    
    return words

def word_to_bytes_little_endian(word: str) -> Tuple[str, str, str, str]:
    """Convert 32-bit word to 4 bytes in little-endian format"""
    if len(word) != 8:
        word = word.ljust(8, '0')
    
    byte0 = word[6:8]
    byte1 = word[4:6]
    byte2 = word[2:4]
    byte3 = word[0:2]
    
    return byte0, byte1, byte2, byte3

def split_memory(words: List[str]) -> Tuple[List[str], List[str]]:
    """Split words into IMEM and DMEM"""
    total_words_needed = 8192
    if len(words) < total_words_needed:
        words.extend(['00000000'] * (total_words_needed - len(words)))
    
    imem_words = words[0:4096]
    dmem_words = words[4096:8192]
    
    return imem_words, dmem_words

def create_byte_files(words: List[str]) -> Tuple[List[str], List[str], List[str], List[str]]:
    """Create 4 byte files from word list"""
    file0_bytes = []
    file1_bytes = []
    file2_bytes = []
    file3_bytes = []
    
    for word in words:
        byte0, byte1, byte2, byte3 = word_to_bytes_little_endian(word)
        file0_bytes.append(byte0)
        file1_bytes.append(byte1)
        file2_bytes.append(byte2)
        file3_bytes.append(byte3)
    
    return file0_bytes, file1_bytes, file2_bytes, file3_bytes

def save_mem_file(bytes_list: List[str], filename: str):
    """Save bytes to .mem file"""
    with open(filename, 'w') as f:
        for byte in bytes_list:
            f.write(byte + '\n')

def process_hex_file(input_file: str):
    """Main processing function with minimal output"""
    
    if not os.path.exists(input_file):
        print(f"❌ Error: {input_file} not found!")
        return False
    
    try:
        with open(input_file, 'r') as f:
            hex_input = f.read()
        
        cleaned_hex = clean_hex_input(hex_input)
        
        if len(cleaned_hex) == 0:
            print("❌ Error: No valid hex data found in input file!")
            return False
        
        words = hex_to_words(cleaned_hex)
        imem_words, dmem_words = split_memory(words)
        
        imem_bytes = create_byte_files(imem_words)
        for i, bytes_list in enumerate(imem_bytes):
            filename = f"imem_{i}.mem"
            save_mem_file(bytes_list, filename)
        
        dmem_bytes = create_byte_files(dmem_words)
        for i, bytes_list in enumerate(dmem_bytes):
            filename = f"dmem_{i}.mem"
            save_mem_file(bytes_list, filename)
        
        return True
        
    except Exception as e:
        print(f"❌ Error processing file: {e}")
        return False

def show_usage():
    """Show usage information"""
    print("Usage: python3 split_bios_fpga.py <input_hex_file>")

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("❌ Error: No input file specified!")
        show_usage()
        sys.exit(1)
        
    input_file = sys.argv[1]
    
    success = process_hex_file(input_file)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()