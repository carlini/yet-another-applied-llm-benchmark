from evaluator import *

DESCRIPTION = "Test if the model can rewrite a given Python program into an equivalent C program."

TAGS = ['code', 'c']

question = """
Here's a python program. Please rewrite it in c with the type signature float solve_dp(float* arr, int size, int lines_left)

def solve_dp(graph, lines_left):
    n = len(graph)

    dp = [[[1e9 for _ in range(10)] for _ in range(lines_left + 1)] for _ in range(n + 1)]
    # Initialize how as -1 indicating no decision made
    how = [[[-1 for _ in range(10)] for _ in range(lines_left + 1)] for _ in range(n + 1)]

    for i in range(n, -1, -1):
        for j in range(lines_left + 1):
            for k in range(10):
                if i == n and j == 0:
                    dp[i][j][k] = 0
                else:
                    # Option 1: don't take the line
                    if i < n and k < 9:
                        if dp[i + 1][j][k + 1] < dp[i][j][k]:
                            dp[i][j][k] = dp[i + 1][j][k + 1]
                            how[i][j][k] = k + 1  # Representing choosing not to take the line

                    # Option 2: take the line
                    if i < n and j > 0:
                        cost = graph[i] + (k - 8)**2
                        if cost + dp[i + 1][j - 1][0] < dp[i][j][k]:
                            dp[i][j][k] = cost + dp[i + 1][j - 1][0]
                            how[i][j][k] = 0  # Representing choosing to take the line

    # Reconstruct the solution

    i, j, k = 0, lines_left, 6
    taken_lines = []
    while i < n:
        if how[i][j][k] == 0:  # Chose to take the line
            taken_lines.append(n - i)
            i += 1
            j -= 1
            k = 0
        else:  # Chose not to take the line
            i += 1
            k += 1

    return dp[0][lines_left][6]
"""

test_case, answer = make_c_test([("solve_dp(arr, 100, 100)", "11290")], header="float arr[] = {71, 89, 34, 63, 19, 94, 54, 61, 88, 20, 66, 46, 26, 87, 55, 81, 6, 2, 72, 75, 98, 78, 24, 95, 73, 7, 56, 48, 14, 99, 64, 51, 69, 77, 28, 47, 8, 22, 49, 3, 62, 32, 10, 82, 35, 18, 85, 60, 83, 23, 5, 40, 41, 68, 53, 52, 44, 45, 65, 84, 93, 25, 13, 1, 31, 11, 12, 97, 38, 0, 43, 90, 36, 70, 33, 17, 21, 30, 16, 15, 74, 67, 58, 37, 39, 96, 79, 29, 27, 92, 86, 9, 80, 42, 57, 91, 59, 4, 76, 50};")


TestProgramRewriteC = question >> LLMRun() >> ExtractCode() >> CRun(test_case) >> SubstringEvaluator(answer)

if __name__ == "__main__":
    print(run_test(TestProgramRewriteC))
