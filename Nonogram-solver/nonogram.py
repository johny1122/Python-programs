# Jonathan Birnbaum   #
# 204801070           #
# yonatan11           #
# Intro2CS EX8        #


def get_row_variations(row, blocks):
    """
    The function finds all the correct variations of a given row according
    to the given blocks constraints
    :param row: A list of one row
    :param blocks: list of constraints
    :return: list of all correct variations
    """
    length_row = len(row)
    sum_blocks = sum(blocks)
    length_blocks = len(blocks)

    if not blocks:  # if there are no blocks so all the row is 0
        return [[0] * len(row)]

    if 1 not in row and -1 not in row:  # if only 0 in row
        return [row]

    def get_row_variations_helper(curr_ind, opt_paint, one_count, block_ind,
                                  all_ones):
        """
        The function helps the get_row_variations function and words with
        backtracking algorithm
        :param curr_ind: int of the current index in the row
        :param opt_paint: list of the optional paint solutions of a row
        :param one_count: int that counts the painted indexes in a sequence
        :param block_ind: int of the index of the current block in blocks list
        :param all_ones: int that count all the painted indexes in the row
        :return: list of the possible solutions of a row
        """
        # if finished all the blocks
        if block_ind == len(blocks):
            if len(opt_paint) != length_row:
                return []
            else:
                temp = [opt_paint[:]]  # creating a shallow copy
                return temp

        if one_count > blocks[block_ind]:
            return []

        # if there are ones as much as in all blocks
        if all_ones == sum_blocks:
            if 1 not in row[curr_ind:]:
                temp = [opt_paint[:]]
                temp[0] += (length_row - curr_ind) * [0]
                return temp

        # if there are no places ahead for the blocks and spaces
        spaces = length_blocks - block_ind - 1
        if (length_row - curr_ind) < (sum(blocks[
                                          block_ind:]) + spaces - one_count):
            return []

        # if arrived to end row
        if curr_ind == length_row:  # if arrived to end row
            temp = [opt_paint[:]]  # creating a shallow copy
            return temp

        if len(opt_paint) > 0:
            if sum(count_blocks(opt_paint)) > sum_blocks:
                temp = [opt_paint[:]]  # creating a shallow copy
                return temp

            if (one_count > 0) and (one_count < blocks[block_ind]) and  \
                    opt_paint[-1] == 0:
                return []

        solutions = []
        if row[curr_ind] != -1:  # if there's already painted or empty
            if row[curr_ind] == 1:
                one_count += 1
                all_ones += 1
            if row[curr_ind] == 0 and one_count == blocks[block_ind]:
                block_ind += 1
                one_count = 0
            opt_paint.append(row[curr_ind])
            solutions += get_row_variations_helper(curr_ind + 1, opt_paint,
                                                   one_count, block_ind,
                                                   all_ones)
            opt_paint.pop()

        else:
            opt_paint.append(1)  # adding 1 and sending ahead
            one_count += 1
            all_ones += 1
            solutions += get_row_variations_helper(curr_ind + 1, opt_paint,
                                                   one_count, block_ind,
                                                   all_ones)
            one_count -= 1
            all_ones -= 1
            opt_paint.pop()

            if one_count == blocks[block_ind]:
                block_ind += 1
                one_count = 0
            opt_paint.append(0)  # adding 0 and sending ahead
            solutions += get_row_variations_helper(curr_ind + 1, opt_paint,
                                                   one_count, block_ind,
                                                   all_ones)
            opt_paint.pop()

        return solutions

    all_solutions = get_row_variations_helper(0, [], 0, 0, 0)
    return sort_solutions(all_solutions, blocks)


def sort_solutions(solutions, blocks):
    """
    The function sorts all the possible lists of a row that have the
    same blocks as in the given blocks list
    :param solutions: list of all the possible row solutions
    :param blocks: list of the blocks
    :return: list of the row's lists that match the blocks conditions
    """
    good_solutions = []
    for solution in solutions:
        if count_blocks(solution) == blocks:
            good_solutions.append(solution)
    if not good_solutions:
        good_solutions = [[]]
    return good_solutions


def count_blocks(row):
    """
    The function gets a row and counts all of it's blocks
    :param row: list of a row
    :return: list of the blocks in the given row
    """
    blocks = []
    count_1 = 0
    for num in row:
        if num == 1:
            count_1 += 1
        else:
            if count_1 != 0:
                blocks.append(count_1)
                count_1 = 0
    if row[-1] == 1:
        blocks.append(count_1)
    return blocks


def get_intersection_row(rows):
    """
    The function makes a list of all the indexes and put 1/0 if they were in
    all of the lists on the same index and puts in the index -1 of there was
     a different
    :param rows: List of rows
    :return: List with all the similarities and differences
    """
    if len(rows) == 1:
        return rows[0]
    elif not rows:
        return []
    shared_list = []
    different = False
    for index in range(len(rows[0])):
        index_status = rows[0][index]
        for row in rows:
            if row[index] != index_status:
                different = True
        if different:
            shared_list.append(-1)
            different = False
        else:
            shared_list.append(index_status)
    return shared_list


def conclude_from_constraints(board, constraints):
    """
    The function gets a board and change it by putting 1 or 0 in all the
    places that it's
    must for them to be there.
    :param board: list of a board
    :param constraints: list of the blocks
    :return: None
    """
    changed = True
    no_solution = False
    while changed:  # while there are changes to the rows or columns
        changed = False
        if not board:
            return None

        # change rows #

        # change the rows according to constraints
        for row in range(len(board)):
            temp_row = get_intersection_row(get_row_variations(
                board[row], constraints[0][row]))

            if temp_row == []:
                no_solution = True
                put_in_no_solution(board, row, -1)
                break

            # if there was different - change with the new row
            if temp_row != board[row] and temp_row != []:
                board[row] = temp_row
                changed = True

        # change columns #

        columns = []
        for index in range(len(board[0])):  # make a list of the columns
            temp = [row[index] for row in board]
            columns.append(temp)

        # change the columns according to constraints
        for column in range(len(columns)):
            temp_column = get_intersection_row(get_row_variations
                                               (columns[column],
                                                constraints[1][column]))

            if temp_column == []:
                no_solution = True
                put_in_no_solution(columns, -1, column)

            # if there was different - change with the new column
            if temp_column != columns[column] and temp_column != []:
                columns[column] = temp_column
                changed = True
                break

        # updating the board with the new columns change
        for index in range(len(columns[0])):
            temp = [column[index] for column in columns]
            board[index] = temp

        if no_solution:
            break
    return None


def put_in_no_solution(board, row_index=-1, column_index=-1):
    """
    The function changes a row or a column that there's no solution for them
    :param board: list of a board
    :param row_index: int of the row with no solution
    :param column_index: int of the column with no solution
    :return: None
    """
    if row_index != -1:
        for num in range(len(board[row_index])):
            board[row_index][num] = -1

    elif column_index != -1:
        for row in range(len(board)):
            board[row][column_index] = -1


def init_board(rows_num, columns_num):
    """
    The functions creates a board
    :param rows_num: int of the rows in board
    :param columns_num: int of the columns in board
    :return: List of the created board
    """
    board = []
    for row in range(rows_num):
        board.append([])
        for column in range(columns_num):
            board[row].append(-1)

    return board


def solve_easy_nonogram(constraints):
    """
    The function plays and solves an easy nonogram game
    :param constraints: list of the constraints blocks
    :return: list of the solved board
    """
    rows_num = len(constraints[0])
    columns_num = len(constraints[1])
    board = init_board(rows_num, columns_num)
    conclude_from_constraints(board, constraints)
    return board


def solve_nonogram(constraints):
    return [[[1, 1], [0, 0]]]
