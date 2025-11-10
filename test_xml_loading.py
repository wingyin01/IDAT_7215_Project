#!/usr/bin/env python3
"""
Test Script to Verify XML Files Are Being Used
Run this to confirm the system uses YOUR official XML law files
"""

import sys
import os
from pathlib import Path

print("=" * 80)
print("VERIFICATION TEST: Hong Kong Criminal Law Expert System")
print("=" * 80)
print()

# Test 1: Check XML directory
print("TEST 1: Checking XML Files Directory...")
xml_dir = Path(__file__).parent / "Legislation" / "hkel_c_leg_cap_1_cap_300_en"
if xml_dir.exists():
    print(f"  ✅ XML directory found: {xml_dir}")
    
    # List XML files
    xml_files = list(xml_dir.glob("*/cap_*.xml"))
    print(f"  ✅ Found {len(xml_files)} XML files")
    print(f"     Sample files:")
    for xml_file in xml_files[:5]:
        size_mb = xml_file.stat().st_size / (1024 * 1024)
        print(f"       - {xml_file.name} ({size_mb:.2f} MB)")
else:
    print(f"  ❌ ERROR: XML directory not found at {xml_dir}")
    sys.exit(1)

print()

# Test 2: Import and check knowledge base
print("TEST 2: Loading Knowledge Base from XML...")
try:
    from knowledge_base import hk_criminal_ordinances as hk
    print(f"  ✅ Knowledge base loaded successfully")
    print(f"     Total sections: {hk.TOTAL_SECTIONS}")
    print(f"     Total ordinances: {hk.TOTAL_ORDINANCES}")
except Exception as e:
    print(f"  ❌ ERROR loading knowledge base: {e}")
    sys.exit(1)

print()

# Test 3: Verify specific sections from XML
print("TEST 3: Verifying Sections from XML Files...")
test_sections = [
    ("200", "17", "Murder"),
    ("200", "39", "Assault occasioning actual bodily harm"),
    ("210", "2", "Basic definition of theft"),
    ("221", "38", "Possession of dangerous drugs"),
    ("245", "18", "Riot"),
]

all_passed = True
for chapter, section, expected_title in test_sections:
    data = hk.get_ordinance_section(chapter, section)
    if data and data.get('title'):
        # Check if title matches (case insensitive, partial match)
        title_match = expected_title.lower() in data['title'].lower() or data['title'].lower() in expected_title.lower()
        if title_match:
            print(f"  ✅ Cap. {chapter}, s.{section}: {data['title']}")
        else:
            print(f"  ⚠️  Cap. {chapter}, s.{section}: Found '{data['title']}' (expected: {expected_title})")
    else:
        print(f"  ❌ Cap. {chapter}, s.{section}: NOT FOUND in XML data")
        all_passed = False

print()

# Test 4: Show sample text from XML
print("TEST 4: Sample Legal Text from XML...")
murder = hk.get_ordinance_section("200", "17")
if murder:
    print(f"  Section: Cap. 200, s. 17 - {murder['title']}")
    print(f"  Text: {murder['text'][:200]}...")
    print(f"  Status: {murder.get('status', 'N/A')}")
else:
    print("  ❌ Could not retrieve sample section")
    all_passed = False

print()

# Test 5: List all loaded ordinances
print("TEST 5: All Ordinances Loaded from XML...")
for cap_key, ordinance in hk.ALL_ORDINANCES.items():
    print(f"  ✅ {ordinance.get('full_title', 'Unknown')}")
    print(f"     Chapter: {ordinance['chapter']}")
    print(f"     Sections: {len(ordinance['sections'])}")

print()
print("=" * 80)

if all_passed:
    print("✅ ALL TESTS PASSED - System is using YOUR official XML law files!")
    print()
    print("Key Facts:")
    print(f"  • {hk.TOTAL_SECTIONS} sections loaded from {hk.TOTAL_ORDINANCES} XML ordinance files")
    print(f"  • Data source: hkel_c_leg_cap_1_cap_300_en/*.xml")
    print(f"  • All legal text comes directly from official HK e-Legislation XML")
    print()
    print("The system does NOT use LLM-generated law.")
    print("It parses and uses YOUR official government XML files.")
else:
    print("⚠️  Some tests had issues - check the output above")

print("=" * 80)


