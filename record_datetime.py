import datetime
import random

members = ['Aさん', 'Bさん', 'Cさん', 'Dさん', 'Eさん']

log_file = 'datetime_log.txt'
now = datetime.datetime.now()
formatted = now.strftime('%Y-%m-%d (%a.) %H:%M:%S')
selected = random.choice(members)

with open(log_file, 'a') as f:
    f.write(f'{formatted}  {selected}\n')

print(f'追記しました: {formatted}  {selected}')
