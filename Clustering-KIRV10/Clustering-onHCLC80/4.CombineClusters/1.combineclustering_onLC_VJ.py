
# it's matching everything based on the ID from the clustering file. There are 2 sets of ID's you're dealing with: the clonotype ID, and the cluster ID. 
#
# hout stores everything by cluster ID, hout_hash stores everything by clonotype ID. 
#
# The only purpose of hout_hash is so that if you come across a clonotype ID, you can check to see the cluster ID that it is a part of. 
#
# When reading in the light file, you'll come across clonotype IDs that match with the heavy, but don't have any way of knowing what cluster they came from, so it searches the hout_hash (on line 48) to see if there's an associated cluster ID. If not, then we have a light that clustered without a heavy. A later check is also done to see if there's a heavy without a light. 

import csv

FILE1="clustered-heavies-KIRV10.dat"

PAIRED='KIRV10-paired.csv'

MISSING="missing.dat"
mout = open(MISSING,'w')

hout = {}

hout_hash = {}
d = {}
cluster_index = 0
with open(FILE1) as fin:
    for line in fin:
        if "END" in line.strip():
            hout[hc_id] = d
            d = {}
            cluster_index += 1
        else:
            ls = line.strip().split(' ')
            hc_id = ls[3]+'_'+ls[4]+'_'+str(len(ls[5]))+'_'+str(cluster_index)
            if ls[0] not in d:
                d[ls[0]] = {'heavies': [], 'lights': []}
                hout_hash[ls[0]] = []
            d[ls[0]]['heavies'].append({'cluster': hc_id, 'ls': ls})
            
            hout_hash[ls[0]].append(hc_id)
            
cluster_index = 0

light_clusters = {}
with open(PAIRED) as fin:
    fin.readline()
    for line in fin:
        ls = line.strip().split(',')
        clonotype_id = ls[0] + '_' + ls[1] + '_' + ls[3]
        cluster_id = ls[19] + '_' + ls[20]
        
        d = None
        if clonotype_id not in hout_hash:
            mout.write(clonotype_id + '\n')
            continue
            
        for h in hout_hash[clonotype_id]:
            if clonotype_id in hout[h]:
                d = hout[h]
                break
            
        if not d:
            print("Missing:", clonotype_id)
        else:
            d[clonotype_id]['lights'].append({'cluster_id': cluster_id, 'ls': ls})

            

i = 0
for key in hout:
    if i > 10:
        break
        
    i += 1
    
mout.close()

with open('10Xout.csv', 'w') as fout:
    fout.write('function,mongo_id,heavy_id,heavy_v,heavy_j,heavy_cdr3,heavy_cluster,light_id,light_v,light_j,light_cdr3,light_cluster,heavy_raw,light_raw\n')
    for cluster_id in hout:
        for mid in hout[cluster_id]:
            d = hout[cluster_id][mid]
            if len(d['heavies']) == 0 or len(d['lights']) == 0:
                print(mid,'doesnt have a light or heavy')
                continue
            hls = d['heavies'][0]['ls']
            lls = d['lights'][0]['ls']
            #print(lls)
            fout.write(hls[2] +','+ hls[0] + ',' + hls[1] + ',' + hls[3] + ',' + hls[4] + ',' + hls[5] + ',' + cluster_id + ',' + lls[3] + ',' + lls[19] + ',' + lls[20] + ',' + lls[22] + ',' + d['lights'][0]['cluster_id'] + ',' + hls[7] + ',' + lls[30] + '\n')
# -


