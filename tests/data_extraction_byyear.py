from evaluator import *

DESCRIPTION = "Test if the model can extract structured data from (somewhat) unstructured text."

TAGS = ['data']

question = '''
From the following data extract the best performing defense each year, in the format {year: robust accuracy}

So for example the answer for {"2024": 69.71, "2023": ..., ...}, now fill it in for every other year. Return the answer as a JSON dict.


Rank	Method	Standard
accuracy	AutoAttack
robust
accuracy	Best known
robust
accuracy	AA eval.
potentially
unreliable	Extra
data	Architecture	Venue
1	Robust Principles: Architectural Design Principles for Adversarially Robust CNNs
It uses additional 50M synthetic images in training.	93.27%	71.07%	71.07%	
×
×	RaWideResNet-70-16	BMVC 2023
2	Better Diffusion Models Further Improve Adversarial Training
It uses additional 50M synthetic images in training.	93.25%	70.69%	70.69%	
×
×	WideResNet-70-16	ICML 2023
3	MixedNUTS: Training-Free Accuracy-Robustness Balance via Nonlinearly Mixed Classifiers
It uses an ensemble of networks. The robust base classifier uses 50M synthetic images. 69.71% robust accuracy is due to the original evaluation (Adaptive AutoAttack)	95.19%	70.08%	69.71%	
×
☑	ResNet-152 + WideResNet-70-16	arXiv, Feb 2024
4	Improving the Accuracy-Robustness Trade-off of Classifiers via Adaptive Smoothing
It uses an ensemble of networks. The robust base classifier uses 50M synthetic images.	95.23%	68.06%	68.06%	
×
☑	ResNet-152 + WideResNet-70-16 + mixing network	SIMODS 2024
5	Decoupled Kullback-Leibler Divergence Loss
It uses additional 20M synthetic images in training.	92.16%	67.73%	67.73%	
×
×	WideResNet-28-10	arXiv, May 2023
6	Better Diffusion Models Further Improve Adversarial Training
It uses additional 20M synthetic images in training.	92.44%	67.31%	67.31%	
×
×	WideResNet-28-10	ICML 2023
7	Fixing Data Augmentation to Improve Adversarial Robustness
66.56% robust accuracy is due to the original evaluation (AutoAttack + MultiTargeted)	92.23%	66.58%	66.56%	
×
☑	WideResNet-70-16	arXiv, Mar 2021
8	Improving Robustness using Generated Data
It uses additional 100M synthetic images in training. 66.10% robust accuracy is due to the original evaluation (AutoAttack + MultiTargeted)	88.74%	66.11%	66.10%	
×
×	WideResNet-70-16	NeurIPS 2021
9	Uncovering the Limits of Adversarial Training against Norm-Bounded Adversarial Examples
65.87% robust accuracy is due to the original evaluation (AutoAttack + MultiTargeted)	91.10%	65.88%	65.87%	
×
☑	WideResNet-70-16	arXiv, Oct 2020
10	Revisiting Residual Networks for Adversarial Robustness: An Architectural Perspective	91.58%	65.79%	65.79%	
×
☑	WideResNet-A4	arXiv, Dec. 2022
11	Fixing Data Augmentation to Improve Adversarial Robustness
It uses additional 1M synthetic images in training. 64.58% robust accuracy is due to the original evaluation (AutoAttack + MultiTargeted)	88.50%	64.64%	64.58%	
×
×	WideResNet-106-16	arXiv, Mar 2021
12	Stable Neural ODE with Lyapunov-Stable Equilibrium Points for Defending Against Adversarial Attacks
Based on the model Rebuffi2021Fixing_70_16_cutmix_extra. 64.20% robust accuracy is due to AutoAttack + transfer APGD from Rebuffi2021Fixing_70_16_cutmix_extra	93.73%	71.28%	64.20%	
☑
☑	WideResNet-70-16, Neural ODE block	NeurIPS 2021
13	Fixing Data Augmentation to Improve Adversarial Robustness
It uses additional 1M synthetic images in training. 64.20% robust accuracy is due to the original evaluation (AutoAttack + MultiTargeted)	88.54%	64.25%	64.20%	
×
×	WideResNet-70-16	arXiv, Mar 2021
14	Exploring and Exploiting Decision Boundary Dynamics for Adversarial Robustness
It uses additional 10M synthetic images in training.	93.69%	63.89%	63.89%	
×
×	WideResNet-28-10	ICLR 2023
15	Improving Robustness using Generated Data
It uses additional 100M synthetic images in training. 63.38% robust accuracy is due to the original evaluation (AutoAttack + MultiTargeted)	87.50%	63.44%	63.38%	
×
×	WideResNet-28-10	NeurIPS 2021
16	Robustness and Accuracy Could Be Reconcilable by (Proper) Definition
It uses additional 1M synthetic images in training.	89.01%	63.35%	63.35%	
×
×	WideResNet-70-16	ICML 2022
17	Helper-based Adversarial Training: Reducing Excessive Margin to Achieve a Better Accuracy vs. Robustness Trade-off	91.47%	62.83%	62.83%	
×
☑	WideResNet-34-10	OpenReview, Jun 2021
18	Robust Learning Meets Generative Models: Can Proxy Distributions Improve Adversarial Robustness?
It uses additional 10M synthetic images in training.	87.30%	62.79%	62.79%	
×
×	ResNest152	ICLR 2022
19	Uncovering the Limits of Adversarial Training against Norm-Bounded Adversarial Examples
62.76% robust accuracy is due to the original evaluation (AutoAttack + MultiTargeted)	89.48%	62.80%	62.76%	
×
☑	WideResNet-28-10	arXiv, Oct 2020
20	Exploring Architectural Ingredients of Adversarially Robust Deep Neural Networks
Uses exponential moving average (EMA)	91.23%	62.54%	62.54%	
×
☑	WideResNet-34-R	NeurIPS 2021
21	Exploring Architectural Ingredients of Adversarially Robust Deep Neural Networks	90.56%	61.56%	61.56%	
×
☑	WideResNet-34-R	NeurIPS 2021
22	Parameterizing Activation Functions for Adversarial Robustness
It uses additional ~6M synthetic images in training.	87.02%	61.55%	61.55%	
×
×	WideResNet-28-10-PSSiLU	arXiv, Oct 2021
23	Robustness and Accuracy Could Be Reconcilable by (Proper) Definition
It uses additional 1M synthetic images in training.	88.61%	61.04%	61.04%	
×
×	WideResNet-28-10	ICML 2022
24	Helper-based Adversarial Training: Reducing Excessive Margin to Achieve a Better Accuracy vs. Robustness Trade-off
It uses additional 1M synthetic images in training.	88.16%	60.97%	60.97%	
×
×	WideResNet-28-10	OpenReview, Jun 2021
25	Fixing Data Augmentation to Improve Adversarial Robustness
It uses additional 1M synthetic images in training. 60.73% robust accuracy is due to the original evaluation (AutoAttack + MultiTargeted)	87.33%	60.75%	60.73%	
×
×	WideResNet-28-10	arXiv, Mar 2021
26	Do Wider Neural Networks Really Help Adversarial Robustness?
87.67%	60.65%	60.65%	Unknown	☑	WideResNet-34-15	arXiv, Oct 2020
27	Improving Neural Network Robustness via Persistency of Excitation	86.53%	60.41%	60.41%	
×
☑	WideResNet-34-15	ACC 2022
28	Robust Learning Meets Generative Models: Can Proxy Distributions Improve Adversarial Robustness?
It uses additional 10M synthetic images in training.	86.68%	60.27%	60.27%	
×
×	WideResNet-34-10	ICLR 2022
29	Adversarial Weight Perturbation Helps Robust Generalization	88.25%	60.04%	60.04%	
×
☑	WideResNet-28-10	NeurIPS 2020
30	Improving Neural Network Robustness via Persistency of Excitation	89.46%	59.66%	59.66%	
×
☑	WideResNet-28-10	ACC 2022
31	Geometry-aware Instance-reweighted Adversarial Training
Uses 
ℓ
∞
 = 0.031 ≈ 7.9/255 instead of 8/255.	89.36%	59.64%	59.64%	
×
☑	WideResNet-28-10	ICLR 2021
32	Unlabeled Data Improves Adversarial Robustness	89.69%	59.53%	59.53%	
×
☑	WideResNet-28-10	NeurIPS 2019
33	Improving Robustness using Generated Data
It uses additional 100M synthetic images in training. 58.50% robust accuracy is due to the original evaluation (AutoAttack + MultiTargeted)	87.35%	58.63%	58.50%	
×
×	PreActResNet-18	NeurIPS 2021
34	Data filtering for efficient adversarial training
86.10%	58.09%	58.09%	
×
×	WideResNet-34-20	Pattern Recognition 2024
35	Scaling Adversarial Training to Large Perturbation Bounds	85.32%	58.04%	58.04%	
×
×	WideResNet-34-10	ECCV 2022
36	Efficient and Effective Augmentation Strategy for Adversarial Training	88.71%	57.81%	57.81%	
×
×	WideResNet-34-10	NeurIPS 2022
37	LTD: Low Temperature Distillation for Robust Adversarial Training
86.03%	57.71%	57.71%	
×
×	WideResNet-34-20	arXiv, Nov 2021
38	Helper-based Adversarial Training: Reducing Excessive Margin to Achieve a Better Accuracy vs. Robustness Trade-off	89.02%	57.67%	57.67%	
×
☑	PreActResNet-18	OpenReview, Jun 2021
39	LAS-AT: Adversarial Training with Learnable Attack Strategy
85.66%	57.61%	57.61%	
×
×	WideResNet-70-16	arXiv, Mar 2022
40	A Light Recipe to Train Robust Vision Transformers	91.73%	57.58%	57.58%	
×
☑	XCiT-L12	arXiv, Sep 2022
41	Data filtering for efficient adversarial training
86.54%	57.30%	57.30%	
×
×	WideResNet-34-10	Pattern Recognition 2024
42	A Light Recipe to Train Robust Vision Transformers	91.30%	57.27%	57.27%	
×
☑	XCiT-M12	arXiv, Sep 2022
43	Uncovering the Limits of Adversarial Training against Norm-Bounded Adversarial Examples
57.14% robust accuracy is due to the original evaluation (AutoAttack + MultiTargeted)	85.29%	57.20%	57.14%	
×
×	WideResNet-70-16	arXiv, Oct 2020
44	HYDRA: Pruning Adversarially Robust Neural Networks
Compressed model	88.98%	57.14%	57.14%	
×
☑	WideResNet-28-10	NeurIPS 2020
45	Decoupled Kullback-Leibler Divergence Loss	85.31%	57.09%	57.09%	
×
×	WideResNet-34-10	arXiv, May 2023
46	Helper-based Adversarial Training: Reducing Excessive Margin to Achieve a Better Accuracy vs. Robustness Trade-off
It uses additional 1M synthetic images in training.	86.86%	57.09%	57.09%	
×
×	PreActResNet-18	OpenReview, Jun 2021
47	LTD: Low Temperature Distillation for Robust Adversarial Training
85.21%	56.94%	56.94%	
×
×	WideResNet-34-10	arXiv, Nov 2021
48	Uncovering the Limits of Adversarial Training against Norm-Bounded Adversarial Examples
56.82% robust accuracy is due to the original evaluation (AutoAttack + MultiTargeted)	85.64%	56.86%	56.82%	
×
×	WideResNet-34-20	arXiv, Oct 2020
49	Fixing Data Augmentation to Improve Adversarial Robustness
It uses additional 1M synthetic images in training.	83.53%	56.66%	56.66%	
×
×	PreActResNet-18	arXiv, Mar 2021
50	Improving Adversarial Robustness Requires Revisiting Misclassified Examples	87.50%	56.29%	56.29%	
×
☑	WideResNet-28-10	ICLR 2020
51	LAS-AT: Adversarial Training with Learnable Attack Strategy
84.98%	56.26%	56.26%	
×
×	WideResNet-34-10	arXiv, Mar 2022
52	Adversarial Weight Perturbation Helps Robust Generalization	85.36%	56.17%	56.17%	
×
×	WideResNet-34-10	NeurIPS 2020
53	A Light Recipe to Train Robust Vision Transformers	90.06%	56.14%	56.14%	
×
☑	XCiT-S12	arXiv, Sep 2022
54	Are Labels Required for Improving Adversarial Robustness?	86.46%	56.03%	56.03%	Unknown	☑	WideResNet-28-10	NeurIPS 2019
55	Robust Learning Meets Generative Models: Can Proxy Distributions Improve Adversarial Robustness?
It uses additional 10M synthetic images in training.	84.59%	55.54%	55.54%	
×
×	ResNet-18	ICLR 2022
56	Using Pre-Training Can Improve Model Robustness and Uncertainty	87.11%	54.92%	54.92%	
×
☑	WideResNet-28-10	ICML 2019
57	Bag of Tricks for Adversarial Training
86.43%	54.39%	54.39%	Unknown	×	WideResNet-34-20	ICLR 2021
58	Boosting Adversarial Training with Hypersphere Embedding	85.14%	53.74%	53.74%	
×
×	WideResNet-34-20	NeurIPS 2020
59	Learnable Boundary Guided Adversarial Training
Uses 
ℓ
∞
 = 0.031 ≈ 7.9/255 instead of 8/255	88.70%	53.57%	53.57%	
×
×	WideResNet-34-20	ICCV 2021
60	Attacks Which Do Not Kill Training Make Adversarial Learning Stronger	84.52%	53.51%	53.51%	
×
×	WideResNet-34-10	ICML 2020
61	Overfitting in adversarially robust deep learning	85.34%	53.42%	53.42%	
×
×	WideResNet-34-20	ICML 2020
62	Self-Adaptive Training: beyond Empirical Risk Minimization
Uses 
ℓ
∞
 = 0.031 ≈ 7.9/255 instead of 8/255.	83.48%	53.34%	53.34%	Unknown	×	WideResNet-34-10	NeurIPS 2020
63	Theoretically Principled Trade-off between Robustness and Accuracy
Uses 
ℓ
∞
 = 0.031 ≈ 7.9/255 instead of 8/255.	84.92%	53.08%	53.08%	Unknown	×	WideResNet-34-10	ICML 2019
64	Learnable Boundary Guided Adversarial Training
Uses 
ℓ
∞
 = 0.031 ≈ 7.9/255 instead of 8/255	88.22%	52.86%	52.86%	
×
×	WideResNet-34-10	ICCV 2021
65	Adversarial Robustness through Local Linearization	86.28%	52.84%	52.84%	Unknown	×	WideResNet-40-8	NeurIPS 2019
66	Efficient and Effective Augmentation Strategy for Adversarial Training	85.71%	52.48%	52.48%	
×
×	ResNet-18	NeurIPS 2022
67	Adversarial Robustness: From Self-Supervised Pre-Training to Fine-Tuning
Uses ensembles of 3 models.	86.04%	51.56%	51.56%	Unknown	×	ResNet-50	CVPR 2020
68	Efficient Robust Training via Backward Smoothing
85.32%	51.12%	51.12%	Unknown	×	WideResNet-34-10	arXiv, Oct 2020
69	Scaling Adversarial Training to Large Perturbation Bounds	80.24%	51.06%	51.06%	
×
×	ResNet-18	ECCV 2022
70	Improving Adversarial Robustness Through Progressive Hardening
86.84%	50.72%	50.72%	Unknown	×	WideResNet-34-10	arXiv, Mar 2020
71	Robustness library	87.03%	49.25%	49.25%	Unknown	×	ResNet-50	GitHub,
Oct 2019
72	Harnessing the Vulnerability of Latent Layers in Adversarially Trained Models	87.80%	49.12%	49.12%	Unknown	×	WideResNet-34-10	IJCAI 2019
73	Metric Learning for Adversarial Robustness	86.21%	47.41%	47.41%	Unknown	×	WideResNet-34-10	NeurIPS 2019
74	You Only Propagate Once: Accelerating Adversarial Training via Maximal Principle
Focuses on fast adversarial training.	87.20%	44.83%	44.83%	Unknown	×	WideResNet-34-10	NeurIPS 2019
75	Towards Deep Learning Models Resistant to Adversarial Attacks	87.14%	44.04%	44.04%	Unknown	×	WideResNet-34-10	ICLR 2018
76	Understanding and Improving Fast Adversarial Training
Focuses on fast adversarial training.	79.84%	43.93%	43.93%	Unknown	×	PreActResNet-18	NeurIPS 2020
77	Rethinking Softmax Cross-Entropy Loss for Adversarial Robustness	80.89%	43.48%	43.48%	Unknown	×	ResNet-32	ICLR 2020
78	Fast is better than free: Revisiting adversarial training
Focuses on fast adversarial training.	83.34%	43.21%	43.21%	Unknown	×	PreActResNet-18	ICLR 2020
79	Adversarial Training for Free!	86.11%	41.47%	41.47%	Unknown	×	WideResNet-34-10	NeurIPS 2019
80	MMA Training: Direct Input Space Margin Maximization through Adversarial Training	84.36%	41.44%	41.44%	Unknown	×	WideResNet-28-4	ICLR 2020
81	A Tunable Robust Pruning Framework Through Dynamic Network Rewiring of DNNs
Compressed model	87.32%	40.41%	40.41%	
×
×	ResNet-18	ASP-DAC 2021
82	Controlling Neural Level Sets
Uses 
ℓ
∞
 = 0.031 ≈ 7.9/255 instead of 8/255.	81.30%	40.22%	40.22%	Unknown	×	ResNet-18	NeurIPS 2019
83	Robustness via Curvature Regularization, and Vice Versa	83.11%	38.50%	38.50%	Unknown	×	ResNet-18	CVPR 2019
84	Defense Against Adversarial Attacks Using Feature Scattering-based Adversarial Training	89.98%	36.64%	36.64%	Unknown	×	WideResNet-28-10	NeurIPS 2019
85	Adversarial Interpolation Training: A Simple Approach for Improving Model Robustness	90.25%	36.45%	36.45%	Unknown	×	WideResNet-28-10	OpenReview, Sep 2019
86	Adversarial Defense via Learning to Generate Diverse Attacks	78.91%	34.95%	34.95%	Unknown	×	ResNet-20	ICCV 2019
87	Sensible adversarial learning	91.51%	34.22%	34.22%	Unknown	×	WideResNet-34-10	OpenReview, Sep 2019
88	Towards Stable and Efficient Training of Verifiably Robust Neural Networks
Verifiably robust model with 32.24% provable robust accuracy	44.73%	32.64%	32.64%	Unknown	×	5-layer-CNN	ICLR 2020
89	Bilateral Adversarial Training: Towards Fast Training of More Robust Models Against Adversarial Attacks	92.80%	29.35%	29.35%	Unknown	×	WideResNet-28-10	ICCV 2019
90	Enhancing Adversarial Defense by k-Winners-Take-All
Uses 
ℓ
∞
 = 0.031 ≈ 7.9/255 instead of 8/255.
7.40% robust accuracy is due to 1 restart of APGD-CE and 30 restarts of Square Attack
Note: this adaptive evaluation (Section 5) reports 0.16% robust accuracy on a different model (adversarially trained ResNet-18).	79.28%	18.50%	7.40%	
☑
×	DenseNet-121	ICLR 2020
91	Manifold Regularization for Adversarial Robustness	90.84%	1.35%	1.35%	Unknown	×	ResNet-18	arXiv, Mar 2020
92	Adversarial Defense by Restricting the Hidden Space of Deep Neural Networks	89.16%	0.28%	0.28%	Unknown	×	ResNet-110	ICCV 2019
93	Jacobian Adversarially Regularized Networks for Robustness	93.79%	0.26%	0.26%	Unknown	×	WideResNet-34-10	ICLR 2020
94	ClusTR: Clustering Training for Robustness	91.03%	0.00%	0.00%	Unknown	×	WideResNet-28-10	arXiv, Jun 2020
95	Standardly trained model	94.78%	0.0%	0.0%	Unknown	×	WideResNet-28-10	N/A
'''


TestDataYearExtract = question >> LLMRun() >> ExtractJSON() >> JSONSubsetEvaluator({
    "2024": 69.71,
    "2023": 71.07,
    "2022": 65.79,
    "2021": 66.56,
    "2020": 65.87,
    "2019": 59.53,
    "2018": 44.04
})




if __name__ == "__main__":
    print(run_test(TestDataYearExtract))

