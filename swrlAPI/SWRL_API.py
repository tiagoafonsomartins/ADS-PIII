import os
import subprocess


def query_result(number_of_metrics: int):
    query_result_temp = subprocess.run(
        ['java', '-jar', 'swrlAPI\\SWRLAPIExample.jar', str(number_of_metrics), 'swrlAPI\\ADS.owl'],
        universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    query_result = []
    for i in query_result_temp.stdout.split("Result:")[1].split("\n")[1:-1]:
        aux_clean_alg = i.split("\r")[0]
        clean_alg = aux_clean_alg.split(":")[1]
        query_result.append(clean_alg)
    return query_result
