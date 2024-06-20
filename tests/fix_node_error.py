from evaluator import *

DESCRIPTION = "Test if the model can identify a node error message"

TAGS = ['explain']

question = """
How do I fix this

nicholas@npc site % http-server 
dyld[63275]: Library not loaded: /opt/homebrew/opt/icu4c/lib/libicui18n.73.dylib
  Referenced from: <758FD1B7-1836-321E-A1D9-E47EC3C39702> /opt/homebrew/Cellar/node/21.5.0/bin/node
  Reason: tried: '/opt/homebrew/opt/icu4c/lib/libicui18n.73.dylib' (no such file), '/System/Volumes/Preboot/Cryptexes/OS/opt/homebrew/opt/icu4c/lib/libicui18n.73.dylib' (no such file), '/opt/homebrew/opt/icu4c/lib/libicui18n.73.dylib' (no such file), '/opt/homebrew/Cellar/icu4c/74.2/lib/libicui18n.73.dylib' (no such file), '/System/Volumes/Preboot/Cryptexes/OS/opt/homebrew/Cellar/icu4c/74.2/lib/libicui18n.73.dylib' (no such file), '/opt/homebrew/Cellar/icu4c/74.2/lib/libicui18n.73.dylib' (no such file)
"""

TestFixNode = question >> LLMRun() >> SubstringEvaluator("brew reinstall node")
    

if __name__ == "__main__":
    print(run_test(TestFixNode))
