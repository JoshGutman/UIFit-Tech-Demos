from django import forms

def make_config(post_dict):
    path_names = ["output_dir", "bng_command", "model", "exp_file"]
    general_names = ["job_name", "use_cluster", "cluster_parallel", "max_walltime"]
    fitting_names = ["max_generations", "permutations", "obj_func", "smoothing", "keep_parents", "mutate"]

    free_names = set()


    path_str = """############# 
### PATHS ### 
#############
"""

    general_str = """
####################### 
### General Options ### 
####################### 
"""

    fitting_str = """
####################### 
### Fitting Options ### 
####################### 
"""

    free_str = """

# Generate free parameters
"""


    for key in post_dict:
        print(key)
        if key in path_names:
            path_str += "{} = {}\n".format(key, post_dict[key])
        elif key in general_names:
            general_str += "{} = {}\n".format(key, post_dict[key])
        elif key in fitting_names:
            fitting_str += "{} = {}\n".format(key, post_dict[key])
        elif "csrfmiddlewaretoken" in key:
            pass
        else:
            free_names.add(key.split("_")[0])

    for name in free_names:
        lower = name + "_lower"
        upper = name + "_upper"
        free_str += "loguniform_var={}\t{}\t{}\n".format(name, post_dict[lower], post_dict[upper])
        
    


    return path_str + general_str + fitting_str + free_str

    
        


def interpret_bngl(file):
    contents = read_bngl(file)
    free_parameters = get_free_parameters(contents)
    free_fields = make_free_fields(free_parameters)

    path_names = ["output_dir", "bng_command", "model", "exp_file"]
    general_names = ["job_name", "use_cluster", "cluster_parallel", "max_walltime"]
    fitting_names = ["max_generations", "permutations", "obj_func", "smoothing", "keep_parents", "mutate"]

    path_fields = make_other_fields(path_names)
    general_fields = make_other_fields(general_names)
    fitting_fields = make_other_fields(fitting_names)

    return make_dict(free_fields, path_fields, general_fields, fitting_fields)


def read_bngl(file):
    with open(file, "rU") as infile:
        return infile.readlines()

def get_free_parameters(contents):
    out = []
    for line in contents:
        if "__FREE__" in line:
            out.append(line.strip().split()[0])
    return out


def make_free_fields(parameters):
    out = []
    for p in parameters:
        out.append(FreeOption(p))
    return out


def make_other_fields(names):
    out = []
    for name in names:
        #out.append(forms.CharField(label=name))
        out.append(Option(name))
    return out


def make_dict(free, path, general, fitting):
    return {"free": free,
            "path": path,
            "general": general,
            "fitting": fitting}

class Option:
    def __init__(self, name, width=25):
        self.label = '<label for="{}">{}</label>'.format(name, name.split("_")[0])
        self.field = '<input type="text" id="{}" name="{}" size="{}">'.format(name, name, width)


class FreeOption:
    def __init__(self, name):
        self.lower = Option(name + "_lower", 7)
        self.upper = '<input type="text" name="{}_upper" id="{}_upper" size="7">'.format(name, name)


if __name__ == "__main__":
    import sys
    c = read_bngl(sys.argv[1])
    print(get_free_parameters(c))
