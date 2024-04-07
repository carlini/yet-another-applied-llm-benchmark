from evaluator import *

DESCRIPTION = "Test if the model can predict the date a few news headlines were published."

TAGS = ['fun']

question = """
What date was this the front page of HN? Format it YYYY-MM-DD.


1.
We Made One Gram Of Remdesivir (acsh.org)
709 points by tomstokes on [date] | 231 comments
2.
Crafting “Crafting Interpreters” (stuffwithstuff.com)
777 points by _vbdg on [date] | 75 comments
3.
Bose QC 35 Firmware 4.5.2 Noise Cancellation Investigation Report (bose.com)
640 points by robbiet480 on [date] | 323 comments
4.
Csound: A sound and music computing system (csound.com)
226 points by diaphanous on [date] | 92 comments
5.
New Jersey needs COBOL programmers for their unemployment claims system (twitter.com/manicode)
447 points by enraged_camel on [date] | 297 comments
6.
All models are wrong, but some are completely wrong (rssdss.design.blog)
305 points by magoghm on [date] | 208 comments
7.
Configs suck? Try a real programming language (beepb00p.xyz)
289 points by gyre007 on [date] | 345 comments
8.
Ilo sitelen, a handmade computer for Toki Pona (increpare.com)
204 points by tobr on [date] | 90 comments
9.
The Svelte Compiler Handbook (lihautan.com)
330 points by PKop on [date] | 136 comments
10.
Show HN: Export HN Favorites to a CSV File
240 points by gabrielsroka on [date] | 39 comments
"""

TestDateNewsHeadlines = question >> LLMRun() >> SubstringEvaluator("2020-04-05")

if __name__ == "__main__":
    print(run_test(TestDateNewsHeadlines))

