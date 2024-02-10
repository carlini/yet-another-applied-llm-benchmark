from evaluator import *

DESCRIPTION = "Test if the model can process a large table of text and identify rows with specific values."

TAGS = ['data']

question = '''
Here is a table about information of states and territory.

State / territory	Total (mi2) 	Total (km2) 	Land (mi2) 	Land (km2) 	Water (mi2) 	Water (km2) 	%
water
 Alaska	665,384	1,723,337	570,641	1,477,953	94,743	245,383	14.2%
 Texas	268,596	695,662	261,232	676,587	7,365	19,075	2.7%
 California	163,695	423,967	155,779	403,466	7,916	20,501	4.8%
 Montana	147,040	380,831	145,546	376,962	1,494	3,869	1.0%
 New Mexico	121,590	314,917	121,298	314,161	292	757	0.2%
 Arizona	113,990	295,234	113,594	294,207	396	1,026	0.3%
 Nevada	110,572	286,380	109,781	284,332	791	2,048	0.7%
 Colorado	104,094	269,601	103,642	268,431	452	1,170	0.4%
 Oregon	98,379	254,799	95,988	248,608	2,391	6,191	2.4%
 Wyoming	97,813	253,335	97,093	251,470	720	1,864	0.7%
 Michigan	96,714	250,487	56,539	146,435	40,175	104,052	41.5%
 Minnesota	86,936	225,163	79,627	206,232	7,309	18,930	8.4%
 Utah	84,897	219,882	82,170	212,818	2,727	7,064	3.2%
 Idaho	83,569	216,443	82,643	214,045	926	2,398	1.1%
 Kansas	82,278	213,100	81,759	211,754	520	1,346	0.6%
 Nebraska	77,348	200,330	76,824	198,974	524	1,356	0.7%
 South Dakota	77,116	199,729	75,811	196,350	1,305	3,379	1.7%
 Washington	71,298	184,661	66,456	172,119	4,842	12,542	6.8%
 North Dakota	70,698	183,108	69,001	178,711	1,698	4,397	2.4%
 Oklahoma	69,899	181,037	68,595	177,660	1,304	3,377	1.9%
 Missouri	69,707	180,540	68,742	178,040	965	2,501	1.4%
 Florida	65,758	170,312	53,625	138,887	12,133	31,424	18.5%
 Wisconsin	65,496	169,635	54,158	140,268	11,339	29,367	17.3%
 Georgia	59,425	153,910	57,513	148,959	1,912	4,951	3.2%
 Illinois	57,914	149,995	55,519	143,793	2,395	6,202	4.1%
 Iowa	56,273	145,746	55,857	144,669	416	1,077	0.7%
 New York	54,555	141,297	47,126	122,057	7,429	19,240	13.6%
 North Carolina	53,819	139,391	48,618	125,920	5,201	13,471	9.7%
 Arkansas	53,179	137,732	52,035	134,771	1,143	2,961	2.1%
 Alabama	52,420	135,767	50,645	131,171	1,775	4,597	3.4%
 Louisiana	52,378	135,659	43,204	111,898	9,174	23,761	17.5%
 Mississippi	48,432	125,438	46,923	121,531	1,509	3,907	3.1%
 Pennsylvania	46,054	119,280	44,743	115,883	1,312	3,397	2.8%
 Ohio	44,826	116,098	40,861	105,829	3,965	10,269	8.8%
 Virginia	42,775	110,787	39,490	102,279	3,285	8,508	7.7%
 Tennessee	42,144	109,153	41,235	106,798	909	2,355	2.2%
 Kentucky	40,408	104,656	39,486	102,269	921	2,387	2.3%
 Indiana	36,420	94,326	35,826	92,789	593	1,537	1.6%
 Maine	35,380	91,633	30,843	79,883	4,537	11,750	12.8%
 South Carolina	32,020	82,933	30,061	77,857	1,960	5,076	6.1%
 West Virginia	24,230	62,756	24,038	62,259	192	497	0.8%
 Maryland	12,406	32,131	9,707	25,142	2,699	6,990	21.8%
 Hawaii	10,932	28,313	6,423	16,635	4,509	11,678	41.2%
 Massachusetts	10,554	27,336	7,800	20,202	2,754	7,134	26.1%
 Vermont	9,616	24,906	9,217	23,871	400	1,035	4.2%
 New Hampshire	9,349	24,214	8,953	23,187	397	1,027	4.2%
 New Jersey	8,723	22,591	7,354	19,047	1,368	3,544	15.7%
 Connecticut	5,543	14,357	4,842	12,542	701	1,816	12.6%
 Puerto Rico	5,325	13,791	3,424	8,868	1,901	4,924	35.7%
 Delaware	2,489	6,446	1,949	5,047	540	1,399	21.7%
 Northern Mariana Islands	1,976	5,117	182	472	1,793	4,644	90.7%
 Rhode Island	1,545	4,001	1,034	2,678	511	1,324	33.1%
 U.S. Virgin Islands	733	1,898	134	348	599	1,550	81.7%
 American Samoa	581	1,505	76	198	505	1,307	86.9%
 Guam	571	1,478	210	543	361	935	63.2%
 District of Columbia	68	177	61	158	7	19	10.3%
Minor Outlying Islands[3][a]	16	41	16	41	0	0	0.0%
Contiguous US	3,120,428	8,081,869	2,954,843	7,653,006	165,589	428,865	5.3%
50 States	3,796,676	9,833,342	3,531,846	9,147,436	264,834	685,907	7.0%
50 States and DC	3,796,744	9,833,519	3,531,907	9,147,594	264,841	685,926	7.0%
 United States	3,805,927	9,857,306	3,535,932	9,158,022	269,995	699,284	7.1%

List for me each of the states that have more than 20,000 square kilometers of water, from lowest to highest. Don't list any other states.

'''

stepbystep = """To answer this question follow these steps in order:
1. List just the amount of water in each state.
2. Filter those to ones with over 20k square kilometers of water.
3. Sort them from lowest to highest.
4. Say "The final answer is" and list the states in that order.

"""

evaluation = "This is a student answer about which states have the most water: \n<A>\n\nThe correct answer is: California, Louisiana, Wisconsin, Florida, Michigan, and Alaska (in that order).\n\nDoes the student answer exactly these states in this order? Think out loud about their answer. Then, if the student got the states in this order, answer 'The student passes' otherwise answer 'The student fails'.\n\n"


TestStateTable = question >> LLMRun() >> ((LLMRun(evaluation, llm=EVAL_LLM) >> SubstringEvaluator("student passes")) & SubstringEvaluator("California") & SubstringEvaluator("Louisiana") & SubstringEvaluator("Wisconsin") & SubstringEvaluator("Wisconsin"))
TestStateTableStepbystep = (question + stepbystep) >> LLMRun() >> ((LLMRun(evaluation, llm=EVAL_LLM) >> SubstringEvaluator("student passes")) & SubstringEvaluator("California") & SubstringEvaluator("Louisiana") & SubstringEvaluator("Wisconsin") & SubstringEvaluator("Wisconsin"))


if __name__ == "__main__":
    print(run_test(TestStateTableStepbystep))

