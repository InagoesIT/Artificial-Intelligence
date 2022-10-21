priority_queue = []
priority_queue.append((5, (2, 3), True))
priority_queue.append((1, (4, 5), False))
priority_queue.append((3, (4, 5), True))
priority_queue.append((3, (4, 5), True))
priority_queue.sort()
states_set = dict()
resulting_dict = dict()

for score, state, explored in priority_queue:
    if state in resulting_dict and score >= resulting_dict[state][0]:
        continue
    resulting_dict[state] = (score, explored)
print(resulting_dict)

new_queue = []
for key in resulting_dict:
    new_queue.append((resulting_dict[key][0], key, resulting_dict[key][0]))

print(new_queue)
