import copy
next_move = {}
flag = 0
evalmatrix = [[99, -8, 8, 6, 6, 8, -8, 99],
              [-8, -24, -4, -3, -3, -4, -24, -8],
              [8, -4, 7, 4, 4, 7, -4, 8],
              [6, -3, 4, 0, 0, 4, -3, 6],
              [6, -3, 4, 0, 0, 4, -3, 6],
              [8, -4, 7, 4, 4, 7, -4, 8],
              [-8, -24, -4, -3, -3, -4, -24, -8],
              [99, -8, 8, 6, 6, 8, -8, 99]]

row_value = ["a", "b", "c", "d", "e", "f", "g", "h"]
col_value = ["1", "2", "3", "4", "5", "6", "7", "8"]

def convertvalues(depth, evalue, alpha_beta_dict):
    if alpha_beta_dict[depth][0] == - 10000:
        minf = "-Infinity"
    else:
        minf = str(alpha_beta_dict[depth][0])

    if alpha_beta_dict[depth][1] == 10000:
        pinf = "Infinity"
    else:
        pinf = str(alpha_beta_dict[depth][1])

    if evalue == 10000:
        ev = "Infinity"
    elif evalue == -10000:
        ev = "-Infinity"
    else:
        ev = str(evalue)

    s = ev + "," + minf + "," + pinf
    return s

def findnextmove(playersecond, position):
    possiblevalues = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
    conversion = {}
    conv_key = []
    if playersecond == "O":
        oppplayer = "X"
    else:
        oppplayer = "O"
    position[playersecond].sort()
    for i in position[playersecond]:
        for k in xrange(0, 8):
            x = (i[0] + possiblevalues[k][0])
            y = (i[1] + possiblevalues[k][1])
            if x > 7 or x < 0 or y > 7 or y < 0:
                continue

            if [x, y] in position["O"]:
                continue
            elif [x, y] in position["X"]:
                continue

            else:
                con_list = []
                con_list.append([i[0], i[1]])
                diffx = i[0] - x
                diffy = i[1] - y
                counter = 1
                newx = i[0]
                newy = i[1]
                while (0 <= newx < 8 and 0 <= newy < 8):
                    newx += diffx
                    newy += diffy

                    if [newx, newy] in position[oppplayer]:
                        conversion[x, y] = con_list
                        conv_key.append([x, y])
                        break
                    elif [newx, newy] not in position["O"] and [newx, newy] not in position["X"]:
                        break
                    elif [newx, newy] in position[playersecond]:
                        con_list.append([newx, newy])
    return conv_key, conversion

def traverse(playerfirst, depth, depth_dict, d_dict, alpha_beta_dict, a_b_dict, parent, par, val_dict, v_dict):
    global flag
    global next_move
    global init_player
    global output_lines

    if (depth == original_depth or (parent[depth] == [9,9] and parent[depth-1] == [9,9])):
        evalue = 0
        for ij in depth_dict[depth]:

            for j in depth_dict[depth][ij]:

                if init_player == "X":

                    if ij == "X":
                        evalue = evalue + evalmatrix[j[0]][j[1]]
                    else:
                        evalue = evalue - evalmatrix[j[0]][j[1]]

                elif init_player == "O":
                    if ij == "X":
                        evalue = evalue - evalmatrix[j[0]][j[1]]
                    else:
                        evalue = evalue + evalmatrix[j[0]][j[1]]

        v_dict[depth] = evalue
        val_dict[depth] = v_dict[depth]
        v_dict = copy.deepcopy(val_dict)

        if depth == 0:

            #print "root"+ "," +str(depth)+ "," + convertvalues(depth, evalue, alpha_beta_dict)
            output_lines.append("root" + "," + str(depth) + "," + convertvalues(depth, evalue, alpha_beta_dict))
            for vv in xrange(1, len(vv_d)):
                val_dict[vv] = copy.deepcopy(vv_d[vv])
                v_dict[vv] = copy.deepcopy(vv_d[vv])

        elif parent[depth] == [9, 9]:
            #print "pass"+ "," + str(depth)+ "," + convertvalues(depth, evalue, alpha_beta_dict)
            output_lines.append("pass"+ "," + str(depth)+ "," + convertvalues(depth, evalue, alpha_beta_dict))

        else:
            #print row_value[parent[depth][1]] + col_value[parent[depth][0]]+ "," + str(depth)+ "," + convertvalues(depth, evalue, alpha_beta_dict)
            output_lines.append(row_value[parent[depth][1]] + col_value[parent[depth][0]]+ "," + str(depth)+ "," + convertvalues(depth, evalue, alpha_beta_dict))


        return evalue

    else:
        if depth == 0:
            #print "root"+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict)
            output_lines.append("root"+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict))
            for vv in xrange(1, len(vv_d)):
                val_dict[vv] = copy.deepcopy(vv_d[vv])
                v_dict[vv] = copy.deepcopy(vv_d[vv])

        elif parent[depth] == [9, 9]:
            #print "pass"+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict)
            output_lines.append("pass"+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict))
        else:
            #print row_value[parent[depth][1]] + col_value[parent[depth][0]]+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict)
            output_lines.append(row_value[parent[depth][1]] + col_value[parent[depth][0]]+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict))


        if playerfirst == "O":
            conv_key, conversion = findnextmove("X", depth_dict[depth])
        else:
            conv_key, conversion = findnextmove("O", depth_dict[depth])

        conv_key.sort()
        if len(conv_key) == 0:
            flag = 1
            depth_dict[depth + 1] = d_dict[depth]
            d_dict = copy.deepcopy(depth_dict)

            par[depth + 1] = [9, 9]
            parent[depth + 1] = par[depth + 1]
            par = copy.deepcopy(parent)

            if playerfirst == "X":
                v = traverse("O", depth + 1, depth_dict, d_dict, alpha_beta_dict, a_b_dict, parent, par, val_dict, v_dict)
                if (depth) % 2 == 1:
                    v_dict = copy.deepcopy(val_dict)
                    if v< val_dict[depth]:
                        v_dict[depth] = v
                        val_dict[depth] = v_dict[depth]
                        v_dict = copy.deepcopy(val_dict)

                    if v < alpha_beta_dict[depth][1] and v > alpha_beta_dict[depth][0]:
                        a_b_dict[depth][1] = v
                        alpha_beta_dict[depth][1] = a_b_dict[depth][1]
                        a_b_dict = copy.deepcopy(alpha_beta_dict)

                    if parent[depth] == [-1, -1]:
                        #print "root"+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict)
                        output_lines.append("root"+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict))
                        for vv in xrange(1, len(vv_d)):
                            val_dict[vv] = copy.deepcopy(vv_d[vv])
                            v_dict[vv] = copy.deepcopy(vv_d[vv])

                    elif parent[depth] == [9, 9]:
                        #print "pass"+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict)
                        output_lines.append("pass"+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict))
                    else:
                        #print row_value[parent[depth][1]] + col_value[parent[depth][0]]+ ","+ str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict)
                        output_lines.append(row_value[parent[depth][1]] + col_value[parent[depth][0]]+ ","+ str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict))

                    if val_dict[depth] <= alpha_beta_dict[depth][0]:
                        temp = copy.deepcopy(val_dict[depth])
                        if depth % 2 == 1:
                            v_dict[depth] = 10000
                        else:
                            v_dict[depth] = -10000
                        val_dict[depth] = v_dict[depth]
                        v_dict = copy.deepcopy(val_dict)
                        # print "eqe"
                        return temp
                else:
                    v_dict = copy.deepcopy(val_dict)
                    if v > val_dict[depth]:
                        v_dict[depth] = v
                        val_dict[depth] = v_dict[depth]
                        v_dict = copy.deepcopy(val_dict)

                    if v < alpha_beta_dict[depth][1] and v > alpha_beta_dict[depth][0]:
                        a_b_dict[depth][0] = v
                        alpha_beta_dict[depth][0] = a_b_dict[depth][0]
                        a_b_dict = copy.deepcopy(alpha_beta_dict)

                    if parent[depth] == [-1, -1]:
                        #print "root" + "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict)
                        output_lines.append("root" + "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict))
                        for vv in xrange(1, len(vv_d)):
                            val_dict[vv] = copy.deepcopy(vv_d[vv])
                            v_dict[vv] = copy.deepcopy(vv_d[vv])

                    elif parent[depth] == [9, 9]:
                        #print "pass"+ "," +str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict)
                        output_lines.append("pass"+ "," +str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict))
                    else:
                        #print row_value[parent[depth][1]] + col_value[parent[depth][0]]+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict)
                        output_lines.append(row_value[parent[depth][1]] + col_value[parent[depth][0]]+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict))

                    if val_dict[depth] >= alpha_beta_dict[depth][1]:
                        temp = copy.deepcopy(val_dict[depth])
                        if depth % 2 == 1:
                            v_dict[depth] = 10000
                        else:
                            v_dict[depth] = -10000
                        val_dict[depth] = v_dict[depth]
                        v_dict = copy.deepcopy(val_dict)
                        return temp

                temp = copy.deepcopy(val_dict[depth])
                if depth % 2 == 1:
                    v_dict[depth] = 10000
                else:
                    v_dict[depth] = -10000
                val_dict[depth] = v_dict[depth]
                v_dict = copy.deepcopy(val_dict)
                return temp

            else:
                v = traverse("X", depth + 1, depth_dict, d_dict, alpha_beta_dict, a_b_dict, parent, par, val_dict, v_dict)

                if (depth) % 2 == 1:
                    v_dict = copy.deepcopy(val_dict)
                    if v < val_dict[depth]:
                        v_dict[depth] = v
                        val_dict[depth] = v_dict[depth]
                        v_dict = copy.deepcopy(val_dict)

                    if v < alpha_beta_dict[depth][1] and v > alpha_beta_dict[depth][0]:
                        a_b_dict[depth][1] = v
                        alpha_beta_dict[depth][1] = a_b_dict[depth][1]
                        a_b_dict = copy.deepcopy(alpha_beta_dict)

                    if parent[depth] == [-1, -1]:
                        #print "root"+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict)
                        output_lines.append("root"+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict))
                        for vv in xrange(1, len(vv_d)):
                            val_dict[vv] = copy.deepcopy(vv_d[vv])
                            v_dict[vv] = copy.deepcopy(vv_d[vv])

                    elif parent[depth] == [9, 9]:
                        #print "pass"+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict)
                        output_lines.append("pass"+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict))
                    else:
                        #print row_value[parent[depth][1]] + col_value[parent[depth][0]]+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict)
                        output_lines.append(row_value[parent[depth][1]] + col_value[parent[depth][0]]+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict))

                    if val_dict[depth] <= alpha_beta_dict[depth][0]:
                        temp = copy.deepcopy(val_dict[depth])
                        if depth % 2 == 1:
                            v_dict[depth] = 10000
                        else:
                            v_dict[depth] = -10000
                        val_dict[depth] = v_dict[depth]
                        v_dict = copy.deepcopy(val_dict)
                        # print "eqe"
                        return temp
                else:
                    v_dict = copy.deepcopy(val_dict)
                    if v > val_dict[depth]:
                        v_dict[depth] = v
                        val_dict[depth] = v_dict[depth]
                        v_dict = copy.deepcopy(val_dict)

                    if v < alpha_beta_dict[depth][1] and v > alpha_beta_dict[depth][0]:
                        a_b_dict[depth][0] = v
                        alpha_beta_dict[depth][0] = a_b_dict[depth][0]
                        a_b_dict = copy.deepcopy(alpha_beta_dict)

                    if parent[depth] == [-1, -1]:
                        #print "root"+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict)
                        output_lines.append("root"+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict))
                        for vv in xrange(1, len(vv_d)):
                            val_dict[vv] = copy.deepcopy(vv_d[vv])
                            v_dict[vv] = copy.deepcopy(vv_d[vv])

                    elif parent[depth] == [9, 9]:
                        #print "pass"+ "," + str(depth), val_dict[depth], alpha_beta_dict[depth]
                        output_lines.append("pass"+ "," + str(depth), val_dict[depth], alpha_beta_dict[depth])
                    else:
                        #print row_value[parent[depth][1]]+ col_value[parent[depth][0]]+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict)
                        output_lines.append(row_value[parent[depth][1]]+ col_value[parent[depth][0]]+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict))

                    if val_dict[depth] >= alpha_beta_dict[depth][1]:
                        temp = copy.deepcopy(val_dict[depth])
                        if depth % 2 == 1:
                            v_dict[depth] = 10000
                        else:
                            v_dict[depth] = -10000
                        val_dict[depth] = v_dict[depth]
                        v_dict = copy.deepcopy(val_dict)
                        return temp

                temp = copy.deepcopy(val_dict[depth])
                if depth % 2 == 1:
                    v_dict[depth] = 10000
                else:
                    v_dict[depth] = -10000
                val_dict[depth] = v_dict[depth]
                v_dict = copy.deepcopy(val_dict)
                # print "eqe"
                return temp
        else:
            for i in conv_key:
                alpha_beta_dict[depth + 1] = a_b_dict[depth]
                a_b_dict = copy.deepcopy(alpha_beta_dict)

                par[depth + 1] = i
                parent[depth + 1] = par[depth + 1]
                par = copy.deepcopy(parent)

                try:
                    dep = depth + 1
                    while (dep != original_depth + 1):
                        del depth_dict[dep]
                        del d_dict[dep]
                        dep += 1
                    position = d_dict[depth]
                except KeyError:
                    pass
                position = d_dict[depth]

                position[playerfirst].append(i)
                for j in conversion[i[0], i[1]]:
                    position[playerfirst].append(j)
                    if playerfirst == "X":
                        position["O"].remove(j)
                    else:
                        position["X"].remove(j)

                if flag == 0:
                    flag = 1
                    next_move = copy.deepcopy(position)

                depth_dict[depth + 1] = position
                d_dict = copy.deepcopy(depth_dict)

                if playerfirst == "X":
                    v = traverse("O", depth + 1, depth_dict, d_dict, alpha_beta_dict, a_b_dict, parent, par, val_dict, v_dict)

                    if depth % 2 == 1:

                        v_dict = copy.deepcopy(val_dict)
                        if v < val_dict[depth]:
                            v_dict[depth] = v
                            val_dict[depth] = v_dict[depth]
                            v_dict = copy.deepcopy(val_dict)

                        if v < alpha_beta_dict[depth][1] and v > alpha_beta_dict[depth][0]:
                            a_b_dict[depth][1] = v
                            alpha_beta_dict[depth][1] = a_b_dict[depth][1]
                            a_b_dict = copy.deepcopy(alpha_beta_dict)

                        if parent[depth] == [-1, -1]:
                            #print "root"+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict)
                            output_lines.append("root"+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict))
                            for vv in xrange(1, len(vv_d)):
                                val_dict[vv] = copy.deepcopy(vv_d[vv])
                                v_dict[vv] = copy.deepcopy(vv_d[vv])

                        elif parent[depth] == [9, 9]:
                            #print "pass"+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict)
                            output_lines.append("pass"+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict))
                        else:
                            #print row_value[parent[depth][1]] + col_value[parent[depth][0]]+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict)
                            output_lines.append(row_value[parent[depth][1]] + col_value[parent[depth][0]]+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict))

                        if val_dict[depth] <= alpha_beta_dict[depth][0]:
                            temp = copy.deepcopy(val_dict[depth])
                            if depth % 2 == 1:
                                v_dict[depth] = 10000
                            else:
                                v_dict[depth] = -10000
                            val_dict[depth] = v_dict[depth]
                            v_dict = copy.deepcopy(val_dict)
                            # print "eqe"
                            return temp

                    else:
                        v_dict = copy.deepcopy(val_dict)
                        if v > val_dict[depth]:
                            v_dict[depth] = v
                            val_dict[depth] = v_dict[depth]
                            v_dict = copy.deepcopy(val_dict)
                        if v < alpha_beta_dict[depth][1] and v > alpha_beta_dict[depth][0]:
                            a_b_dict[depth][0] = v
                            alpha_beta_dict[depth][0] = a_b_dict[depth][0]
                            a_b_dict = copy.deepcopy(alpha_beta_dict)

                        if parent[depth] == [-1, -1]:
                            #print "root"+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict)
                            output_lines.append("root"+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict))
                            for vv in xrange(1, len(vv_d)):
                                val_dict[vv] = copy.deepcopy(vv_d[vv])
                                v_dict[vv] = copy.deepcopy(vv_d[vv])

                        elif parent[depth] == [9, 9]:
                            #print "pass"+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict)
                            output_lines.append("pass"+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict))
                        else:
                            #print row_value[parent[depth][1]] + col_value[parent[depth][0]]+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict)
                            output_lines.append(row_value[parent[depth][1]] + col_value[parent[depth][0]]+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict))

                        if val_dict[depth] >= alpha_beta_dict[depth][1]:

                            temp = copy.deepcopy(val_dict[depth])
                            if depth % 2 == 1:
                                v_dict[depth] = 10000
                            else:
                                v_dict[depth] = -10000
                            val_dict[depth] = v_dict[depth]
                            v_dict = copy.deepcopy(val_dict)
                            return temp


                else:
                    v = traverse("X", depth + 1, depth_dict, d_dict, alpha_beta_dict, a_b_dict, parent, par, val_dict, v_dict)

                    if depth % 2 == 1:
                        v_dict = copy.deepcopy(val_dict)
                        if v <= val_dict[depth]:
                            v_dict[depth] = v
                            val_dict[depth] = v_dict[depth]
                            v_dict = copy.deepcopy(val_dict)

                        if v < alpha_beta_dict[depth][1] and v > alpha_beta_dict[depth][0]:

                            a_b_dict[depth][1] = v
                            alpha_beta_dict[depth][1] = a_b_dict[depth][1]
                            a_b_dict = copy.deepcopy(alpha_beta_dict)

                        if parent[depth] == [-1, -1]:
                            #print "root"+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict)
                            output_lines.append("root"+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict))
                            for vv in xrange(1, len(vv_d)):
                                val_dict[vv] = copy.deepcopy(vv_d[vv])
                                v_dict[vv] = copy.deepcopy(vv_d[vv])

                        elif parent[depth] == [9, 9]:
                            #print "pass"+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict)
                            output_lines.append("pass"+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict))
                        else:
                            #print row_value[parent[depth][1]] + col_value[parent[depth][0]]+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict)
                            output_lines.append(row_value[parent[depth][1]] + col_value[parent[depth][0]]+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict))

                        if val_dict[depth] <= alpha_beta_dict[depth][0]:
                            temp = copy.deepcopy(val_dict[depth])
                            if depth % 2 == 1:
                                v_dict[depth] = 10000
                            else:
                                v_dict[depth] = -10000
                            val_dict[depth] = v_dict[depth]
                            v_dict = copy.deepcopy(val_dict)
                            return temp

                    else:
                        v_dict = copy.deepcopy(val_dict)
                        if v > val_dict[depth]:
                            v_dict[depth] = v
                            val_dict[depth] = v_dict[depth]
                            v_dict = copy.deepcopy(val_dict)

                        if v < alpha_beta_dict[depth][1] and v > alpha_beta_dict[depth][0]:
                            a_b_dict[depth][0] = v
                            alpha_beta_dict[depth][0] = a_b_dict[depth][0]
                            a_b_dict = copy.deepcopy(alpha_beta_dict)

                        if parent[depth] == [-1, -1]:
                            #print "root"+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict)
                            output_lines.append("root"+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict))
                            for vv in xrange(1, len(vv_d)):
                                val_dict[vv] = copy.deepcopy(vv_d[vv])
                                v_dict[vv] = copy.deepcopy(vv_d[vv])

                        elif parent[depth] == [9, 9]:
                            #print "pass"+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict)
                            output_lines.append("pass"+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict))
                        else:
                            #print row_value[parent[depth][1]] + col_value[parent[depth][0]]+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict)
                            output_lines.append(row_value[parent[depth][1]] + col_value[parent[depth][0]]+ "," + str(depth)+ "," + convertvalues(depth, val_dict[depth], alpha_beta_dict))

                        if val_dict[depth] >= alpha_beta_dict[depth][1]:
                            temp = copy.deepcopy(val_dict[depth])
                            if depth % 2 == 1:
                                v_dict[depth] = 10000
                            else:
                                v_dict[depth] = -10000
                            val_dict[depth] = v_dict[depth]
                            v_dict = copy.deepcopy(val_dict)
                            return temp

        temp = copy.deepcopy(val_dict[depth])

        if depth % 2 == 1:
            v_dict[depth] = 10000
        else:
            v_dict[depth] = -10000
        val_dict[depth] = v_dict[depth]
        v_dict = copy.deepcopy(val_dict)

        return temp

        pass


original_depth = 0

with open("./Input/input.txt") as fin:
    player = ""
    original_depth = -1
    board = []
    position = {}
    row = 0
    col = 0
    j = []
    for line in fin:
        if player == "":
            player = line
            player = player.strip()

        elif original_depth == -1:
            original_depth = int(line)

        else:
            col = 0
            j = []
            for i in line:
                if i == "\n":
                    continue
                if i == "O":
                    if i in position:
                        position["O"].append([row, col])
                    else:
                        position["O"] = [[row, col]]

                elif i == "X":
                    if i in position:
                        position["X"].append([row, col])
                    else:
                        position["X"] = [[row, col]]

                j.append(i)
                col += 1

            board.append(j)
            row += 1

depth_dict = {}
parent = {}
parent[0] = [-1, -1]
par = copy.deepcopy(parent)
depth = 0

val_dict = {}
for i in xrange(original_depth):
    if i % 2 == 0:
        val_dict[i] = -10000
    else:
        val_dict[i] = 10000

v_d = copy.deepcopy(val_dict)
vv_d = copy.deepcopy(val_dict)

alpha_beta_dict = []
for i in xrange(original_depth + 1):
    alpha_beta_dict.append([-10000, 10000])
a_b_dict = copy.deepcopy(alpha_beta_dict)
if "O" not in position:
    position["O"] = []
elif "X" not in position:
    position["X"] = []
init_player = copy.deepcopy(player)
next_move = copy.deepcopy(position)
depth_dict[depth] = position
output_lines = []
dd_1 = copy.deepcopy(depth_dict)
if "O" in position and "X" in position:
    v = traverse(player, depth, depth_dict, dd_1, alpha_beta_dict, a_b_dict, parent, par, val_dict, v_d)


n_m = ""
for i in xrange(8):
    for j in xrange(8):
        try:
            if [i,j] in next_move["X"]:
                n_m += "X"
            elif [i,j] in next_move["O"]:
                n_m += "O"
            else:
                n_m += "*"
        except:
            n_m += "*"
            continue
    #print n_m
    n_m = ""

with open("./output.txt","wb") as fop:
    n_m = ""
    for i in xrange(8):
        for j in xrange(8):
            try:
                if [i, j] in next_move["X"]:
                    n_m += "X"
                elif [i, j] in next_move["O"]:
                    n_m += "O"
                else:
                    n_m += "*"
            except:
                n_m += "*"
                continue
        fop.write(n_m + "\n")
        n_m = ""
    fop.write("Node,Depth,Value,Alpha,Beta" + "\n")
    for i in output_lines:
        fop.write(i + "\n")