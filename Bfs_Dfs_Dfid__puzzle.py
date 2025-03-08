from sys import setrecursionlimit
setrecursionlimit(100000)

class Node:
    def __init__(self, state, parent=None):
        # Store the node state and parent state
        self.state = [row[:] for row in state]  
        self.parent = parent  # tracing
    
    def __str__(self):
        # Print the state of the node in a readable format
        return '\n'.join([' '.join(row) for row in self.state])

class PuzzleSolver:
    def __init__(self, start, goal=None):
        # Initialize the puzzle with start and goal states
        self.start = start
        self.goal = goal if goal else Node([['1', '2', '3'], ['4', '5', '6'], ['7', '8', ' ']])
    
    def is_solvable(self, state):
        # Check if the puzzle state is solvable by counting inversions
        flat = [tile for row in state.state for tile in row if tile != ' ']
        inversions = 0
        for i in range(len(flat)):
            for j in range(i + 1, len(flat)):
                if flat[i] > flat[j]:
                    inversions += 1
        return inversions % 2 == 0

    def find_space(self, state):
        # Find the position (x, y) of the empty space (' ')
        for i in range(3):
            for j in range(3):
                if state.state[i][j] == ' ':
                    return (i, j)
        return None

    def find_moves(self, pos):
        # Generate valid moves for the empty space
        x, y = pos
        return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

    def is_valid(self, move):
        # Check if a move is within bounds of the 3x3 puzzle
        x, y = move
        return 0 <= x < 3 and 0 <= y < 3

    def play_move(self, state, move, space):
        # Generate a new state after making the move
        x, y = space  
        new_x, new_y = move  
        new_state = [row[:] for row in state.state] 
        new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
        return Node(new_state, state)

    def generate_children(self, state):
        # Generate all valid children from a state
        children = []
        space = self.find_space(state)
        moves = self.find_moves(space)
        for move in moves:
            if self.is_valid(move):
                child = self.play_move(state, move, space)
                children.append(child)
        return children

    def state_to_string(self, state):
        # Helper to convert state to string for comparison
        return ''.join([''.join(row) for row in state.state])

    def solve_puzzle_backtracking(self):
        # Simple backtracking to find a solution
        def backtrack(node):
            state_list = [self.state_to_string(self.start)]  # Track visited states
            def recursive_backtrack(current):
                if self.state_to_string(current) == self.state_to_string(self.goal):
                    return current
                for child in self.generate_children(current):
                    child_str = self.state_to_string(child)
                    if child_str not in state_list:
                        state_list.append(child_str)
                        result = recursive_backtrack(child)
                        if result:
                            return result
                return None
            return recursive_backtrack(node)

        final_state = backtrack(self.start)
        if final_state:
            print("Backtracking Solution Found:")
            self.disp_solution(final_state)
        else:
            print("No solution found with backtracking.")

    def solve_puzzle_dfs(self):
        # Depth-first search to solve the puzzle
        open_list = [self.start]
        closed_list = set()
        
        while open_list:
            current = open_list.pop() 
            current_str = self.state_to_string(current)
            
            if current_str == self.state_to_string(self.goal):
                print("DFS Solution Found:")
                self.disp_solution(current)
                return
            
            if current_str not in closed_list:
                closed_list.add(current_str)
                children = self.generate_children(current)
                open_list.extend(children) 
        print("No solution found with DFS.")

    def solve_puzzle_bfs(self):
        # Breadth-first search to solve the puzzle
        open_list = [self.start]
        closed_list = set()
        
        while open_list:
            current = open_list.pop(0) 
            current_str = self.state_to_string(current)
            
            if current_str == self.state_to_string(self.goal):
                print("BFS Solution Found:")
                self.disp_solution(current)
                return
            
            if current_str not in closed_list:
                closed_list.add(current_str)
                children = self.generate_children(current)
                open_list.extend(children) 
        print("No solution found with BFS.")

    def solve_puzzle_dfid(self):
        def dls(node, depth, visited):
            if depth < 0:
                return None
            current_str = self.state_to_string(node)
            if current_str == self.state_to_string(self.goal):
                return node
            if current_str in visited:
                return None
            visited.add(current_str)
            for child in self.generate_children(node):
                result = dls(child, depth - 1, visited.copy())
                if result:
                    return result
            return None

        depth = 0
        while True:
            visited = set()
            result = dls(self.start, depth, visited)
            if result:
                print("DFID Solution Found:")
                self.disp_solution(result)
                return
            depth += 1
            if depth > 50: 
                print("No solution found with DFID within depth limit.")
                return

    def disp_solution(self, final_state):
        # Display the solution path from start to goal
        if not final_state:
            print("No path to display.")
            return
        path = []
        current = final_state
        while current:
            path.append(current)
            current = current.parent
        path.reverse()
        for i, node in enumerate(path):
            print(f"Step {i}:\n{node}\n")


def main():
    start = Node([['4', '7', '8'], ['3', '6', '5'], ['1', '2', ' ']])
    solver = PuzzleSolver(start=start)
    print("Starting State:")
    print(start)
    print("\nGoal State:")
    print(solver.goal)
    print("\nSolving with different methods:\n")
    #solver.solve_puzzle_backtracking()
    #solver.solve_puzzle_dfs()
    #solver.solve_puzzle_bfs()
    solver.solve_puzzle_dfid()
    print('end')


main()