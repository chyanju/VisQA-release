import requests
import pickle
import urllib.parse
import time
import json

def extract_subid(full_id):
	# kong and d3 have different ids here and actual files, need to replace
	return full_id.replace("kong_","").replace("d3_","")

app = "http://localhost:5000/query-vis-sempre"
with open("./dataset/qadata.json","r") as f:
	qadata = json.load(f)
with open("./dataset/chart-list.json","r") as f:
	chart_list = json.load(f)
chart_dict = {p["name"]:(p["dataset"],p["filename"]) for p in chart_list}

cnt_correct = 0
collected_data = []
skipped_keys = []
key_list = list(qadata.keys())
for i in range(len(key_list)):
	dkey = key_list[i]

	time.sleep(3)
	print("# ============ correct: {}, successful: {}, skipped: {} ============ #".format(cnt_correct, len(collected_data), len(skipped_keys)))
	print("# fetching {}/{}: {}".format(i, len(key_list), dkey))
	# ddataset = qadata[dkey]["dataset"]
	# dspecfile = extract_subid(qadata[dkey]["chartName"])+".json"
	# druntimefile = extract_subid(qadata[dkey]["chartName"])+".csv"
	ddataset, dspecfile = chart_dict[qadata[dkey]["chartName"]]
	druntimefile = dspecfile.replace(".json",".csv")
	dquery = qadata[dkey]["question"]
	danswer = qadata[dkey]["answer"]
	print("  # dataset: {}".format(ddataset))
	print("  # specFile: {}".format(dspecfile))
	print("  # runtimeFile: {}".format(druntimefile))
	print("  # query: {}".format(dquery))
	print("  # answer: {}".format(danswer))
	durl = "{}?questionId={}&dataset={}&specFile={}&runtimeFile={}&query={}&answer={}".format(
		app, dkey, ddataset, dspecfile, druntimefile, 
		urllib.parse.quote(dquery), urllib.parse.quote(danswer),
	)
	print("  # url: {}".format(durl))
	r = requests.get(durl)
	if r.status_code==200:
		pass
	else:
		skipped_keys.append(dkey)
		print("Failed. Skip.")
		continue

	# compare solution
	dentry = r.json()
	dcorrect = dentry["targetAnswer"] == dentry["systemAnswer"]
	print("  # correct: {}".format(dcorrect))
	dentry["correct"] = dcorrect
	if dcorrect:
		cnt_correct += 1
	collected_data.append(dentry)

	with open("./analysis.pkl", "wb") as f:
		pickle.dump({"data":collected_data, "skipped_keys": skipped_keys}, f)



