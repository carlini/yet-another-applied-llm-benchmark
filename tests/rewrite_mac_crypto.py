from evaluator import *

DESCRIPTION = "Test the ability of the model to rewrite a simple c program so it will run on ubuntu, and keep bugs in place."

TAGS = ['code', 'c']

question = """
Rewrite this c code so it will run on ubuntu. DO NOT FIX ANY BUGS.

```c
#include <stdio.h>
#include <strings.h>
#include <CommonCrypto/CommonDigest.h>

unsigned char memory[1<<20];
void* malloc_ptr = (void*)&memory;

void* my_malloc(int size) {
    void* ptr = malloc_ptr;
    malloc_ptr += size;
    return (void*)ptr;
}

void compute_md5(char *str, unsigned char *hex_result) {
    unsigned char result[CC_MD5_DIGEST_LENGTH];
    CC_MD5_CTX md5ctx;
    CC_MD5_Init(&md5ctx);
    CC_MD5_Update(&md5ctx, str, strlen(str));
    CC_MD5_Final(result, &md5ctx);

    for (int i = 0; i < CC_MD5_DIGEST_LENGTH; i++) {
        sprintf((char*)(hex_result + (i * 2)), "%02x", result[i]);
    }
}

int main(int argc, char** argv) {
    char* msg = (char*)my_malloc(32);
    char* result = (char*)my_malloc(33);
    msg[0] = '\0';

    compute_md5(argv[1], (unsigned char*)result);
    result[33] = '\0';

    strcat(msg, "Your password is wrong, ");
    strcat(msg, argv[2]);

    if (strcmp(result, "13bd041ac6e683f0c8ddba41eeed9e67") == 0) {
      puts("CORRECT!");
      return 0;
    } else {
      puts(msg);
      return 1;
    }
}
```
"""

TestProgramRewriteCCrypto = question >> LLMRun() >> ExtractCode(keep_main=True) >> \
    ((CRun(gccflags="-lcrypto", argv="emacsisbetterthanvim a") >> SubstringEvaluator("CORRECT!")) &
     (CRun(gccflags="-lcrypto", argv="randompw a") >> SubstringEvaluator("wrong")) &
     (CRun(gccflags="-lcrypto", argv=f"a {'a'*8}13bd041ac6e683f0c8ddba41eeed9e67") >> SubstringEvaluator("CORRECT!")))
     


if __name__ == "__main__":
    from llm import llm
    print(run_test(TestProgramRewriteCCrypto))

