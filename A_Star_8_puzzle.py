import heapq

class PriorityQueue:
    def __init__(self):
        self.heap = []

    def enqueue(self, x):
        heapq.heappush(self.heap, x)

    def dequeue(self):
        return heapq.heappop(self.heap)

    def is_empty(self):
        return len(self.heap) == 0

class Node:
    def __init__(self, state, parent=None):
        self.state = tuple(tuple(row) for row in state)  
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0  

    def __lt__(self, other):
        return self.f < other.f

    def heuristic(self, goal):
        distance = 0
        goal = tuple(tuple(row) for row in goal)
        for r in range(3):
            for c in range(3):
                val = self.state[r][c]
                if val != 0:
                    goal_row, goal_col = divmod(val - 1, 3)
                    distance += abs(r - goal_row) + abs(c - goal_col)
        return distance

    def out_place (self , goal):
        distance = 0
        goal = tuple(tuple(row) for row in goal)
        for r in range(3):
            for c in range(3):
                val = self.state[r][c]
                if val != 0:
                    goal_row, goal_col = divmod(val - 1, 3)
                    if r != goal_row or c != goal_col:
                        distance += 1
        return distance
    def to_list(self):
        return [list(row) for row in self.state]

class PuzzleSolver:
    def __init__(self, start):
        self.start = [row[:] for row in start] 
        self.goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        
    def is_solvable(self):
        
        flat = [x for row in self.start for x in row if x != 0]
        inversions = 0
        for i in range(len(flat)):
            for j in range(i + 1, len(flat)):
                if flat[i] > flat[j]:
                    inversions += 1
        return inversions % 2 == 0  

    def find_space(self, state):
        for r in range(3):
            for c in range(3):
                if state[r][c] == 0:
                    return (r, c)
        return None

    def find_moves(self, pos):
        (r, c) = pos
        return [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]

    def is_valid(self, move):
        (r, c) = move
        return 0 <= r < 3 and 0 <= c < 3

    def play_move(self, state, move, space):
        (r, c) = space
        (new_r, new_c) = move
        new_state = [row[:] for row in state]
        new_state[r][c], new_state[new_r][new_c] = new_state[new_r][new_c], new_state[r][c]
        return new_state

    def find_children(self, state):
        children = []
        space = self.find_space(state)
        for move in self.find_moves(space):
            if self.is_valid(move):
                child_state = self.play_move(state, move, space)
                children.append(child_state)
        return children

    def solve_puzzle(self):
        if not self.is_solvable():
            return None, "Puzzle is not solvable"

        pq = PriorityQueue()
        start_node = Node(self.start)
        start_node.h = start_node.out_place(self.goal)
        start_node.f = start_node.g + start_node.h
        pq.enqueue(start_node)

        explored = set()  

        while not pq.is_empty():
            current_node = pq.dequeue()
            if current_node.state == tuple(tuple(row) for row in self.goal):
                return self.reconstruct_path(current_node), f"Solution found in {current_node.g} moves"

            state_str = current_node.state  
            if state_str in explored:
                continue
            explored.add(state_str)

            for child_state in self.find_children(current_node.to_list()):
                child_tuple = tuple(tuple(row) for row in child_state)
                if child_tuple not in explored:
                    child_node = Node(child_state, current_node)
                    child_node.g = current_node.g + 1
                    child_node.h = child_node.heuristic(self.goal)
                    child_node.f = child_node.g + child_node.h
                    pq.enqueue(child_node)

        return None, "No solution found"

    def reconstruct_path(self, node):
        path = []
        while node is not None:
            path.append(node.to_list())
            node = node.parent
        path.reverse()
        return path


def main():
    # Test case 1: Solvable puzzle
    start1 = [[4, 7, 8], [3, 6, 5], [1, 2, 0]]
    ps1 = PuzzleSolver(start1)
    solution1, message1 = ps1.solve_puzzle()
    print("Test 1:")
    print(message1)
    if solution1:
        for i, state in enumerate(solution1):
            print(f"Step {i}: {state}")
    print()

    # Test case 2: Unsolvable puzzle
    start2 = [[8, 1, 2], [0, 4, 3], [7, 6, 5]]  
    ps2 = PuzzleSolver(start2)
    solution2, message2 = ps2.solve_puzzle()
    print("Test 2:")
    print(message2)
    if solution2:
        for i, state in enumerate(solution2):
            print(f"Step {i}: {state}")

main()