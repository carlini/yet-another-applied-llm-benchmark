from evaluator import *

DESCRIPTION = "Test if the model can implement some string logic given a fuzzy description."

TAGS = ['code', 'python']

question = """
Given a parse function like

def parse_transcript(content):
    transcript_segments = []
    pattern = r'\[(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})\]  (.*)'
    matches = re.findall(pattern, content)

    for start_time, end_time, text in matches:
        start_seconds = timedelta(hours=int(start_time[:2]), minutes=int(start_time[3:5]), seconds=int(start_time[6:8]), milliseconds=int(start_time[9:])).total_seconds()
        end_seconds = timedelta(hours=int(end_time[:2]), minutes=int(end_time[3:5]), seconds=int(end_time[6:8]), milliseconds=int(end_time[9:])).total_seconds()
        transcript_segments.append((start_seconds, end_seconds, text))

    return transcript_segments


for data like

[00:00:14.240 --> 00:00:14.420]   the
[00:00:14.420 --> 00:00:14.860]   robust
[00:00:14.860 --> 00:00:15.020]  ness
[00:00:15.020 --> 00:00:15.140]   of
[00:00:15.140 --> 00:00:15.500]   neural
[00:00:15.500 --> 00:00:15.870]   networks
[00:00:15.870 --> 00:00:16.200]  .
[00:00:16.200 --> 00:00:16.410]   And
[00:00:16.410 --> 00:00:16.700]   this
[00:00:16.700 --> 00:00:16.840]   is
[00:00:16.840 --> 00:00:17.200]   joint


write a merge() function that (1) calls parse and (2) merges words into sentences that end in period. Start with the first word and end with the period. Return a list of strings.
"""

test_case, answer = make_python_test([("""merge("[00:00:14.240 --> 00:00:14.420]   the\\n[00:00:14.420 --> 00:00:14.860]   robust\\n[00:00:14.860 --> 00:00:15.020]  ness\\n[00:00:15.020 --> 00:00:15.140]   of\\n[00:00:15.140 --> 00:00:15.500]   neural\\n[00:00:15.500 --> 00:00:15.870]   networks\\n[00:00:15.870 --> 00:00:16.200]  .\\n[00:00:16.200 --> 00:00:16.410]   And\\n[00:00:16.410 --> 00:00:16.700]   this\\n[00:00:16.700 --> 00:00:16.840]   is\\n[00:00:16.840 --> 00:00:17.200]   joint\\n")""", "[' the robustness of neural networks.', ' And this is joint']")], header="""
def parse_transcript(content):
    transcript_segments = []
    pattern = r'\[(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})\]  (.*)'
    matches = re.findall(pattern, content)

    for start_time, end_time, text in matches:
        start_seconds = timedelta(hours=int(start_time[:2]), minutes=int(start_time[3:5]), seconds=int(start_time[6:8]), milliseconds=int(start_time[9:])).total_seconds()
        end_seconds = timedelta(hours=int(end_time[:2]), minutes=int(end_time[3:5]), seconds=int(end_time[6:8]), milliseconds=int(end_time[9:])).total_seconds()
        transcript_segments.append((start_seconds, end_seconds, text))

    return transcript_segments
""")


TestWhisperMerge = question >> LLMRun() >> ExtractCode() >> PythonRun(test_case) >> SubstringEvaluator(answer)

if __name__ == "__main__":
    print(run_test(TestWhisperMerge))
