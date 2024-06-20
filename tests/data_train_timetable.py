from evaluator import *

DESCRIPTION = "Test if the model can extract structured data from (somewhat) unstructured text."

TAGS = ['data']

timetable = """
 Station Name 101 501 103 401 105 701 301 403 107 703 303 405 109 705 305 407 111 503 113 505 115 507 117 509 119 511 121 513 123 307 409 125 707 309 411 127 709 311 413 129 711 313 415 131 515 133 135 137 139 141 143 145
Zone Service Type L1 L5 L1 L4 L1 B7 L3 L4 L1 B7 L3 L4 L1 B7 L3 L4 L1 L5 L1 L5 L1 L5 L1 L5 L1 L5 L1 L5 L1 L3 L4 L1 B7 L3 L4 L1 B7 L3 L4 L1 B7 L3 L4 L1 L5 L1 L1 L1 L1 L1 L1 L1
6 Gilroy -- -- -- -- -- -- -- 5:52am -- -- 6:29am 6:50am -- -- 7:29am -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
6 San Martin -- -- -- -- -- -- -- 6:01am -- -- 6:38am 6:59am -- -- 7:38am -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
6 Morgan Hill -- -- -- -- -- -- -- 6:07am -- -- 6:44am 7:05am -- -- 7:44am -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
5 Blossom Hill -- -- -- -- -- -- -- 6:22am -- -- 6:59am 7:20am -- -- 7:59am -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
5 Capitol -- -- -- -- -- -- -- 6:28am -- -- 7:05am 7:26am -- -- 8:05am -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
4 Tamien 4:20am 5:00am -- 5:36am -- -- 6:16am 6:35am -- -- 7:12am 7:33am 7:46am -- 8:12am -- 8:48am -- -- -- 10:46am -- -- -- 12:46pm -- -- -- 2:46pm -- -- -- -- -- -- 4:46pm -- -- -- 5:43pm -- -- -- 6:48pm -- 7:46pm -- 8:36pm -- 9:36pm -- 11:05pm
4 San Jose Diridon 4:26am 5:07am 5:13am 5:42am 5:52am 5:57am 6:23am 6:42am 6:52am 6:57am 7:21am 7:40am 7:52am 7:57am 8:21am 8:42am 8:54am 9:41am 9:52am 10:41am 10:52am 11:41am 11:52am 12:41pm 12:52pm 1:41pm 1:52pm 2:41pm 2:52pm 3:20pm 3:42pm 3:52pm 3:57pm 4:21pm 4:42pm 4:52pm 4:57pm 5:21pm 5:42pm 5:52pm 5:57pm 6:21pm 6:42pm 6:54pm 7:41pm 7:52pm 8:11pm 8:43pm 9:12pm 9:43pm 10:30pm 11:12pm
4 College Park -- -- -- -- -- -- -- -- -- -- -- 7:44am -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 3:24pm -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
4 Santa Clara 4:32am 5:13am 5:19am 5:48am 5:58am -- -- 6:48am 6:58am -- -- 7:48am 7:58am -- -- 8:48am 9:00am 9:47am 9:58am 10:47am 10:58am 11:47am 11:58am 12:47pm 12:58pm 1:47pm 1:58pm 2:47pm 2:58pm -- 3:48pm 3:58pm -- -- 4:48pm 4:58pm -- -- 5:48pm 5:58pm -- -- 6:48pm 7:00pm 7:47pm 7:58pm 8:17pm 8:49pm 9:18pm 9:49pm 10:36pm 11:18pm
4 Lawrence 4:38am -- 5:25am -- 6:07am -- 6:33am -- 7:07am -- 7:31am -- 8:07am -- 8:31am -- 9:06am -- 10:04am -- 11:04am -- 12:04pm -- 1:04pm -- 2:04pm -- 3:04pm 3:31pm -- 4:07pm -- 4:31pm -- 5:07pm -- 5:31pm -- 6:07pm -- 6:31pm -- 7:06pm -- 8:04pm 8:23pm 8:55pm 9:24pm 9:55pm 10:42pm 11:24pm
3 Sunnyvale 4:42am 5:21am 5:29am 5:56am 6:12am -- 6:37am 6:56am 7:12am -- 7:35am 7:56am 8:12am -- 8:35am 8:56am 9:10am 9:54am 10:08am 10:54am 11:08am 11:54am 12:08pm 12:54pm 1:08pm 1:54pm 2:08pm 2:54pm 3:08pm 3:36pm 3:56pm 4:12pm -- 4:35pm 4:56pm 5:12pm -- 5:35pm 5:56pm 6:12pm -- 6:35pm 6:56pm 7:10pm 7:54pm 8:08pm 8:27pm 8:59pm 9:28pm 9:59pm 10:46pm 11:28pm
3 Mountain View 4:47am 5:25am 5:34am 6:01am 6:17am 6:11am 6:42am 7:01am 7:17am 7:11am 7:40am 8:01am 8:17am 8:11am 8:40am 9:01am 9:15am 9:59am 10:13am 10:59am 11:13am 11:59am 12:13pm 12:59pm 1:13pm 1:59pm 2:13pm 2:59pm 3:13pm 3:41pm 4:01pm 4:17pm 4:11pm 4:40pm 5:01pm 5:17pm 5:11pm 5:40pm 6:01pm 6:17pm 6:11pm 6:40pm 7:01pm 7:15pm 7:59pm 8:13pm 8:32pm 9:04pm 9:33pm 10:04pm 10:51pm 11:33pm
3 San Antonio 4:51am -- 5:38am -- 6:20am -- 6:46am -- 7:20am -- 7:44am -- 8:20am -- 8:44am -- 9:19am -- 10:17am -- 11:17am -- 12:17pm -- 1:17pm -- 2:17pm -- 3:17pm 3:44pm -- 4:20pm -- 4:44pm -- 5:20pm -- 5:44pm -- 6:20pm -- 6:44pm -- 7:19pm -- 8:17pm 8:36pm 9:08pm 9:37pm 10:08pm 10:55pm 11:37pm
3 California Avenue 4:55am -- 5:42am -- 6:25am -- 6:50am -- 7:25am -- 7:48am -- 8:25am -- 8:48am -- 9:23am -- 10:22am -- 11:22am -- 12:22pm -- 1:22pm -- 2:22pm -- 3:22pm 3:49pm -- 4:25pm -- 4:48pm -- 5:25pm -- 5:48pm -- 6:25pm -- 6:48pm -- 7:23pm -- 8:21pm 8:40pm 9:12pm 9:41pm 10:12pm 10:59pm 11:41pm
3 Palo Alto 4:59am 5:33am 5:46am 6:08am 6:29am 6:19am 6:54am 7:09am 7:29am 7:19am 7:52am 8:09am 8:29am 8:19am 8:52am 9:09am 9:27am 10:07am 10:26am 11:07am 11:26am 12:07pm 12:26pm 1:07pm 1:26pm 2:07pm 2:26pm 3:07pm 3:26pm 3:53pm 4:09pm 4:29pm 4:19pm 4:52pm 5:09pm 5:29pm 5:19pm 5:52pm 6:09pm 6:29pm 6:19pm 6:52pm 7:09pm 7:27pm 8:07pm 8:25pm 8:44pm 9:17pm 9:45pm 10:17pm 11:03pm 11:46pm
3 Menlo Park 5:02am 5:37am 5:50am -- 6:32am -- 6:58am -- 7:32am -- 7:56am -- 8:32am -- 8:56am -- 9:31am 10:10am 10:30am 11:10am 11:30am 12:10pm 12:30pm 1:10pm 1:30pm 2:10pm 2:30pm 3:10pm 3:30pm 3:56pm -- 4:32pm -- 4:56pm -- 5:32pm -- 5:56pm -- 6:32pm -- 6:56pm -- 7:30pm 8:10pm 8:28pm 8:47pm 9:20pm 9:49pm 10:20pm 11:07pm 11:50pm
2 Redwood City 5:08am 5:42am 5:55am 6:15am 6:38am 6:26am 7:03am 7:15am 7:38am 7:26am 8:01am 8:15am 8:38am 8:26am 9:01am 9:15am 9:36am 10:16am 10:35am 11:16am 11:35am 12:16pm 12:35pm 1:16pm 1:35pm 2:16pm 2:35pm 3:16pm 3:35pm 4:02pm 4:15pm 4:38pm 4:26pm 5:01pm 5:15pm 5:38pm 5:26pm 6:01pm 6:15pm 6:38pm 6:26pm 7:01pm 7:15pm 7:36pm 8:16pm 8:34pm 8:53pm 9:27pm 9:55pm 10:27pm 11:13pm 11:56pm
2 San Carlos 5:13am -- 6:00am 6:20am 6:42am -- -- 7:20am 7:42am -- -- 8:20am 8:42am -- -- 9:20am 9:41am -- 10:40am -- 11:40am -- 12:40pm -- 1:40pm -- 2:40pm -- 3:40pm -- 4:20pm 4:42pm -- -- 5:20pm 5:42pm -- -- 6:20pm 6:42pm -- -- 7:20pm 7:41pm -- 8:39pm 8:58pm 9:32pm 10:00pm 10:32pm 11:18pm 11:59pm
2 Belmont 5:16am -- 6:04am -- 6:46am -- 7:09am -- 7:46am -- 8:07am -- 8:46am -- 9:07am -- 9:44am -- 10:43am -- 11:43am -- 12:43pm -- 1:43pm -- 2:43pm -- 3:43pm 4:08pm -- 4:46pm -- 5:07pm -- 5:46pm -- 6:07pm -- 6:46pm -- 7:07pm -- 7:44pm -- 8:42pm 9:01pm 9:35pm 10:04pm 10:35pm 11:22pm 12:05am
2 Hillsdale 5:20am 5:50am 6:08am -- 6:50am 6:34am 7:13am -- 7:50am 7:34am 8:11am -- 8:50am 8:34am 9:11am -- 9:48am 10:23am 10:47am 11:23am 11:47am 12:23pm 12:47pm 1:23pm 1:47pm 2:23pm 2:47pm 3:23pm 3:47pm 4:12pm -- 4:50pm 4:34pm 5:11pm -- 5:50pm 5:34pm 6:11pm -- 6:50pm 6:34pm 7:11pm -- 7:49pm 8:24pm 8:47pm 9:06pm 9:39pm 10:08pm 10:39pm 11:26pm 12:09am
2 Hayward Park 5:23am -- 6:11am -- 6:53am -- -- -- 7:53am -- -- -- 8:53am -- -- -- 9:51am -- 10:50am -- 11:50am -- 12:50pm -- 1:50pm -- 2:50pm -- 3:50pm -- -- 4:53pm -- -- -- 5:53pm -- -- -- 6:53pm -- -- -- 7:52pm -- 8:50pm 9:09pm 9:42pm 10:11pm 10:42pm 11:29pm 12:12am
2 San Mateo 5:26am 5:55am 6:14am 6:28am 6:56am -- -- 7:28am 7:56am -- -- 8:28am 8:56am -- -- 9:28am 9:55am 10:29am 10:54am 11:29am 11:54am 12:29pm 12:54pm 1:29pm 1:54pm 2:29pm 2:54pm 3:29pm 3:54pm -- 4:28pm 4:56pm -- -- 5:28pm 5:56pm -- -- 6:28pm 6:56pm -- -- 7:28pm 7:56pm 8:29pm 8:54pm 9:13pm 9:46pm 10:15pm 10:46pm 11:33pm 12:16am
2 Burlingame 5:30am -- 6:18am 6:31am 7:00am -- -- 7:31am 8:00am -- -- 8:31am 9:00am -- -- 9:31am 9:59am -- 10:58am -- 11:58am -- 12:58pm -- 1:58pm -- 2:58pm -- 3:58pm -- 4:31pm 5:00pm -- -- 5:31pm 6:00pm -- -- 6:31pm 7:00pm -- -- 7:31pm 8:00pm -- 8:58pm 9:17pm 9:50pm 10:18pm 10:50pm 11:36pm 12:19am
2 Millbrae 5:35am 6:01am 6:23am 6:36am 7:04am 6:44am 7:21am 7:36am 8:04am 7:44am 8:19am 8:36am 9:04am 8:44am 9:19am 9:37am 10:04am 10:36am 11:03am 11:36am 12:03pm 12:36pm 1:03pm 1:36pm 2:03pm 2:36pm 3:03pm 3:36pm 4:03pm 4:20pm 4:36pm 5:04pm 4:44pm 5:19pm 5:36pm 6:04pm 5:44pm 6:19pm 6:36pm 7:04pm 6:44pm 7:19pm 7:36pm 8:06pm 8:35pm 9:04pm 9:23pm 9:55pm 10:24pm 10:55pm 11:42pm 12:26am
1 San Bruno 5:39am -- 6:28am 6:41am 7:09am -- -- 7:41am 8:09am -- -- 8:41am 9:09am -- -- 9:42am 10:08am -- 11:08am -- 12:08pm -- 1:08pm -- 2:08pm -- 3:08pm -- 4:08pm -- 4:41pm 5:09pm -- -- 5:41pm 6:09pm -- -- 6:41pm 7:09pm -- -- 7:41pm 8:10pm -- 9:08pm 9:27pm 10:00pm 10:29pm 10:59pm 11:47pm 12:30am
1 South San Francisco 5:43am -- 6:32am -- 7:13am -- 7:28am -- 8:13am -- 8:26am -- 9:13am -- 9:26am -- 10:13am -- 11:13am -- 12:13pm -- 1:13pm -- 2:13pm -- 3:13pm -- 4:13pm 4:27pm -- 5:13pm -- 5:26pm -- 6:13pm -- 6:26pm -- 7:13pm -- 7:26pm -- 8:14pm -- 9:12pm 9:31pm 10:04pm 10:33pm 11:03pm 11:51pm 12:34am
1 Bayshore 5:50am -- 6:38am -- 7:19am -- -- -- 8:19am -- -- -- 9:19am -- -- -- 10:19am -- 11:19am -- 12:19pm -- 1:19pm -- 2:19pm -- 3:19pm -- 4:19pm -- -- 5:19pm -- -- -- 6:19pm -- -- -- 7:19pm -- -- -- 8:21pm -- 9:19pm 9:38pm 10:11pm 10:39pm 11:10pm 11:57pm 12:40am
1 22nd Street 5:55am 6:14am 6:44am 6:52am 7:24am -- -- 7:52am 8:24am -- -- 8:52am 9:24am -- -- 9:53am 10:25am 10:49am 11:25am 11:49am 12:25pm 12:49pm 1:25pm 1:49pm 2:25pm 2:49pm 3:25pm 3:49pm 4:25pm 4:36pm 4:52pm 5:24pm 4:58pm 5:35pm 5:52pm 6:24pm 5:58pm 6:35pm 6:52pm 7:25pm 6:58pm 7:35pm 7:52pm 8:27pm 8:50pm 9:25pm 9:44pm 10:16pm 10:45pm 11:15pm 12:03am 12:46am
1 San Francisco 6:01am 6:20am 6:50am 6:58am 7:31am 7:03am 7:41am 7:58am 8:31am 8:03am 8:39am 8:58am 9:31am 9:03am 9:39am 9:59am 10:31am 10:55am 11:31am 11:55am 12:31pm 12:55pm 1:31pm 1:55pm 2:31pm 2:55pm 3:31pm 3:55pm 4:31pm 4:41pm 4:58pm 5:31pm 5:03pm 5:41pm 5:58pm 6:31pm 6:03pm 6:41pm 6:58pm 7:32pm 7:03pm 7:41pm 7:58pm 8:33pm 8:59pm 9:31pm 9:50pm 10:24pm 10:53pm 11:23pm 12:11am 12:52am
"""

question = '''How long does the 703, 303, and 509 train take to get from Mountain View to San Francisco in minutes? Answer in JSON {"703": time in minutes, "303": ..., "509": ...}.'''


TestTrainSchedule = (question+timetable) >> LLMRun() >> ExtractJSON() >> JSONSubsetEvaluator({
    "703": 52,
    "303": 59,
    "509": 56,
})

question_hard = '''It's currently 6:00pm and I'm at Belmont station. I want to get to San Bruno. Tell me how to get there with which train(s) to take, and what time I will arrive, to arrive as soon as possible'''


TestTrainScheduleHard = (question_hard+timetable) >> LLMRun() >> (SubstringEvaluator("6:41") & SubstringEvaluator("Millbrae"))

question_python = '''Write a python function called 'mtv_to_sf(str) -> json' that will take a timetable like the following as a string as input, and return how long it takes the 703, 303, and 509 trains to get from Mountain View to San Francisco in minutes? Answer in JSON {"703": time in minutes, "303": ..., "509": ...}. The timetable may change over time so write the function to look at the new data I have in the future.'''


test_case, answer = make_python_test([("mtv_to_sf("+repr(timetable)+")", {
    "703": 52,
    "303": 59,
    "509": 56,
})])


TestTrainSchedulePython = (question_python+timetable) >> LLMRun() >> ExtractCode(keep_main=False) >> PythonRun(test_case) >> SubstringEvaluator(answer)




if __name__ == "__main__":
    print(run_test(TestTrainScheduleHard))

