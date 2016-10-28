#!/usr/bin/env/ python

def sense(p, colors, sensing_color, sensor_right):
    result = [[] for y in range(len(p))] 
    pHit   = sensor_right
    pMiss  = 1 - sensor_right
    
    for i in range(len(p)):
        for j in range(len(p[0])):
            hit = (sensing_color == colors[i][j]) 
            result[i].append(float(p[i][j] * (hit * pHit + (1-hit) * pMiss)))
    
    s = sum(map(sum, result))
    
    for i in range(len(result)):
        for j in range(len(result[0])):
            result[i][j] = result[i][j] / s
    
    return result
    
def move(p, v_motion, h_motion, p_move):
    result     = [[] for y in range(len(p))]
    p_not_move = 1 - p_move
    
    for i in range(len(p)):
        for j in range(len(p[0])):
            s = float(p_move * p[(i - v_motion) % len(p)][(j - h_motion) % len(p[0])])
            s = float(s + p_not_move * p[(i - v_motion + 1 * v_motion) % len(p)][(j - h_motion + 1 * h_motion) % len(p[0])])
            result[i].append(s)
            
    return result

def localize(colors, measurements, motions, sensor_right, p_move):
    # initializes p to a uniform distribution over a grid of the same dimensions as colors
    pinit = 1.0 / float(len(colors)) / float(len(colors[0]))
    p     = [[pinit for row in range(len(colors[0]))] for col in range(len(colors))]
    for i in range(len(motions)):
        p = move(p, motions[i][0], motions[i][1], p_move) 
        p = sense(p, colors, measurements[i], sensor_right)
    return p

def show(p):
    rows = ['[' + ','.join(map(lambda x: '{0:.5f}'.format(x),r)) + ']' for r in p]
    print '[' + ',\n '.join(rows) + ']'
    
colors = [['R','G','G','R','R'],
          ['R','R','G','R','R'],
          ['R','R','G','G','R'],
          ['R','R','R','R','R']]
measurements = ['G','G','G','G','G']
motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]
p = localize(colors,measurements,motions,sensor_right = 0.7, p_move = 0.8)
show(p)
