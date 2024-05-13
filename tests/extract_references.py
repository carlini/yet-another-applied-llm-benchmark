from evaluator import *

DESCRIPTION = "Test if the model can extract paper tiles from a block of text."

TAGS = ['code', 'python']

question = '''Extract a list the titles of the papers from the following list of references.
Start your response

```json
[title_1, title_2, ...]
```

Here's the block of text:

A Suffix Arrays                                                         [45] SHOKRI, R., STRONATI, M., SONG, C., AND                                                              
A suffix of length k of a string x are the last k characters (or,       SHMATIKOV, V. Membership inference attacks against                                                        
tokens) of this string, i.e,. x[−k:]                                    machine learning models. In IEEE Symposium on                                                             
. If we want to know: “was                                              Security and Privacy (2017).                                                                              
0 100 200 300                                                           [46] SOLDAINI, L. AI2 Dolma: 3 trillion token open corpus                                                 
length of k-gram                                                        for language model pretraining, 2023.                                                                     
104                                                                     [47] SOMEPALLI, G., SINGLA, V., GOLDBLUM, M., GEIPING, J., AND GOLDSTEIN, T. Diffusion art or digital     
105                                                                     forgery? Investigating data replication in diffusion models. In CVPR (2023).                              
106                                                                     [48] SOUTHWOOD, T. R. E., AND HENDERSON, P. A. Ecological methods. John Wiley & Sons, 2009.               
# generated kgrams                                                      [49] TOUVRON, H., LAVRIL, T., IZACARD, G., MARTINET, X., LACHAUX, M.-A., LACROIX, T., ROZIÈRE, B., GOYAL, 
in training data                                                        N., HAMBRO, E., AZHAR, F., RODRIGUEZ, A., JOULIN, A., GRAVE, E., AND LAMPLE,                              
Figure 14: The suffix length threshold k significantly impacts          G. LLaMA: Open and Efficient Foundation Language                                                          
the rate of data determined to be memorized. We set k = 50.             Models, 2023.                                                                                             
x                                                                       [50] TOUVRON, H., MARTIN, L., STONE, K., ALBERT, P.,                                                      
′                                                                       ALMAHAIRI, A., BABAEI, Y., BASHLYKOV, N., BATRA, S., BHARGAVA, P., BHOSALE, S., ET AL. LLaMA              
[−k:]                                                                   2: Open foundation and fine-tuned chat models. arXiv                                                      
in x”, then we would have to do an O(n) search checking                 preprint arXiv:2307.09288 (2023).                                                                         
all suffixes of x. This linear scan is expensive if x is large,         [51] TTI. Introducing Falcon 180b.                                                                        
as it is in training large language models, often terabytes in          [52] YEOM, S., GIACOMELLI, I., FREDRIKSON, M., AND                                                        
size. Instead, a suffix array will enable us to do this search          JHA, S. Privacy risk in machine learning: Analyzing                                                       
efficiently in O(logn) time.                                            the connection to overfitting. In IEEE CSF (2018).                                                        
A suffix array s over a dataset X, denoted as s(X) is a                 [53] ZELTERMAN, D. Smooth nonparametric estimation of                                                     
data structure that indexes all suffixes of this string in a            the quantile function. Journal of statistical planning                                                    
lexicographically-sorted ordering. This sorting, as we will             and inference 26, 3 (1990), 339–352.                                                                      
see, is important as it enables efficient binary searches for a         [54] ZHANG, S., ROLLER, S., GOYAL, N., ARTETXE, M.,                                                       
particular substring/suffix.                                            CHEN, M., CHEN, S., DEWAN, C., DIAB, M., LI, X.,                                                          
In the simplest form, we can consider the suffix array of a             LIN, X. V., MIHAYLOV, T., OTT, M., SHLEIFER, S.,                                                          
word, e.g., x =“banana”. The following is the set of all suffixes       SHUSTER, K., SIMIG, D., KOURA, P. S., SRIDHAR,                                                            
as obtained by traversing the string backwards and keeping only         A., WANG, T., AND ZETTLEMOYER, L. Opt: Open                                                               
unique suffixes, in this case, all suffixes: {“a”, “na”,                pre-trained transformer language models, 2022.                                                            
“ana”, “nana”, “ anana”, “banana”}, which are represented by            [55] ZIEGLER, A. Github Copilot research recitation, 2021.                                                
the indices s = {5,4,3,2,1,0}. In this form, we still require           [56] ZOU, A., WANG, Z., KOLTER, J. Z., AND FREDRIKSON, M. Universal and transferable adversarial          
an O(n) search as there is no ordering. However, a suffix array         attacks on aligned language models. arXiv preprint                                                        
will store these suffixes in a lexicographically sorted ordering.       arXiv:2307.15043 (2023).                                                                                  
'''


answer = set([
        "membership inference attacks against machine learning models",
        "ai2 dolma: 3 trillion token open corpus for language model pretraining",
        "diffusion art or digital forgery? investigating data replication in diffusion models",
        "ecological methods",
        "llama: open and efficient foundation language models",
        "llama 2: open foundation and fine-tuned chat models",
        "introducing falcon 180b",
        "privacy risk in machine learning: analyzing the connection to overfitting",
        "smooth nonparametric estimation of the quantile function",
        "opt: open pre-trained transformer language models",
        "github copilot research recitation",
        "universal and transferable adversarial attacks on aligned language models",
        ])

def check_ok(dat):
    import json
    dat = dat.replace("```json", "```")
    dat = dat.split("```")[1]
    dat = dat.lower().replace(".","")
    return set(json.loads(dat)) == answer


TestExtractRef = question >> LLMRun() >> PyFunc(check_ok)


if __name__ == "__main__":
    print(run_test(TestExtractRef))




