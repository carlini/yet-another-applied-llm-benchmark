from evaluator import *

DESCRIPTION = "Test if a model can decompile a long (300 line) python bytecode function back to python."

TAGS = ['code', 'python']

question = """
Disassemble the following python into a function called foo:


  2           0 LOAD_CONST               1 (16)
              2 STORE_FAST               2 (PH)

  4           4 LOAD_CONST               2 (0)
              6 STORE_FAST               3 (extra)

  5           8 LOAD_CONST               2 (0)
             10 STORE_FAST               4 (col)

  6          12 BUILD_LIST               0
             14 STORE_FAST               5 (pivots)

  8          16 LOAD_CONST               3 (<code object <listcomp> at 0x101093660, file "/private/tmp/a.py", line 8>)
             18 LOAD_CONST               4 ('rref.<locals>.<listcomp>')
             20 MAKE_FUNCTION            0
             22 LOAD_GLOBAL              0 (range)
             24 LOAD_FAST                0 (matrix)
             26 LOAD_ATTR                1 (shape)
             28 LOAD_CONST               2 (0)
             30 BINARY_SUBSCR
             32 CALL_FUNCTION            1
             34 GET_ITER
             36 CALL_FUNCTION            1
             38 STORE_FAST               6 (used_for_row)

 10          40 LOAD_FAST                0 (matrix)
             42 LOAD_FAST                2 (PH)
             44 BINARY_MODULO
             46 STORE_FAST               0 (matrix)

 11     >>   48 LOAD_FAST                4 (col)
             50 LOAD_FAST                3 (extra)
             52 BINARY_ADD
             54 LOAD_FAST                0 (matrix)
             56 LOAD_ATTR                1 (shape)
             58 LOAD_CONST               5 (1)
             60 BINARY_SUBSCR
             62 LOAD_CONST               5 (1)
             64 BINARY_SUBTRACT
             66 COMPARE_OP               0 (<)
             68 EXTENDED_ARG             2
             70 POP_JUMP_IF_FALSE      628
             72 LOAD_FAST                4 (col)
             74 LOAD_FAST                0 (matrix)
             76 LOAD_ATTR                1 (shape)
             78 LOAD_CONST               2 (0)
             80 BINARY_SUBSCR
             82 COMPARE_OP               0 (<)
             84 EXTENDED_ARG             2
             86 POP_JUMP_IF_FALSE      628

 13          88 LOAD_FAST                0 (matrix)
             90 LOAD_FAST                4 (col)
             92 LOAD_FAST                4 (col)
             94 LOAD_FAST                3 (extra)
             96 BINARY_ADD
             98 BUILD_TUPLE              2
            100 BINARY_SUBSCR
            102 LOAD_CONST               2 (0)
            104 COMPARE_OP               2 (==)
            106 EXTENDED_ARG             1
            108 POP_JUMP_IF_FALSE      262

 14         110 LOAD_GLOBAL              2 (np)
            112 LOAD_METHOD              3 (all)
            114 LOAD_FAST                0 (matrix)
            116 LOAD_CONST               0 (None)
            118 LOAD_CONST               0 (None)
            120 BUILD_SLICE              2
            122 LOAD_FAST                4 (col)
            124 BUILD_TUPLE              2
            126 BINARY_SUBSCR
            128 LOAD_CONST               2 (0)
            130 COMPARE_OP               2 (==)
            132 CALL_METHOD              1
            134 POP_JUMP_IF_FALSE      146

 15         136 LOAD_FAST                3 (extra)
            138 LOAD_CONST               5 (1)
            140 INPLACE_ADD
            142 STORE_FAST               3 (extra)

 16         144 JUMP_ABSOLUTE           48

 17     >>  146 LOAD_GLOBAL              2 (np)
            148 LOAD_METHOD              4 (argwhere)
            150 LOAD_FAST                0 (matrix)
            152 LOAD_CONST               0 (None)
            154 LOAD_CONST               0 (None)
            156 BUILD_SLICE              2
            158 LOAD_FAST                4 (col)
            160 LOAD_FAST                3 (extra)
            162 BINARY_ADD
            164 BUILD_TUPLE              2
            166 BINARY_SUBSCR
            168 LOAD_CONST               2 (0)
            170 COMPARE_OP               3 (!=)
            172 CALL_METHOD              1
            174 LOAD_METHOD              5 (flatten)
            176 CALL_METHOD              0
            178 LOAD_CONST               6 (-1)
            180 BINARY_SUBSCR
            182 STORE_FAST               7 (other)

 18         184 LOAD_FAST                7 (other)
            186 LOAD_FAST                4 (col)
            188 COMPARE_OP               0 (<)
            190 POP_JUMP_IF_FALSE      202

 19         192 LOAD_FAST                3 (extra)
            194 LOAD_CONST               5 (1)
            196 INPLACE_ADD
            198 STORE_FAST               3 (extra)

 20         200 JUMP_ABSOLUTE           48

 22     >>  202 LOAD_GLOBAL              6 (list)
            204 LOAD_FAST                0 (matrix)
            206 LOAD_FAST                7 (other)
            208 BINARY_SUBSCR
            210 CALL_FUNCTION            1
            212 LOAD_GLOBAL              6 (list)
            214 LOAD_FAST                0 (matrix)
            216 LOAD_FAST                4 (col)
            218 BINARY_SUBSCR
            220 CALL_FUNCTION            1
            222 ROT_TWO
            224 LOAD_FAST                0 (matrix)
            226 LOAD_FAST                4 (col)
            228 STORE_SUBSCR
            230 LOAD_FAST                0 (matrix)
            232 LOAD_FAST                7 (other)
            234 STORE_SUBSCR

 23         236 LOAD_FAST                6 (used_for_row)
            238 LOAD_FAST                7 (other)
            240 BINARY_SUBSCR
            242 LOAD_FAST                6 (used_for_row)
            244 LOAD_FAST                4 (col)
            246 BINARY_SUBSCR
            248 ROT_TWO
            250 LOAD_FAST                6 (used_for_row)
            252 LOAD_FAST                4 (col)
            254 STORE_SUBSCR
            256 LOAD_FAST                6 (used_for_row)
            258 LOAD_FAST                7 (other)
            260 STORE_SUBSCR

 25     >>  262 LOAD_FAST                5 (pivots)
            264 LOAD_METHOD              7 (append)
            266 LOAD_FAST                4 (col)
            268 LOAD_FAST                3 (extra)
            270 BINARY_ADD
            272 CALL_METHOD              1
            274 POP_TOP

 26         276 LOAD_FAST                0 (matrix)
            278 LOAD_FAST                4 (col)
            280 LOAD_FAST                4 (col)
            282 LOAD_FAST                3 (extra)
            284 BINARY_ADD
            286 BUILD_TUPLE              2
            288 BINARY_SUBSCR
            290 STORE_FAST               8 (pivot)

 27         292 LOAD_FAST                4 (col)
            294 LOAD_FAST                3 (extra)
            296 BINARY_ADD
            298 LOAD_FAST                1 (graphlen)
            300 COMPARE_OP               0 (<)
            302 EXTENDED_ARG             1
            304 POP_JUMP_IF_FALSE      348

 28         306 LOAD_GLOBAL              2 (np)
            308 LOAD_METHOD              8 (abs)
            310 LOAD_FAST                8 (pivot)
            312 CALL_METHOD              1
            314 LOAD_CONST               5 (1)
            316 COMPARE_OP               2 (==)
            318 EXTENDED_ARG             1
            320 POP_JUMP_IF_TRUE       396
            322 LOAD_GLOBAL              2 (np)
            324 LOAD_METHOD              8 (abs)
            326 LOAD_FAST                8 (pivot)
            328 CALL_METHOD              1
            330 LOAD_FAST                2 (PH)
            332 LOAD_CONST               5 (1)
            334 BINARY_SUBTRACT
            336 COMPARE_OP               2 (==)
            338 EXTENDED_ARG             1
            340 POP_JUMP_IF_TRUE       396
            342 LOAD_ASSERTION_ERROR
            344 RAISE_VARARGS            1
            346 JUMP_FORWARD            48 (to 396)

 30     >>  348 LOAD_GLOBAL              2 (np)
            350 LOAD_METHOD              8 (abs)
            352 LOAD_FAST                8 (pivot)
            354 CALL_METHOD              1
            356 LOAD_CONST               7 (2)
            358 COMPARE_OP               2 (==)
            360 EXTENDED_ARG             1
            362 POP_JUMP_IF_TRUE       388
            364 LOAD_GLOBAL              2 (np)
            366 LOAD_METHOD              8 (abs)
            368 LOAD_FAST                8 (pivot)
            370 CALL_METHOD              1
            372 LOAD_FAST                2 (PH)
            374 LOAD_CONST               7 (2)
            376 BINARY_SUBTRACT
            378 COMPARE_OP               2 (==)
            380 EXTENDED_ARG             1
            382 POP_JUMP_IF_TRUE       388
            384 LOAD_ASSERTION_ERROR
            386 RAISE_VARARGS            1

 31     >>  388 LOAD_FAST                8 (pivot)
            390 LOAD_CONST               7 (2)
            392 INPLACE_FLOOR_DIVIDE
            394 STORE_FAST               8 (pivot)

 32     >>  396 LOAD_FAST                0 (matrix)
            398 LOAD_FAST                4 (col)
            400 DUP_TOP_TWO
            402 BINARY_SUBSCR
            404 LOAD_FAST                8 (pivot)
            406 INPLACE_MULTIPLY
            408 ROT_THREE
            410 STORE_SUBSCR

 33         412 LOAD_FAST                0 (matrix)
            414 LOAD_FAST                4 (col)
            416 DUP_TOP_TWO
            418 BINARY_SUBSCR
            420 LOAD_FAST                2 (PH)
            422 INPLACE_MODULO
            424 ROT_THREE
            426 STORE_SUBSCR

 35         428 LOAD_GLOBAL              2 (np)
            430 LOAD_METHOD              4 (argwhere)
            432 LOAD_FAST                0 (matrix)
            434 LOAD_CONST               0 (None)
            436 LOAD_CONST               0 (None)
            438 BUILD_SLICE              2
            440 LOAD_FAST                4 (col)
            442 LOAD_FAST                3 (extra)
            444 BINARY_ADD
            446 BUILD_TUPLE              2
            448 BINARY_SUBSCR
            450 CALL_METHOD              1
            452 LOAD_METHOD              5 (flatten)
            454 CALL_METHOD              0
            456 STORE_FAST               9 (others)

 37         458 LOAD_FAST                9 (others)
            460 GET_ITER
        >>  462 FOR_ITER               154 (to 618)
            464 STORE_FAST              10 (i)

 38         466 LOAD_FAST               10 (i)
            468 LOAD_FAST                4 (col)
            470 COMPARE_OP               2 (==)
            472 EXTENDED_ARG             1
            474 POP_JUMP_IF_FALSE      480
            476 EXTENDED_ARG             1
            478 JUMP_ABSOLUTE          462

 39     >>  480 LOAD_FAST                6 (used_for_row)
            482 LOAD_FAST               10 (i)
            484 DUP_TOP_TWO
            486 BINARY_SUBSCR
            488 LOAD_FAST                6 (used_for_row)
            490 LOAD_FAST                4 (col)
            492 BINARY_SUBSCR
            494 INPLACE_OR
            496 ROT_THREE
            498 STORE_SUBSCR

 40         500 LOAD_FAST                4 (col)
            502 LOAD_FAST                1 (graphlen)
            504 COMPARE_OP               0 (<)
            506 EXTENDED_ARG             2
            508 POP_JUMP_IF_FALSE      548

 41         510 LOAD_FAST                0 (matrix)
            512 LOAD_FAST               10 (i)
            514 DUP_TOP_TWO
            516 BINARY_SUBSCR
            518 LOAD_FAST                0 (matrix)
            520 LOAD_FAST                4 (col)
            522 BINARY_SUBSCR
            524 LOAD_FAST                0 (matrix)
            526 LOAD_FAST               10 (i)
            528 LOAD_FAST                4 (col)
            530 LOAD_FAST                3 (extra)
            532 BINARY_ADD
            534 BUILD_TUPLE              2
            536 BINARY_SUBSCR
            538 BINARY_MULTIPLY
            540 INPLACE_SUBTRACT
            542 ROT_THREE
            544 STORE_SUBSCR
            546 JUMP_FORWARD            50 (to 598)

 43     >>  548 LOAD_FAST                0 (matrix)
            550 LOAD_FAST               10 (i)
            552 LOAD_FAST                4 (col)
            554 LOAD_FAST                3 (extra)
            556 BINARY_ADD
            558 BUILD_TUPLE              2
            560 BINARY_SUBSCR
            562 LOAD_CONST               2 (0)
            564 COMPARE_OP               3 (!=)
            566 EXTENDED_ARG             2
            568 POP_JUMP_IF_FALSE      598

 44         570 LOAD_FAST                0 (matrix)
            572 LOAD_FAST               10 (i)
            574 BINARY_SUBSCR
            576 LOAD_FAST                0 (matrix)
            578 LOAD_FAST                4 (col)
            580 BINARY_SUBSCR
            582 BINARY_SUBTRACT
            584 LOAD_FAST                2 (PH)
            586 BINARY_MODULO
            588 LOAD_FAST                0 (matrix)
            590 LOAD_FAST               10 (i)
            592 STORE_SUBSCR
            594 EXTENDED_ARG             2
            596 JUMP_ABSOLUTE          548

 45     >>  598 LOAD_FAST                0 (matrix)
            600 LOAD_FAST               10 (i)
            602 DUP_TOP_TWO
            604 BINARY_SUBSCR
            606 LOAD_FAST                2 (PH)
            608 INPLACE_MODULO
            610 ROT_THREE
            612 STORE_SUBSCR
            614 EXTENDED_ARG             1
            616 JUMP_ABSOLUTE          462

 47     >>  618 LOAD_FAST                4 (col)
            620 LOAD_CONST               5 (1)
            622 INPLACE_ADD
            624 STORE_FAST               4 (col)
            626 JUMP_ABSOLUTE           48

 49     >>  628 LOAD_GLOBAL              2 (np)
            630 LOAD_METHOD              9 (array)
            632 LOAD_FAST                0 (matrix)
            634 CALL_METHOD              1
            636 LOAD_FAST                2 (PH)
            638 BINARY_MODULO
            640 STORE_FAST               0 (matrix)

 50         642 LOAD_CONST               8 (<code object <listcomp> at 0x101093b30, file "/private/tmp/a.py", line 50>)
            644 LOAD_CONST               4 ('rref.<locals>.<listcomp>')
            646 MAKE_FUNCTION            0
            648 LOAD_FAST                6 (used_for_row)
            650 GET_ITER
            652 CALL_FUNCTION            1
            654 RETURN_VALUE

Disassembly of <code object <listcomp> at 0x101093660, file "/private/tmp/a.py", line 8>:
  8           0 BUILD_LIST               0
              2 LOAD_FAST                0 (.0)
        >>    4 FOR_ITER                14 (to 20)
              6 STORE_FAST               1 (i)
              8 LOAD_GLOBAL              0 (set)
             10 LOAD_FAST                1 (i)
             12 BUILD_LIST               1
             14 CALL_FUNCTION            1
             16 LIST_APPEND              2
             18 JUMP_ABSOLUTE            4
        >>   20 RETURN_VALUE

Disassembly of <code object <listcomp> at 0x101093b30, file "/private/tmp/a.py", line 50>:
 50           0 BUILD_LIST               0
              2 LOAD_FAST                0 (.0)
        >>    4 FOR_ITER                12 (to 18)
              6 STORE_FAST               1 (x)
              8 LOAD_GLOBAL              0 (sorted)
             10 LOAD_FAST                1 (x)
             12 CALL_FUNCTION            1
             14 LIST_APPEND              2
             16 JUMP_ABSOLUTE            4
        >>   18 RETURN_VALUE

"""

test_case, answer = make_python_test([("foo(arr, 37)", "[[0, 38], [0, 38], [0, 6, 28, 35, 38], [0, 6, 18, 21, 28, 35, 38], [0, 6, 28, 35, 38], [0, 6, 21, 28, 35, 38], [0, 5, 10, 23, 38], [0, 5, 10, 23, 38], [0, 5, 10, 23, 38], [0, 5, 9, 10, 23, 38], [0, 5, 9, 10, 13, 17, 23, 30, 38], [0, 5, 9, 10, 11, 23, 27, 38], [0, 5, 9, 10, 11, 23, 27, 38], [0, 5, 9, 10, 11, 23, 25, 27, 38], [0, 1, 5, 7, 8, 9, 10, 11, 12, 15, 16, 19, 23, 25, 26, 27, 34, 38], [0, 1, 5, 7, 8, 9, 10, 11, 12, 15, 16, 19, 23, 25, 26, 27, 34, 38], [0, 1, 5, 7, 8, 9, 10, 11, 12, 15, 16, 19, 23, 25, 26, 27, 34, 38], [0, 1, 5, 7, 8, 9, 10, 11, 12, 15, 16, 19, 23, 25, 26, 27, 34, 38], [0, 1, 5, 7, 8, 9, 10, 11, 12, 15, 16, 19, 23, 25, 26, 27, 34, 38], [0, 1, 5, 7, 8, 9, 10, 11, 12, 15, 16, 19, 23, 25, 26, 27, 34, 38], [0, 1, 5, 7, 8, 9, 10, 11, 12, 15, 16, 19, 23, 24, 25, 26, 27, 34, 38], [0, 1, 5, 7, 8, 9, 10, 11, 12, 15, 16, 19, 23, 25, 26, 27, 34, 38], [0, 1, 5, 7, 8, 9, 10, 11, 12, 15, 16, 19, 23, 25, 26, 27, 34, 38], [0, 1, 5, 7, 8, 9, 10, 11, 12, 15, 16, 19, 23, 25, 26, 27, 34, 38], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 16, 19, 20, 21, 23, 25, 26, 27, 28, 31, 34, 35, 36, 37, 38], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 16, 19, 20, 21, 23, 25, 26, 27, 28, 31, 34, 35, 36, 37, 38], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 16, 19, 20, 21, 23, 25, 26, 27, 28, 31, 34, 35, 36, 37, 38], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 16, 19, 20, 21, 23, 25, 26, 27, 28, 31, 34, 35, 36, 37, 38], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 16, 19, 20, 21, 23, 25, 26, 27, 28, 31, 34, 35, 36, 37, 38], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 16, 19, 20, 21, 23, 25, 26, 27, 28, 31, 34, 35, 36, 37, 38], [0, 5, 9, 10, 13, 17, 23, 30, 38], [0, 5, 9, 10, 13, 17, 23, 30, 38], [0, 5, 9, 10, 13, 17, 23, 30, 32, 38], [0, 5, 9, 10, 13, 17, 23, 30, 32, 33, 38], [0, 22, 29, 38], [0, 22, 29, 38], [0, 6, 28, 35, 38], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 16, 19, 20, 21, 23, 25, 26, 27, 28, 31, 34, 35, 36, 37, 38], [14, 18, 21, 28, 35]]")], header="arr = np.array([[1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -10], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -20], [0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0, -20], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -11], [0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, 0, 0, 0, 0, 0, 0, -30], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, 0, 0, 0, 0, 0, -20], [1, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -11], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -14], [0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -10], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, 0, 0, 0, 0, -30], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -10], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -10], [0, 0, 0, -1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -11], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -13], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -11], [0, 0, 0, 0, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -10], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, -2, 0, 0, 0, -20], [0, 0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -10], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -11], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -13], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -13], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -11], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, 0, 0, -10], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -13], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -11], [0, 0, 1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -9], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, 0, -20], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, -40], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])")


TestDisasRref = question >> LLMRun() >> ExtractCode() >> PythonRun(test_case) >> SubstringEvaluator(answer)


if __name__ == "__main__":
    print(run_test(TestDisasRref))
