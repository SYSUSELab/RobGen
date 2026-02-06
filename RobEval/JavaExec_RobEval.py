import os
import shutil
import subprocess

from new_new_constsave import dictt_path
from new_new_constsave import project_name_path_dict
from new_new_constsave import dictt_comile_path
import numpy as np
import json




def read_generatedresult(filename,collection_dictt):
    with open(filename,
              'r',encoding="utf-8") as fr:
        list_tot_question = fr.readlines()
    print(len(list_tot_question))
    dictt_return = {}
    dict_level_tot = {}
    for i in range(0, len(list_tot_question)): ###对每个生成任务
        dictTemp = {}
        ques = json.loads(list_tot_question[i])

        content_doc = collection_dictt[ques['_id']] ###获取任务信息
        project_prefix = project_name_path_dict[content_doc["package"]]###project_name_path_dict 命名空间转化为路径前缀
        package = content_doc["package"]
        if package == "org.jgrapht.nio.dot":
            package = "org.jgrapht"
        package_path = package.replace(".", "/")
        file_name = content_doc["file_name"]
        file_path = project_prefix + "/" + package_path + "/" + file_name
        if content_doc is None:
            print(ques['question_id'])
            continue

        if "project" in content_doc.keys():
            dictTemp["project"] = content_doc["project"]
        dictTemp["name"] = content_doc["name"]
        dictTemp["file_name"] = content_doc["file_name"]
        dictTemp["package"] = content_doc["package"]
        dictTemp["docstring"] = content_doc["docstring"]
        dictTemp["_id"] = str(ques['_id'])
        dictTemp["lineno"] = content_doc["lineno"]
        dictTemp["end_lineno"] = str(content_doc['end_lineno'])
        solutions = ques["generate_results"]
        list_code = []
        for solution in solutions:
            list_code.append(solution)
        dictTemp['code'] = list_code
        level = content_doc["level"]
        dictTemp["level"] = level
        if level not in dict_level_tot.keys():
            dict_level_tot[level] = 1
        else:
            dict_level_tot[level] += 1
        dictt_return[file_path+"_"+content_doc["name"]+"_"+content_doc["lineno"]]=dictTemp
    return dict_level_tot,dictt_return
# file_input="C:/Users/yh199/Downloads/CoderEval-main1/CoderEval-main/experimental-results/Java/CodeGen/Raw-sample10.jsonl"
# file_input="Raw-sample10.jsonl"
if __name__ == "__main__":
    import sys
    file_input=sys.argv[1]
    n = int(sys.argv[2])
    fw = open(file_input+"_out_rob.jsonl", 'w')

    f = open("CoderEval4Java.json", 'r', encoding="utf-8")
    content = f.read()
    f.close()
    collection = []  ###项目信息列表
    collection_dictt = {} ###项目信息字典
    content_json = json.loads(content)
    for l in content_json['RECORDS']:
        collection.append(l)
        collection_dictt[l["_id"]] = l

    record_out = {}
    tot_k = []
    for i in range(0, n):
        tot_k.append(0.0)

    dict_level_tot,dictt_return_file_ques=read_generatedresult(file_input,collection_dictt)
    dict_level_tot_test,dictt_return_file_ques_test=read_generatedresult("RobEval.jsonl",collection_dictt)
    ######### dictt_return_file_ques ：打包好的任务信息，包括路径


    dictt_project={}
    for content in collection: ###将内容按仓库分类
        if content["package"] not in dictt_project.keys():
            dictt_project[content["package"]]=[content]
        else:
            dictt_project[content["package"]].append(content)
    count=0
    for l in project_name_path_dict.keys(): ###按仓库执行
        project_prefix=project_name_path_dict[l]
        excute_path = project_prefix
        for content in dictt_project[l]:
            package=content["package"]
            if package=="org.jgrapht.nio.dot":
                package="org.jgrapht"
            package_path = package.replace(".", "/")
            file_name = content["file_name"]
            os.chdir(project_prefix + "/" + package_path)
            file_path = project_prefix + "/" + package_path + "/" + file_name
            dict_out = {}

            

            if file_path+"_"+content["name"]+"_"+content["lineno"] in dictt_return_file_ques_test:
                all_data=dictt_return_file_ques_test[file_path+"_"+content["name"]+"_"+content["lineno"]]

                dictTemp = {}
                dictTemp = all_data
                temp_l = {}
                docstring = dictTemp['docstring']
                method_name = dictTemp['name']
                codes = dictTemp['code']
                code_level = dictTemp["level"]
                project_name = dictTemp["project"]
                start_line = dictTemp["lineno"]
                end_line = dictTemp["end_lineno"]
                
                ####backready的代码写到project内
                if os.path.exists(file_path.replace("CoderEval-Java-projects", "CoderEval-Java-projects-backready")):
                    f = open(file_path.replace("CoderEval-Java-projects", "CoderEval-Java-projects-backready"), 'r', encoding="utf-8")
                    content_code = f.read()
                    f.close()
                    ftemp = open(file_path, 'w', encoding="utf-8")
                    ftemp.write(content_code.replace("private ","public "))
                    ftemp.close()
                else:
                    if l == "io.protostuff":
                        file_path = file_path.replace("protostuff-api", "protostuff-core")
                        f = open(file_path.replace("CoderEval-Java-projects", "CoderEval-Java-projects-backready"), 'r', encoding="utf-8")
                        content_code = f.read()
                        f.close()
                        ftemp = open(file_path, 'w', encoding="utf-8")
                        ftemp.write(content_code.replace("private ","public "))
                        ftemp.close()
                        excute_path = excute_path.replace("protostuff-api", "protostuff-core")

                    else:
                        print("cannot find the file that contains the method under test!!!")
                        continue


                test_name = "test" + dictTemp["name"].lower()
                
                f_new_test_file = file_path.replace(".java", "_" + dictTemp["name"] + ".java")
                new_class_name = file_name.replace(".java", "_" + dictTemp["name"])
                test_path=f_new_test_file
                target_class_file = test_path.replace(".java", ".class").replace("/src/main/java/", "/target/classes/")
                if os.path.exists(target_class_file):
                    os.remove(target_class_file)
                for code in codes:
                    os.chdir(project_prefix + "/" + package_path)
                    new_class_file = test_path.replace(".java", ".class")
                    ftemp = open(test_path, 'w', encoding="utf-8")
                    ftemp.write(code)
                    ftemp.close()
                    if os.path.exists(new_class_file):
                        os.remove(new_class_file)
                    ###这段是进行编译生成class文件
                    compile_command=""
                    if file_path in dictt_comile_path.keys():
                        exec_command_lines=" ".join(dictt_comile_path[file_path].split(" ")[:-1]+[test_path.split("/")[-1]])
                        compile_command=exec_command_lines
                        sp = subprocess.Popen(
                            exec_command_lines,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, shell=True)
                        stdout, stderr = sp.communicate(timeout=60)
                    else:
                        exec_command_lines="javac -encoding utf8 -cp " + project_prefix + " " + test_path.split("/")[-1]
                        sp = subprocess.Popen(
                            exec_command_lines,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, shell=True)
                        stdout, stderr = sp.communicate(timeout=60)
                        compile_command="javac -encoding utf8 -cp " + project_prefix + " " + test_path.split("/")[-1]

                    if os.path.exists(new_class_file):
                        print("javac success!!!" + new_class_file)
                    else:
                        if l=="io.protostuff":
                            f_new_file_path=file_path.replace("protostuff-api","protostuff-core")

                            if os.path.exists(f_new_file_path):
                                os.chdir(project_prefix.replace("protostuff-api","protostuff-core") + "/" + package_path)
                                new_class_file = test_path.replace("protostuff-api","protostuff-core").replace(".java", ".class")
                                if os.path.exists(new_class_file):
                                    os.remove(new_class_file)
                                if f_new_file_path in dictt_comile_path.keys():
                                    exec_command_lines=" ".join(dictt_comile_path[f_new_file_path].split(" ")[:-1]+[test_path.split("/")[-1]])
                                    compile_command=exec_command_lines
                                    sp = subprocess.Popen(
                                        exec_command_lines,
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, shell=True)
                                    stdout, stderr = sp.communicate(timeout=60)
                                else:
                                    exec_command_lines="javac -encoding utf8 -cp " + project_prefix.replace("protostuff-api",
                                                                                                        "protostuff-core") + " " + test_path.split("/")[-1]
                                    sp = subprocess.Popen(
                                        exec_command_lines,
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, shell=True)
                                    compile_command="javac -encoding utf8 -cp " + project_prefix.replace("protostuff-api",
                                                                                                        "protostuff-core") + " " + test_path.split("/")[-1]
                                    stdout, stderr = sp.communicate(timeout=60)
                                if os.path.exists(new_class_file):
                                    print("javac success!!!" + new_class_file)
                                else:
                                    print("javac error!!!"+new_class_file)
                                    count+=1
                                    print("complie error count!",count)
                                    with open("/home/travis/builds/java/error.txt","+a") as f:
                                        f.write(dictTemp['_id'])
                                        f.write("\n")
                                        f.close()
                                    
                                    

                        else:
                            print("javac error!!!"+new_class_file)
                            count+=1
                            print("complie error count!",count)
                            with open("/home/travis/builds/java/error.txt","+a") as f:
                                f.write(dictTemp['_id'])
                                f.write("\n")
                                f.close()
                            
 
            
            if file_path+"_"+content["name"]+"_"+content["lineno"] not in dictt_return_file_ques:
                continue


            #####
            all_data=dictt_return_file_ques[file_path+"_"+content["name"]+"_"+content["lineno"]]
            dictTemp = {}
            dictTemp = all_data
            temp_l = {}
            docstring = dictTemp['docstring']
            method_name = dictTemp['name']
            codes = dictTemp['code']
            code_level = dictTemp["level"]
            project_name = dictTemp["project"]
            start_line = dictTemp["lineno"]
            end_line = dictTemp["end_lineno"]
            ####backready的代码写到project内
            if os.path.exists(file_path.replace("CoderEval-Java-projects", "CoderEval-Java-projects-backready")):
                f = open(file_path.replace("CoderEval-Java-projects", "CoderEval-Java-projects-backready"), 'r', encoding="utf-8")
                content_code = f.read()
                f.close()
                ftemp = open(file_path, 'w', encoding="utf-8")
                ftemp.write(content_code)
                ftemp.close()
            else:
                if l == "io.protostuff":
                    file_path = file_path.replace("protostuff-api", "protostuff-core")
                    f = open(file_path.replace("CoderEval-Java-projects", "CoderEval-Java-projects-backready"), 'r', encoding="utf-8")
                    content_code = f.read()
                    f.close()
                    ftemp = open(file_path, 'w', encoding="utf-8")
                    ftemp.write(content_code)
                    ftemp.close()
                    excute_path = excute_path.replace("protostuff-api", "protostuff-core")

                else:
                    print("cannot find the file that contains the method under test!!!")
                    continue

            test_name = "test" + dictTemp["name"].lower()
            
            f_new_test_file = file_path.replace(".java", "_" + dictTemp["name"] + ".java")
            new_class_name = file_name.replace(".java", "_" + dictTemp["name"])


            content_code_list = content_code.split("\n")
            tempsss = ""
            try:
                for i in range(int(start_line) - 1, int(end_line)):
                    tempsss += content_code_list[i]
                    tempsss += "\n"
                if content_code.find(tempsss) < 0:
                    continue
            except:
                print("replace finding error:" + str(content["_id"]))

 
            ### 去除旧编译后文件
            new_class_file = file_path.replace(".java", ".class")
            if os.path.exists(new_class_file):
                os.remove(new_class_file)
            

            c = 0
            code_num = 0
            list_generate_code = []
            for code in codes:
                os.chdir(project_prefix + "/" + package_path)
                dict_temp = {}
                dict_temp["generate_code"] = code
                dict_temp["errormessage"] = ""
                dict_temp["error_detail_message"] = ""
                dict_temp["is_pass"] = False
                code_num += 1
                new_class_file = file_path.replace(".java", ".class")
                target_class_file = new_class_file.replace("/src/main/java/", "/target/classes/")
                ftemp = open(file_path, 'w', encoding="utf-8")
                ftemp.write(content_code.replace(tempsss, code).replace("private ","public "))
                ftemp.close()
                if os.path.exists(new_class_file):
                    os.remove(new_class_file)
                ###这段是进行编译生成class文件
                if file_path in dictt_comile_path.keys():
                    sp = subprocess.Popen(
                        dictt_comile_path[file_path],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE, shell=True)
                    stdout, stderr = sp.communicate(timeout=60)
                else:
                    sp = subprocess.Popen(
                        "javac -encoding utf8 -cp " + project_prefix + " " + file_name,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE, shell=True)
                    stdout, stderr = sp.communicate(timeout=60)

                if os.path.exists(new_class_file):
                    print("javac success!!!" + new_class_file)
                else:
                    if l=="io.protostuff":
                        f_new_file_path=file_path.replace("protostuff-api","protostuff-core")

                        if os.path.exists(f_new_file_path):
                            # exist += 1
                            os.chdir(project_prefix.replace("protostuff-api","protostuff-core") + "/" + package_path)
                            new_class_file = file_path.replace("protostuff-api","protostuff-core").replace(".java", ".class")
                            # if os.path.exists(new_class_file):
                            #     os.remove(new_class_file)
                            if f_new_file_path in dictt_comile_path.keys():

                                sp = subprocess.Popen(
                                    dictt_comile_path[f_new_file_path],
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE, shell=True)
                                stdout, stderr = sp.communicate(timeout=60)
                            else:
                                sp = subprocess.Popen(
                                    "javac -encoding utf8 -cp " + project_prefix.replace("protostuff-api",
                                                                                                    "protostuff-core") + " " + file_name,
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE, shell=True)
                                stdout, stderr = sp.communicate(timeout=60)

                            if not os.path.exists(new_class_file):
                                ftemp = open(file_path, 'w', encoding="utf-8")
                                ftemp.write(content_code)
                                ftemp.close()
                                list_generate_code.append(dict_temp)
                                dict_temp["errormessage"]="compile error"
                                if stderr is None:
                                    dict_temp["error_detail_message"] = "null"
                                else:
                                    dict_temp["error_detail_message"] = bytes.decode(stderr, encoding="gbk")
                                # continue
                    else:
                        ftemp = open(file_path, 'w', encoding="utf-8")
                        ftemp.write(content_code)
                        ftemp.close()
                        list_generate_code.append(dict_temp)
                        dict_temp["errormessage"] = "compile error"
                        if stderr is None:
                            dict_temp["error_detail_message"] = "null"
                        else:
                            dict_temp["error_detail_message"] = bytes.decode(stderr, encoding="gbk")
                        # continue

                ### 执行测试的逻辑
                f_new_test_file = file_path.replace(".java", "_" + content["name"] + ".class").replace("/src/main/java","/target/classes")
                if os.path.exists(f_new_test_file.replace("/target/classes","/src/main/java")) and os.path.exists(new_class_file):
                    listt_copyfile=[]
                    listt_copyfile.append(new_class_file)
                    dir_tosearch=new_class_file.rstrip(new_class_file.split("/")[-1])
                    class_name=new_class_file.split("/")[-1].rstrip(".class")
                    if class_name=="IndexStructure":
                        class_name+="s"
                    for temp_file in os.listdir(dir_tosearch):
                        if temp_file.startswith(class_name+"$") and temp_file.endswith(".class"):
                            listt_copyfile.append(dir_tosearch+temp_file)
                    for temp_class in listt_copyfile:
                        if os.path.exists(temp_class.replace("/src/main/java/", "/target/classes/")):
                            os.remove(temp_class.replace("/src/main/java/", "/target/classes/"))
                    for temp_target in listt_copyfile:
                        shutil.copyfile(temp_target, temp_target.replace("/src/main/java/", "/target/classes/"))
                    test_path=""
                    os.chdir(excute_path)
                    if f_new_test_file in dictt_path.keys():
                        sp = subprocess.Popen(
                            dictt_path[f_new_test_file],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, shell=True)
                        test_path=f_new_test_file
                        try:
                            stdout, stderr = sp.communicate(timeout=60)
                            strt = bytes.decode(stdout, encoding="gbk")
                            print(strt)
                        except:
                            ftemp = open(file_path, 'w', encoding="utf-8")
                            ftemp.write(content_code)
                            ftemp.close()
                            list_generate_code.append(dict_temp)
                            continue
                        
                        if strt.find("true") >= 0 and strt.find("false") < 0:
                            c += 1
                            dict_temp["is_pass"] = True
                        else:
                            dict_temp["errormessage"] = "exec error!"
                            if stderr is None:
                                dict_temp["error_detail_message"] = "null"
                            else:
                                dict_temp["error_detail_message"] = bytes.decode(stderr, encoding="gbk")
                            list_generate_code.append(dict_temp)
                            ftemp = open(file_path, 'w', encoding="utf-8")
                            ftemp.write(content_code)
                            ftemp.close()
                            continue
                    else:
                        if target_class_file.find("protostuff-api"):
                            excute_path=excute_path.replace("protostuff-core", "protostuff-api")

                        os.chdir(excute_path)
                        if package == "":
                            sp = subprocess.Popen(
                                "java " + f_new_test_file.removesuffix(".class").split("/")[-1],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, shell=True)
                            test_path=excute_path+f_new_test_file.removesuffix(".class").split("/")[-1]+".class"
                        else:
                            sp = subprocess.Popen(
                                "java " + package + "." + f_new_test_file.removesuffix(".class").split("/")[-1],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, shell=True)
                            test_path=excute_path+"/"+package.replace(".","/")+"/"+f_new_test_file.removesuffix(".class").split("/")[-1]+".class"
                        try:
                            stdout, stderr = sp.communicate(timeout=60)
                            strt = bytes.decode(stdout, encoding="gbk")
                            print(strt)
                        except:
                            list_generate_code.append(dict_temp)
                            ftemp = open(file_path, 'w', encoding="utf-8")
                            ftemp.write(content_code)
                            ftemp.close()
                            dict_temp["errormessage"] = "exec error!"
                            if stderr is None:
                                dict_temp["error_detail_message"] = "null"
                            else:
                                dict_temp["error_detail_message"] = bytes.decode(stderr, encoding="gbk")
                            continue
                        if strt.find("true") >= 0 and strt.find("false") < 0:
                            c += 1
                            dict_temp["is_pass"] = True
                        else:
                            dict_temp["errormessage"] = "exec error!"
                            if stderr is None:
                                dict_temp["error_detail_message"] = "null"
                            else:
                                dict_temp["error_detail_message"] = bytes.decode(stderr, encoding="gbk")
                            list_generate_code.append(dict_temp)
                            ftemp = open(file_path, 'w', encoding="utf-8")
                            ftemp.write(content_code)
                            ftemp.close()
                            continue

                list_generate_code.append(dict_temp)
                ftemp = open(file_path, 'w', encoding="utf-8")
                ftemp.write(content_code)
                ftemp.close()
            if code_level not in record_out.keys():
                temp_tot_k = []
                for tti in range(0, n):
                    temp_tot_k.append(0.0)
            else:
                temp_tot_k = record_out[code_level]
            for k in range(1, n + 1):
                if n - c < k:
                    tot_k[k - 1] += 1.0
                    temp_tot_k[k - 1] += 1.0
                else:
                    tot_k[k - 1] += (1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1)))
                    temp_tot_k[k - 1] += (1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1)))
                # print(dictTemp["_id"], n, c, tot_k[k - 1])
            record_out[code_level] = temp_tot_k
            dict_out["generate_results"] = list_generate_code
            dict_out["docstring"] = dictTemp['docstring']
            dict_out["method_name"] = dictTemp['name']
            dict_out["codes"] = dictTemp['code']
            dict_out["code_level"] = dictTemp["level"]
            dict_out["_id"] = dictTemp["_id"]
            dict_out["project_name"] = dictTemp["project"]
            # dict_out["test_file"]=f_new_test_file
            # dict_out["test_file_java"]=f_new_test_file.replace("/target/classes","/src/main/java").replace(".class",".java")
            # with open(f_new_test_file.replace("/target/classes","/src/main/java").replace(".class",".java"),"r") as f:
            #     test_code=f.read()
            #     # print(test_code)
            #     dict_out["test_file_java_code"]=test_code
            fw.write(json.dumps(dict_out) + "\n")
            fw.flush()
    print(tot_k)
    for tt in tot_k:
        print(tt * 1.0 / 230)
        print("% .2f" % (tt * 1.0 / 230 * 100) + "%")
    print("finish_overall")
    for key_temp in record_out.keys():
        tot_k_1 = record_out[key_temp]
        num_temp = dict_level_tot[key_temp]
        print(key_temp + "\t" + str(num_temp) + "\n")
        for tt in tot_k_1:
            print(" % .2f" % (tt * 1.0 / num_temp * 100) + "%\t")
        print("\n")









