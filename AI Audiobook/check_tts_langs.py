from gtts import lang

print("Supported languages:")
languages = lang.tts_langs()
required_langs = ['en', 'hi'] # en-in is a dialect of en, usually supported via 'tld' or just 'en', but gTTS often treats 'en' with accents. 
# actually gTTS uses 'tld' for accents in some versions, but 'en-in' might be a valid lang code in older/specific versions or google translate api.
# Let's check what's available.

for code, name in languages.items():
    print(f"{code}: {name}")

# Check specifically for the ones we use
print("\nChecking used codes:")
for code in ['en', 'en-in', 'hi']:
    if code in languages:
        print(f"✅ {code} is supported directly.")
    else:
        print(f"❓ {code} might need specific handling (e.g. tld='co.in' for English India).")
