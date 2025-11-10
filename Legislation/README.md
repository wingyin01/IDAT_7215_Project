# Hong Kong Legislation XML Files

This folder contains official Hong Kong legislation in XML format from the e-Legislation Portal.

## 📁 Structure

```
Legislation/
├── hkel_c_leg_cap_1_cap_300_en/      # Chapters 1-300 (English)
├── hkel_c_leg_cap_301_cap_600_en/    # Chapters 301-600 (English)
└── hkel_c_leg_cap_601_cap_end_en/    # Chapters 601+ (English)
```

## 📊 Contents

- **Total Coverage**: All Hong Kong Ordinances (Chapters 1 to 658+)
- **Format**: XML files from official e-Legislation database
- **Language**: English
- **Source**: https://data.gov.hk/en-data/dataset/hk-doj-hkel-legislation-current

## 🎯 Currently Active

The expert system currently uses **5 criminal law ordinances** from `hkel_c_leg_cap_1_cap_300_en`:

1. **Cap. 200** - Crimes Ordinance (206 sections)
2. **Cap. 201** - Offences Against the Person Ordinance (52 sections)
3. **Cap. 210** - Theft Ordinance (40 sections)
4. **Cap. 221** - Dangerous Drugs Ordinance (220 sections)
5. **Cap. 245** - Public Order Ordinance (56 sections)

**Total Active: 574 sections**

## 📝 Available but Not Active

The following folders contain additional legislation that can be activated:

- **Cap. 1-300**: ~300 ordinances (civil, commercial, procedural law, etc.)
- **Cap. 301-600**: ~300 ordinances (financial, regulatory, securities, etc.)
- **Cap. 601+**: ~58 ordinances (newer legislation, companies, competition, etc.)

## 🔧 To Add More Ordinances

Edit `knowledge_base/xml_parser.py` and add ordinances to the `target_files` dictionary.

Example:
```python
target_files = {
    'cap_200': ('cap_200_en_c\\cap_200_20240323000000_en_c.xml', 'Crimes Ordinance'),
    # Add more ordinances here
    'cap_57': ('cap_57_en_c\\cap_57_XXXXXXXX000000_en_c.xml', 'Employment Ordinance'),
}
```

## ⚖️ Legal Notice

These XML files are official government data from the Hong Kong Department of Justice.
- **Copyright**: Government of Hong Kong SAR
- **Terms of Use**: https://www.elegislation.gov.hk/
- **For**: Educational and research purposes

## 📄 File Naming Convention

Files follow this pattern:
```
cap_XXX_en_c\cap_XXX_YYYYMMDD000000_en_c.xml
```

Where:
- `XXX` = Chapter number
- `YYYYMMDD` = Version date (year-month-day)
- `en` = English version
- `c` = Current version

Example: `cap_200_20240323000000_en_c.xml`
- Chapter 200
- Version dated 2024-03-23
- English, current version

