#!/usr/bin/env python3

# Fix Phase 8.1 Freeze Report terminology
import re

def main():
    # Read the file
    with open('C:\Users\User10\Documents\MRV\yuvi\QuantForge\docs\PHASE8_1_FREEZE_APPROVED.md', 'r') as f:
        content = f.read()

    # Fix 1: Replace PERMANENTLY FREEZED with PERMANENTLY FROZEN
    content = content.replace('PERMANENTLY FREEZED', 'PERMANENTLY FROZEN')

    # Fix 2: Replace CONSTRUCTIONALLY APPROVED with CONSTITUTIONALLY APPROVED
    content = content.replace('CONSTRUCTIONALLY APPROVED', 'CONSTITUTIONALLY APPROVED')

    # Fix 3: Replace **CONSTRUCTIONALLY APPROVED** with **CONSTITUTIONALLY APPROVED**
    content = content.replace('**CONSTRUCTIONALLY APPROVED**', '**CONSTITUTIONALLY APPROVED**')

    # Write back
    with open('C:\Users\User10\Documents\MRV\yuvi\QuantForge\docs\PHASE8_1_FREEZE_APPROVED.md', 'w') as f:
        f.write(content)

    print('Terminology fixed successfully')

if __name__ == '__main__':
    main()
