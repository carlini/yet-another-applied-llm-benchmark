import sys
import re
import importlib
import tests
import os
import llm
import numpy as np
import matplotlib.pyplot as plt
import json

from evaluator import Env, Conversation, run_test
import markdown

import multiprocessing as mp

def run_one_test(test, test_llm, eval_llm, vision_eval_llm):
    import docker_controller
    env = Env()
    test.setup(env, Conversation(test_llm), test_llm, eval_llm, vision_eval_llm)

    for success, output in test():
        if success:
            if env.container:
                docker_controller.async_kill_container(env.docker, env.container)
            return True, output
        else:
            pass
    if env.container:
        docker_controller.async_kill_container(env.docker, env.container)
    return False, output
                    


def run_all_tests(test_llm):
    test_llm = llm.LLM(model)
    sr = {}
    for f in os.listdir("tests"):
        if not f.endswith(".py")  or 'basic' not in f : continue
        try:
            spec = importlib.util.spec_from_file_location(f[:-3], "tests/" + f)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except:
            continue
        test_case = [x for x in dir(module) if x.startswith("Test") and x != "TestCase"]
        if len(test_case) == 0:
            #print("Failure", f)
            pass
        else:
            print(f)
            for t in test_case:
                print("Run Job", t)
                tmp = sys.stdout
                sys.stdout = open(os.devnull, 'w')

                test = getattr(module, t)

                ok, reason = run_one_test(test, test_llm, llm.eval_llm, llm.vision_eval_llm)
                fmt = reason.format_markdown()
                while '\n\n' in fmt:
                    fmt = fmt.replace('\n\n', '\n')
                fmt = fmt.replace("\n#", "\n\n#")

                sys.stdout = tmp
                if ok:
                    print("Test Passes:", t)
                else:
                    print("Test Fails:", t, 'from', f)
                sr[f+"."+t] = (ok, fmt)
    return sr


def generate_report(data, tags):
    reasons = {key: {k1: v1[1] for k1,v1 in value.items()} for key, value in data.items()}
    data = {key: {k1: v1[0] for k1,v1 in value.items()} for key, value in data.items()}
    
    # Recalculating all keys to ensure they are in the same order
    all_keys = sorted({key for inner_dict in data.values() for key in inner_dict.keys()})
    print(all_keys,tags.keys())
    assert set(all_keys) == set(tags.keys())
    
    # Calculating mean correctness for each column (key in inner dictionaries)
    column_means = {key: sum(inner_dict.get(key, 0) for inner_dict in data.values()) / len(data) for key in all_keys}

    
    # Sorting columns by mean correctness
    sorted_columns = sorted(all_keys, key=lambda x: column_means[x], reverse=True)
    
    # Calculating mean correctness for each row (outer keys) and sorting them
    row_means = {outer_key: sum(value for value in inner_dict.values()) / len(inner_dict) for outer_key, inner_dict in data.items()}
    sorted_rows = sorted(data.keys(), key=lambda x: row_means[x], reverse=True)

    print(row_means)

    # Transposing the data: columns become rows and rows become columns.
    transposed_data = {}
    for column in sorted_columns:
        transposed_data[column] = {row: data[row][column] for row in sorted_rows if column in data[row]}
    
    # Sorting the transposed columns (originally rows) by their mean correctness
    sorted_transposed_columns = sorted(transposed_data.keys(), key=lambda x: column_means[x], reverse=True)
    
    # Sorting the transposed rows (originally columns) by their mean correctness
    sorted_transposed_rows = sorted(transposed_data[sorted_transposed_columns[0]].keys(), key=lambda x: row_means[x], reverse=True)
    
    # Creating the HTML content with transposed and sorted rows and columns
    html_content = "<html><head><style>td, th {border: 1px solid black; padding: 10px;}</style></head><body>"

    tag_values = set(sum([tags[key] for key in tags], []))
    
    for tag in tag_values:
        html_content += "<span><input type='checkbox' onclick='hiderows()' id='" + tag + "' name='" + tag + "' value='" + tag + "' checked='checked'><label for='" + tag + "'/>" + tag + "</label> | </span>"

    html_content += """<script>
function hiderows() {
    var checkboxes = document.querySelectorAll('input[type="checkbox"]');
    var checked = Array.prototype.slice.call(checkboxes).filter(cb => cb.checked).map(cb => cb.value);
    var rows = document.querySelectorAll('tr');
    console.log(checked);
    // show a row if all of the tags applies
    Array.prototype.slice.call(rows).forEach((row,id) => {
    if (id == 0) return;
    // allow th special
    console.log(checked)
        if (checked.every(tag=>row.getAttribute('tag_'+tag))) {
            row.style.display = 'table-row';
        } else {
            row.style.display = 'none';
        }
    });
}
</script>
"""
    

    html_content += "<table>"
    # Adding the transposed sorted header row (originally columns, now rows)
    html_content += "<tr><th>Question</th><th>Tags</th>" + "".join([f"<th>{key}</th>" for key in sorted_transposed_rows]) + "</tr>"
    
    # Adding transposed sorted rows (originally keys from inner dictionaries, now columns)
    for column_key in sorted_transposed_columns:
        if column_key not in tags:
            print("BAD", tags, column_key)
        this_tags = tags[column_key]

        format_column_key = f'<a href="TODO/tests/{column_key}.py">{column_key}</a>'
        html_content += f"""<tr {' '.join('tag_%s="1"'%x for x in this_tags)}><th>{format_column_key}</th><td>{', '.join(this_tags)}</td>"""
        for row_key in sorted_transposed_rows:
            value = transposed_data[column_key].get(row_key)
            # Color coding the cell or leaving it blank if the value is None
            link = "evaluation_examples/"+column_key+"_"+row_key+".html"
            cell_html = f"<td style='background-color: {'#aaffaa' if value else '#ffaaaa'};'><a href='{link}'>{str(value)}</a></td>" if value is not None else "<td></td>"
            html_content += cell_html
        html_content += "</tr>"
    
    # Closing the table and HTML tags.
    html_content += "</table></body></html>"
    
    # Saving the HTML content to a new file
    html_file_path_transposed_sorted = "evaluation_grid.html"
    with open(html_file_path_transposed_sorted, "w") as file:
        file.write(html_content)

    css = """
    <style>
    code {
        white-space: pre-wrap;
    }
    </style>
    """
    
        
    for column_key in sorted_transposed_columns:
        for row_key in sorted_transposed_rows:
            print("Do, ", column_key, row_key)
            ioutput = output = reasons[row_key][column_key]
            output = re.sub('```[a-z]*', '```', output)
            print(1)
            output = output.split("```")
            print(2)
            output = [output[0]] + ["<code>  "+'\n  '.join(x.split('\n'))+"</code>" if i%2 == 0 else x.replace("\n", "<br>\n") for i,x in enumerate(output[1:])]
            print(3)
            output = "".join(output)
            print(4)
            if len(output) > 100000:
                output = output[:100000] + "..."
            open("evaluation_examples/"+column_key+"_"+row_key+".html", "w").write(css+markdown.markdown(output))
            print(5)
            
        

def get_tags():
    tags = {}
    for f in os.listdir("tests"):
        if not f.endswith(".py") or 'basic' not in f: continue
        try:
            spec = importlib.util.spec_from_file_location(f[:-3], "tests/" + f)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except:
            continue
        if 'TAGS' in dir(module):
            test_case = [x for x in dir(module) if x.startswith("Test") and x != "TestCase"]
            if len(test_case) == 2:
                print("DOUBLE", test_case)
            for t in test_case:
                tags[f+"."+t] = module.TAGS
    return tags

def draw_correlation(nested_dict):
    # Extracting data into a matrix form
    keys = list(nested_dict.keys())
    data = np.array([list(nested_dict[key].values()) for key in keys])
    
    # Compute the correlation matrix
    corr_matrix = np.corrcoef(data)
    
    # Plotting the correlation matrix
    plt.imshow(corr_matrix, cmap='hot', interpolation='nearest')
    plt.colorbar()
    plt.xticks(range(len(keys)), keys)
    plt.yticks(range(len(keys)), keys)
    plt.title("Pairwise Similarity Matrix")
    plt.show()


    
data = {}    
#for model in ["mistral-tiny", "mistral-small", "mistral-medium", "gpt-3.5-turbo", "gpt-4-1106-preview"]:#, "/Users/Nicholas/Downloads/llama-2-13b-chat.Q4_K_M.gguf"]:
#for model in ["mistral-tiny"]:
#for model in ["gpt-3.5-turbo", "gemini-pro", "chat-bison", "mistral-medium", "mistral-small", "mistral-tiny", "gpt-4-1106-preview"]:
#    data[model] = run_all_tests(model)
#open("/tmp/data", "w").write(json.dumps(data))
data = json.loads(open("/tmp/data2").read())

tags = get_tags()

generate_report(data, tags)

#draw_correlation(data)
