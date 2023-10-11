import time
import json


def test():
    ret_str = '{"retCode":0,"retMsg":"OK","result":{"timeSecond":"1696143222","timeNano":"1696143222859435119"},"retExtInfo":{},"time":1696143222859}'
    
    num_runs = 10
    
    t0 = time.time()
    
    for _ in range(num_runs):
        doc = json.loads(ret_str)
        # doc = yyjson_doc(ret_str)
        # root = doc.root()
        # time_nano = root["result"]["timeNano"].str()
        time_nano = doc["result"]["timeNano"]
        # print('time_nano: ', time_nano)
        # doc.release()
        
    t1 = time.time()
    print((t1 - t0) * 1e9 / num_runs)

    
if __name__ == "__main__":
    test()
