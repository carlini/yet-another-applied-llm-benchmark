from evaluator import *

DESCRIPTION = "Test if the model can correctly call a python API for a moderately popular python library."

TAGS = ['code', 'python']

question = """
In python-chess I have a game = chess.pgn.read_game(pgn).

How do I print the PGN notation for all prefixes of this game?

Call your function print_all_prefixes(game). Do not give example code for how to run it.

"""

test_case = """import io
import chess.pgn
print_all_prefixes(chess.pgn.read_game(io.StringIO('1. Nf3 Nf6 2. c4 g6 3. Nc3 Bg7 4. d4 O-O 5. Bf4 d5 6. Qb3 dxc4 7. Qxc4 c6 8. e4 Nbd7 9. Rd1 Nb6 10. Qc5 Bg4 11. Bg5 Na4 12. Qa3 Nxc3 13. bxc3 Nxe4 14. Bxe7 Qb6 15. Bc4 Nxc3')))"""

def check(txt):
    return txt.count('1. Nf3 Nf6 2. c4 g6 3. Nc3 Bg7') > 10, ""
    
    

TestPyChessPrefix = question >> LLMRun() >> ExtractCode() >> PythonRun(test_case) >> PyFunc(check)

if __name__ == "__main__":
    print(run_test(TestPyChessPrefix))
