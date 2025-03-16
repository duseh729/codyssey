file = []

uri = 'C:/Users/duseh/OneDrive/바탕 화면/동미대/코디세이/1주차/'

try:
    file = open(uri + 'mission_computer_main.log', 'r')
except Exception as e:
    print('error', e)
    exit(0)

str = file.read().split('\n')[1:];

# print(str)

str_reverse = sorted(str, reverse=True)

for s in str_reverse:
    print(s)

write_file = open(uri + 'fail_log.log', 'w')
for s in str_reverse[1:3]:
    write_file.write(s + '\n')
write_file.close()
