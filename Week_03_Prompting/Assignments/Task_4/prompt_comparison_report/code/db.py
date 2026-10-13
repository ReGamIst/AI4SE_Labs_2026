import sys; sys.argv=['x']
import importlib.util
spec=importlib.util.spec_from_file_location('ev','evaluate_retrieval_predictions.py'); ev=importlib.util.module_from_spec(spec); spec.loader.exec_module(ev)
def conn(): return ev.load_database()
