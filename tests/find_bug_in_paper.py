from evaluator import *

DESCRIPTION = "Test if a model can find math errors in the latex source of a paper."

TAGS = ['explain']

question = r"""
# Setup

Which of the following equations are incorrect according to the specification?

# Notation

A neural network is a function $F(x) = y$ that accepts an input $x \in \mathbb{R}^n$
and produces an output $y \in \mathbb{R}^m$.
The model $F$ also implicitly depends on some model parameters $\theta$; in our work
the model is fixed, so for convenience we don't show the dependence on $\theta$.

In this paper we focus on neural networks used as an $m$-class classifier.
The output of the network is computed using the softmax function,
which ensures that the output vector $y$ satisfies
$0 \le y_i \le 1$ and $y_1 + \dots + y_m = 1$.
The output vector $y$ is thus treated as a probability distribution, i.e.,
$y_i$ is treated as the probability that input $x$ has class $i$.
The classifier assigns the label $C(x) = \arg\max_i F(x)_i$ to the input $x$.
Let $C^*(x)$ be the correct label of $x$.
The inputs to the softmax function are called \emph{logits}.

We use the notation from Papernot et al. \cite{distillation}: define $F$ to
be the full neural network including the softmax function, $Z(x) = z$ to be the output of
all layers except the softmax (so $z$ are the logits), and
\begin{equation*}
F(x) = \softmax(Z(x)) = y.
\end{equation*}
A neural network typically \footnote{Most simple networks have this simple
  linear structure, however other more sophisticated networks have
  more complicated structures (e.g., ResNet \cite{he2016deep} and Inception \cite{szegedy2015rethinking}).
  The network architecture does not impact our attacks.}
consists of layers
\begin{equation*}
F = \softmax \circ F_n \circ F_{n-1} \circ \cdots \circ F_1
\end{equation*}
where
\begin{equation*}
F_i(x)  = \sigma(\theta_i \cdot x) + \hat\theta_i
\end{equation*}
for some non-linear activation function $\sigma$, some matrix $\theta_i$ of model
weights, and some vector $\hat\theta_i$ of model biases. Together $\theta$ and
$\hat\theta$ make up the model parameters.
Common choices of $\sigma$
are tanh \cite{mishkin2015all}, sigmoid, ReLU \cite{maas2013rectifier}, or ELU \cite{clevert2015fast}.
In this paper we focus primarily on networks that use a ReLU activation function,
as it currently is the most widely used
activation function
\cite{szegedy2015rethinking,springenberg2014striving,mishkin2015all,distillation}.


# Specification:

We define an objective function $f$ such that
$C(x+\delta) = t$ if and only if $f(x+\delta) \le 0$.
There are many possible choices for $f$:

# The equations

\begin{align*}
f_{1}(x') &= -\loss_{F,t}(x') + 1\\
f_{2}(x') &= (\max_{i \ne t}( F(x')_i) - F(x')_t)^+\\
f_{3}(x') &= \text{softplus}(\max_{i \ne t}(F(x')_i) - F(x')_t)-\log(2)\\
f_{4}(x') &= (0.5 - F(x')_t)^+\\
f_{5}(x') &= -\log(2 F(x')_t - 2)\\
f_{6}(x') &= (\max_{i \ne t}( Z(x')_i) - Z(x')_t)^+\\
f_{7}(x') &= \text{softplus}(\max_{i \ne t}(Z(x')_i) - Z(x')_t)-\log(2)
\end{align*}
where $s$ is the correct classification, $(e)^+$ is short-hand for
$\max(e,0)$, $\text{softplus}(x) = \log(1+\exp(x))$, and
$\loss_{F,s}(x)$ is the cross entropy loss for $x$.

# Your task

Consider each equation one by one. End your answer with a python list of numbers [1,2,3,4,5,6,7] for those that are wrong.
"""

question_easier = question + "\nSpecifically, make sure that $C(x+\delta) = t$ if and only if $f(x+\delta) \le 0$. Think step by step about if this is true for each equation and then give your answer as a python list"

def check(x):
    ints = list(map(int,x.split("[")[-1].split("]")[0].split(",")))
    return ints == [1,3,4,5,7], ""

TestFindBugPaper = question >> LLMRun() >> Echo() >> PyFunc(check)

TestFindBugPaperEasy = question_easier >> LLMRun() >> Echo() >> PyFunc(check)


if __name__ == "__main__":
    print(run_test(TestFindBugPaper))
