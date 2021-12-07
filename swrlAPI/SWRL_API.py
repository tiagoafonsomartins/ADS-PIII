import subprocess
query_result_temp = subprocess.check_output(['java', '-jar', 'SWRLAPIExample.jar', "3"])
print(query_result_temp)
query_result = []

for i in query_result_temp.decode("utf-8").split("Result:")[1].split("\n")[1:-1]:
    aux_clean_alg = i.split("\r")[0]
    clean_alg = aux_clean_alg.split(":")[1]
    query_result.append(clean_alg)

print(query_result)


