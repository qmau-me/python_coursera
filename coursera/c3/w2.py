import re

file = open('regex_sum_195288.txt')
sum = 0
for line in file:
  line = line.rstrip()
  y = re.findall('[0-9]+', line)
  for num in y:
    sum += int(num)
print(sum)
