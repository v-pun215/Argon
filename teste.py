from collections import deque
problem_input = []
mn = list(map(int, input().split()))
for i in range(sum(mn)):
    problem_input.append(int(input()))

before_king = deque()
for index, i in enumerate(problem_input):
    if i!=-1:
        before_king.appendleft(i)
    else:
        print(max(before_king))
        before_king.popleft(before_king.index(max(before_king)))