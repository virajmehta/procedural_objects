import numpy as np

def get_com(fn):
    vertices, faces, _ = read_mesh(fn)
    return compute_centroid(vertices, faces)

# roll then pitch then yaw then translate
def transform_point(point, roll, pitch, yaw, x, y, z):
    roll = np.deg2rad(roll)
    pitch = np.deg2rad(pitch)
    yaw = np.deg2rad(yaw)
    roll_mat = np.array([[1, 0, 0],[0, np.cos(roll), -np.sin(roll)],[0, np.sin(roll), np.cos(roll)]])
    pitch_mat = np.array([[np.cos(pitch), 0, np.sin(pitch)],[0,1,0],[-np.sin(pitch),0,np.cos(pitch)]])
    yaw_mat = np.array([[np.cos(yaw),-np.sin(yaw),0],[np.sin(yaw),np.cos(yaw),0],[0,0,1]])
    point = roll_mat.dot(point)
    point = pitch_mat.dot(point)
    point = yaw_mat.dot(point)
    point += np.array([x,y,z])
    return point

def read_mesh(obj_file):
    vertices = []
    connections = []
    lines = []
    toRead = open(obj_file, 'rb')
    for line in toRead:
        line = line.decode('UTF-8').strip()
        lines.append(line)
        try:
            line = line.split()
            if line[0]=='v':
                vertices.append([float(x) for x in line[1:4]])
            elif line[0]=='f':
                vi = []
                nti = []
                if line[1].find('/') == -1:
                    vi = [int(x)-1 for x in line[1:]]
                else:
                    for j in range(1, len(line)):
                        # Break up like by / to read vert inds, tex coords, and normal inds
                        val = line[j]
                        tokens = val.split('/')
                        for i in range(len(tokens)):
                            if i == 0:
                                vi.append(int(tokens[i]) - 1)
                            #elif i == 1:
                            #    if tokens[i] != '':
                            #        vti.append(int(tokens[i]))
                            #elif i == 2:
                            #    nti.append(int(tokens[i]))
                connections.append(vi)
        except Exception as e:
            print(e)
            pass
    toRead.close()
    return (np.array(vertices),np.array(connections),lines)

def _signed_triangle_volume(v0, v1, v2):
    tvec = np.cross(v1, v2)
    return v0.dot(tvec) / 6.

def find_mesh_volume(vertices, triangles):
    total = 0
    for triangle in triangles:
        v0 = vertices[triangle[0], :]
        v1 = vertices[triangle[1], :]
        v2 = vertices[triangle[2], :]
        total += _signed_triangle_volume(v0, v1, v2)
    return total

def find_mesh_surface_area(vertices, triangles):
    total = 0
    for triangle in triangles:
        v0 = vertices[triangle[0], :]
        v1 = vertices[triangle[1], :]
        v2 = vertices[triangle[2], :]
        total += np.linalg.norm(np.cross(v1 - v0, v2 - v0)) / 2.
    return total

def compute_centroid(vertices, triangles):
    total = 0
    centroid = np.zeros((3))
    for triangle in triangles:
        v0 = vertices[triangle[0],:]
        v1 = vertices[triangle[1],:]
        v2 = vertices[triangle[2],:]
        area = np.linalg.norm(np.cross(v1 - v0, v2 - v0)) / 2.
        centroid += v0 * area
        centroid += v1 * area
        centroid += v2 * area
        total += area
    return centroid / (total * 3)

def write_mesh(fn, vertices, faces):
    faces += 1
    with open(fn, 'w') as f:
        for vertex in vertices:
            f.write('v {0:.6f} {1:.6f} {2:.6f}\n'.format(vertex[0], vertex[1], vertex[2]))
        for face in faces:
            f.write('f {0:d} {1:d} {2:d}\n'.format(face[0], face[1], face[2]))


