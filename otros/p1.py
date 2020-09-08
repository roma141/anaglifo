import numpy as np
import conversion

ply_header = '''ply
format ascii 1.0
element vertex %(vert_num)d
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
'''

def read_dic(filename):
    with open(filename, 'r') as f:
        dic = eval(f.read())    
    return dic

def write_ply(fn, verts, colors):
    verts = verts.reshape(-1, 3)
    colors = colors.reshape(-1, 3)
    verts = np.hstack([verts, colors])
    with open(fn, 'wb') as f:
        f.write((ply_header % dict(vert_num=len(verts))).encode('utf-8'))
        np.savetxt(f, verts, fmt='%f %f %f %d %d %d ')


dic = read_dic('curvasn.geojson')

# for d in dic:
# 	print(d) 

verts = []
colors = []

for d in dic['features']:
	print("--------------------")
	print(d['properties']['id'])
	z = d['properties']['id']
	for x in d['geometry']['coordinates'][0]:
		x, y, _, _ = conversion.from_latlon(x[1], x[0])
		print(x, y, z)
		verts.append([float(x), float(y), float(z)])
		colors.append([255,255,255])

write_ply('curvasn.ply', np.array(verts), np.array(colors))

# print(dic['features']['geometry'])
# 19.0 762938.136408956 849024.4842749152
# 19.0 762947.0229065802 848948.8404016602