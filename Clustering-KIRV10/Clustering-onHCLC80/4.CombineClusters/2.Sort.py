import csv

d = {}

with open('10Xout.csv') as fin, open('10Xout_formatted.csv', 'w') as fout:
  fout.write('cluster_id,function,mongo_id,heavy_id,heavy_v,heavy_j,heavy_cdr3,light_id,light_v,light_j,light_cdr3,heavy_raw,light_raw')
  for line in fin:
    ls = line.strip().split(',')
    group = ls[6] + '_' + ls[11]
    fout.write(group + ',' + ','.join([ls[0], ls[1], ls[2], ls[3], ls[4], ls[6], ls[7], ls[8], ls[9], ls[11], ls[12], ls[13]]) + '\n')
