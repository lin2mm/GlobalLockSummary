with open('tests/site.test.mjs', 'r', encoding='utf-8') as f:
    test_code = f.read()

test_code = test_code.replace("const DEFAULT_LABEL = '智能改造产品';", "const DEFAULT_LABEL = '后装智能锁';")
test_code = test_code.replace("const EN_LABEL = 'Retrofit hardware';", "const EN_LABEL = 'Retrofit Smart Lock';")

with open('tests/site.test.mjs', 'w', encoding='utf-8') as f:
    f.write(test_code)

print("Updated tests/site.test.mjs labels!")
