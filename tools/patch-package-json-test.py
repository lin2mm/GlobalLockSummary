import json

with open('package.json', 'r', encoding='utf-8') as f:
    pkg = json.load(f)

test_script = pkg['scripts']['test']
if 'no-duplicate-h1.test.mjs' not in test_script:
    pkg['scripts']['test'] = test_script + ' && node tests/no-duplicate-h1.test.mjs'
    with open('package.json', 'w', encoding='utf-8') as f:
        json.dump(pkg, f, indent=2)
    print("Added no-duplicate-h1 test to package.json scripts!")
else:
    print("Already exists in package.json")

