
with open('notif', 'r') as h:
    notifs = h.readlines()
for i in range(len(notifs)):
    j = notifs[i]
    notifs[i] = j[0:len(j)-1]

notifs = notifs[0:len(notifs)-1]

print(notifs)