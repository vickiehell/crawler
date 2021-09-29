import re
lst=re.findall("\d+","我的电话号码是09823447")
print(lst)
itt=re.finditer("\d+","我的电话号码是038493875")
print(itt)
for i in itt:
    print(i.group())
