from requests import post
import time
base_url = 'https://europe-west1-gnocchi-test-415019.cloudfunctions.net/save_data_1_bq'

sensor = 's1'

with open('HomeC.csv') as f:
    for l in f.readlines()[0:58]:
        t = int(l.strip().split(',')[0])
        v0 = list(map(float, l.strip().split(',')[1:20]))
        v1 = list(map(float, l.strip().split(',')[21:23]))
        v2 = list(map(float, l.strip().split(',')[24:27]))
        v3 = list(map(float, l.strip().split(',')[28:]))
        s0 = l.strip().split(',')[20:21]
        s1 = l.strip().split(',')[23:24]
        s2 = l.strip().split(',')[27:28]
        #print({'sensor': sensor, 'tempo': t, 'val': v0+v1+v2+v3, 'stringhe': s0+s1+s2})
        r = post(f'{base_url}', json={'sensor': sensor, 'tempo': t, 'valori': v0+v1+v2+v3, 'stringhe': s0+s1+s2})
        print(r.text)
        '''with open('graph.html', 'w') as file:
            file.write(r.text)'''
        time.sleep(3)
with open('HomeC.csv') as f:
    for l in f.readlines()[58:]:
        t = int(l.strip().split(',')[0])
        v0 = list(map(float,l.strip().split(',')[1:20]))
        v1 = list(map(float,l.strip().split(',')[21:23]))
        v4 = list(map(float,l.strip().split(',')[24:]))
        s0 = l.strip().split(',')[20:21]
        s1 = l.strip().split(',')[23:24]
        #print({'sensor': sensor, 'tempo': t, 'val': v0 + v1 + v4, 'stringhe': s0+s1})
        r = post(f'{base_url}', json={'sensor': sensor, 'tempo': t, 'valori': v0+v1+v4, 'stringhe': s0+s1})
        print(r.text)
        '''with open('graph.html', 'w') as file:
            file.write(r.text)'''
        time.sleep(3)
print('done')


