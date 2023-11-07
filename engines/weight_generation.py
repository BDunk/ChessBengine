LOCATION_WEIGHTS = {}

LOCATION_WEIGHTS['P'] = []
LOCATION_WEIGHTS['R'] = []
LOCATION_WEIGHTS['N'] = []
LOCATION_WEIGHTS['B'] = []
LOCATION_WEIGHTS['Q'] = []
LOCATION_WEIGHTS['K'] = []


weight_j_p = [0.95, 0.95, 0.975, 0.975, 0.975, 0.975, 0.95, 0.95]
weight_i_p = [0, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 0]

weight_j_r = [0.95, 0.95, 0.975, 0.975, 0.975, 0.975, 0.95, 0.95]
weight_i_r = [0.95, 0.95, 0.975, 0.975, 0.975, 0.975, 0.95, 0.95]

weight_j_n = [0.95, 0.95, 0.975, 0.975, 0.975, 0.975, 0.95, 0.95]
weight_i_n = [0.95, 0.95, 0.975, 0.975, 0.975, 0.975, 0.95, 0.95]

weight_j_b = [0.95, 0.95, 0.975, 0.975, 0.975, 0.975, 0.95, 0.95]
weight_i_b = [0.95, 0.95, 0.975, 0.975, 0.975, 0.975, 0.95, 0.95]

weight_j_q = [0.95, 0.95, 0.975, 0.975, 0.975, 0.975, 0.95, 0.95]
weight_i_q = [0.95, 0.95, 0.975, 0.975, 0.975, 0.975, 0.95, 0.95]

weight_i_k = [1,1,1,1,1,1,1,1]
weight_j_k = [1,1,1,1,1,1,1,1]
for ii in range(8):
    for jj in range(8):
        LOCATION_WEIGHTS['P'].append(round(weight_i_p[ii]*weight_j_p[jj],2))
        LOCATION_WEIGHTS['R'].append(round(weight_i_r[ii]*weight_j_r[jj],2))
        LOCATION_WEIGHTS['N'].append(round(weight_i_n[ii]*weight_j_n[jj],2))
        LOCATION_WEIGHTS['B'].append(round(weight_i_b[ii]*weight_j_b[jj],2))
        LOCATION_WEIGHTS['Q'].append(round(weight_i_q[ii]*weight_j_q[jj],2))
        LOCATION_WEIGHTS['K'].append(round(weight_i_k[ii]*weight_j_k[jj],2))
PIECE_WEIGHTS = {'P':1,'R':5,'N':3,'B':3,'Q':9,'K':1} 
WEIGHTS = {'LOCATION':LOCATION_WEIGHTS, 'PIECE':PIECE_WEIGHTS}
