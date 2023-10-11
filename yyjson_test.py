import time

from ct import ct_init
#from yyjson import yyjson_doc, yyjson_val, seq_yyjson_arr_size, seq_yyjson_doc_free
from yyjson import yyjson_doc, yyjson_val, seq_yyjson_arr_size, \
    seq_yyjson_arr_get_first, seq_yyjson_get_str, seq_unsafe_yyjson_get_next, \
    seq_yyjson_doc_free, seq_yyjson_read, seq_yyjson_doc_get_root, \
    seq_yyjson_doc_get_read_size, seq_yyjson_doc_get_val_count, seq_yyjson_obj_get, \
    seq_yyjson_get_type, seq_yyjson_get_type_desc, seq_yyjson_obj_iter_ptr_new, \
    seq_yyjson_obj_iter_next, seq_yyjson_obj_iter_get_val, \
    seq_yyjson_obj_iter_ptr_free, seq_yyjson_mut_doc_new, seq_yyjson_mut_obj, \
    seq_yyjson_mut_doc_set_root, seq_yyjson_mut_obj_add_str, \
    seq_yyjson_mut_obj_add_int, seq_yyjson_mut_write, seq_yyjson_mut_doc_free, \
    seq_yyjson_mut_obj_add_real, seq_yyjson_mut_obj_add_bool, yyjson_mut_doc


def test():
    s = '{"a1":"abc","b2":100}'
    doc = seq_yyjson_read(s.ptr, s.len, 0)
    if not doc:
        print('nil')
    print('doc: ', doc)
    root = seq_yyjson_doc_get_root(doc)
    print('root: ', root)
    
    doc_size = seq_yyjson_doc_get_read_size(doc)
    print('doc_size: ', doc_size)
    val_count = seq_yyjson_doc_get_val_count(doc)
    print('val_count: ', val_count)
    
    a_str = "a1"
    val = seq_yyjson_obj_get(root, a_str.ptr)
    
    obj_type = seq_yyjson_get_type(val)
    print('obj_type: ', obj_type)
    
    obj_type_str = seq_yyjson_get_type_desc(val)
    print('obj_type_str: ', str.from_ptr(obj_type_str))
    
    a = seq_yyjson_get_str(val)
    print('a: ', str.from_ptr(a))
    
    # seq_yyjson_obj_foreach_test(root)
    
    # yyjson_val *obj = yyjson_doc_get_root(doc);
    # yyjson_obj_iter iter;
    # yyjson_obj_iter_init(obj, &iter);
    # yyjson_val *key, *val;
    # while ((key = yyjson_obj_iter_next(&iter))) {
    #     val = yyjson_obj_iter_get_val(key);
    #     printf("%s: %s\n", yyjson_get_str(key), yyjson_get_type_desc(val));
    # }
    
    root_iter = seq_yyjson_obj_iter_ptr_new(root)
    _key = Ptr[yyjson_val]()
    _val = Ptr[yyjson_val]()
    while True:
        _key = seq_yyjson_obj_iter_next(root_iter)
        if not _key:
            break
        _val = seq_yyjson_obj_iter_get_val(_key)
        _val_type_desc = seq_yyjson_get_type_desc(_val)
        _key_str = seq_yyjson_get_str(_key)
        print('###', str.from_ptr(_key_str), str.from_ptr(_val_type_desc))
    print('333333')
    seq_yyjson_obj_iter_ptr_free(root_iter)
    print('333334')
    # 遍历
    
    # key: cobj
    # val: cobj
    # iter = seq_yyjson_obj_iter_with(root)
    # print('iter: ', iter, type(iter))
    # while True:
    #     key = seq_yyjson_obj_iter_next(iter)
    #     print('-----------')
    #     print('key: ', key)
    #     if not key:
    #         # print('not key')
    #         break
        
    #     key_type = seq_yyjson_get_type(key)
    #     print('key_type: ', key_type)
    #     if key_type == YYJSON_TYPE_STR:
    #         key_val = seq_yyjson_get_str(key)
    #         print('key: ', str.from_ptr(key_val))
    #     else:
    #         # key_val1 = seq_yyjson_get_raw(key)
    #         # print('key: ', str.from_ptr(key_val1))
    #         pass
        
    #     val = seq_yyjson_obj_iter_get_val(key)
    #     val_type = seq_yyjson_get_type(val)
        
    #     print('val_type: ', val_type)
    #     if val_type == YYJSON_TYPE_STR:
    #         val_str = seq_yyjson_get_str(val)
    #         print('value: ', str.from_ptr(val_str))
    #     elif val_type == YYJSON_TYPE_NUM:
    #         int_val = seq_yyjson_get_int(val)
    #         print('value: ', int_val)
    #     # key_str = seq_yyjson_get_str(key)
    #     # print(key, val)
    #     # print(key, val)
    #     # print(str.from_ptr(key_str))
    
    seq_yyjson_doc_free(doc)
    
    print('333335')
    
    # doc = yyjson_doc('{"a":1000,"b":"900000","c":15.6,"obj":{"a":1000000}}')
    s = '{"a":1000,"b":"900000","c":15.6}'
    doc = yyjson_doc(s)
    print('333336', doc)
    root = doc.root()
    print('333337')
    a = root["a"]
    print('a: ', a.int())
    b = root["b"]
    print('b: ', b.str())
    c = root["c"]
    print('c: ', c.float())
    
    obj = root["obj"]
    o1 = obj["a"]
    print('o1: ', o1, o1.int())
    
    doc.release()
    
    # 性能测试
    
    ret_str = '{"retCode":0,"retMsg":"OK","result":{"timeSecond":"1696143222","timeNano":"1696143222859435119"},"retExtInfo":{},"time":1696143222859}'
    
    num_runs = 1000000
    
    t0 = time.time()
    
    for _ in range(num_runs):
        doc = yyjson_doc(ret_str)
        root = doc.root()
        time_nano = root["result"]["timeNano"].str()
        # print('time_nano: ', time_nano)
        doc.release()
        
    t1 = time.time()
    print((t1 - t0) * 1e9 / num_runs)

def arr_test():
    # size_t idx, max;
    # yyjson_val *val;
    # yyjson_arr_foreach(arr, idx, max, val) {
    #     your_func(idx, val);
    # }
    
    # #define yyjson_arr_foreach	(	 	arr,
    #  	idx,
    #  	max,
    #  	val 
    # )		
    # Value:
    #     for ((idx) = 0, \
    #         (max) = yyjson_arr_size(arr), \
    #         (val) = yyjson_arr_get_first(arr); \
    #         (idx) < (max); \
    #         (idx)++, \
    #         (val) = unsafe_yyjson_get_next(val))
    # ret_str = '{"retCode":0,"retMsg":"OK","result":{"category":"linear","list":[{"symbol":"BTCUSDT","contractType":"LinearPerpetual","status":"Trading","baseCoin":"BTC","quoteCoin":"USDT","launchTime":"1585526400000","deliveryTime":"0","deliveryFeeRate":"","priceScale":"2","leverageFilter":{"minLeverage":"1","maxLeverage":"100.00","leverageStep":"0.01"},"priceFilter":{"minPrice":"0.10","maxPrice":"199999.80","tickSize":"0.10"},"lotSizeFilter":{"maxOrderQty":"100.000","minOrderQty":"0.001","qtyStep":"0.001","postOnlyMaxOrderQty":"1000.000"},"unifiedMarginTrade":true,"fundingInterval":480,"settleCoin":"USDT","copyTrading":"normalOnly"}],"nextPageCursor":""},"retExtInfo":{},"time":1696236288675}'
    ret_str = '{"retCode":0,"retMsg":"OK","result":{"category":"linear","list":["a1","a2"],"nextPageCursor":""},"retExtInfo":{},"time":1696236288675}'
    doc = yyjson_doc(ret_str)
    root = doc.root()
    result = root["result"]
    arr = result["list"]
    _idx: int
    _max: int
    _val = Ptr[yyjson_val]()
    _idx = 0
    _max = seq_yyjson_arr_size(arr.p)
    _val = seq_yyjson_arr_get_first(arr.p)
    print(_max)
    while _idx < _max:
        print('1111111112')
        # key_str = seq_yyjson_get_str(__ptr__(_idx))
        # print('key: ', str.from_ptr(key_str))
        val_str = seq_yyjson_get_str(_val)
        print('val: ', str.from_ptr(val_str))
        _idx += 1
        _val = seq_unsafe_yyjson_get_next(_val)
    # print('time_nano: ', time_nano)
    
    arr_list = arr.array_list()
    print(arr_list)
    for i in arr_list:
        print(i.str())
    doc.release()

def obj_list_test():
    ret_str = '{"retCode":0,"retMsg":"OK","result":{"category":"linear","list":["a1","a2"],"nextPageCursor":""},"retExtInfo":{},"time":1696236288675}'
    doc = yyjson_doc(ret_str, read_insitu=True)
    root = doc.root()
    result = root["result"]
    ol = result.obj_list()
    for i in ol:
        key = i[0].str()
        val_type_desc = i[1].type_desc()
        val = ""
        if val_type_desc == "string":
            val = i[1].str()
        elif val_type_desc == "array":
            arr = i[1].array_list()
            for j in arr:
                print(j.str())
        print(key, val, val_type_desc)
    doc.release()
    
def write_test():
    # // Create a mutable doc
    # yyjson_mut_doc *doc = yyjson_mut_doc_new(NULL);
    # yyjson_mut_val *root = yyjson_mut_obj(doc);
    # yyjson_mut_doc_set_root(doc, root);

    # // Set root["name"] and root["star"]
    # yyjson_mut_obj_add_str(doc, root, "name", "Mash");
    # yyjson_mut_obj_add_int(doc, root, "star", 4);

    # // Set root["hits"] with an array
    # int hits_arr[] = {2, 2, 1, 3};
    # yyjson_mut_val *hits = yyjson_mut_arr_with_sint32(doc, hits_arr, 4);
    # yyjson_mut_obj_add_val(doc, root, "hits", hits);

    # // To string, minified
    # const char *json = yyjson_mut_write(doc, 0, NULL);
    # if (json) {
    #     printf("json: %s\n", json); // {"name":"Mash","star":4,"hits":[2,2,1,3]}
    #     free((void *)json);
    # }

    # // Free the doc
    # yyjson_mut_doc_free(doc);
    print('1')
    pNULL = Ptr[byte]()
    print('2')
    doc = seq_yyjson_mut_doc_new(pNULL)
    print('3')
    root = seq_yyjson_mut_obj(doc)
    print('4')
    seq_yyjson_mut_doc_set_root(doc, root)
    print('5')
    
    name0 = "name"
    value0 = "Mash"
    seq_yyjson_mut_obj_add_str(doc, root, name0.ptr, value0.ptr)
    print('6')
    name1 = "star"
    seq_yyjson_mut_obj_add_int(doc, root, name1.ptr, 4)
    print('7')
    name2 = "real"
    seq_yyjson_mut_obj_add_real(doc, root, name2.ptr, 300.32)
    print('7.1')
    name3 = "bool1"
    seq_yyjson_mut_obj_add_bool(doc, root, name3.ptr, True)
    print('7.2')
    
    pLen = Ptr[int]()
    json_str = seq_yyjson_mut_write(doc, Int[32](0), pLen)
    print('8')
    print(str.from_ptr(json_str))
    
    seq_yyjson_mut_doc_free(doc)
    print('9')
    
    # from C import LIBRARY.seq_yyjson_mut_obj_add_null(cobj, cobj, cobj) -> bool
    # from C import LIBRARY.seq_yyjson_mut_obj_add_true(cobj, cobj, cobj) -> bool
    # from C import LIBRARY.seq_yyjson_mut_obj_add_bool(cobj, cobj, cobj, bool) -> bool
    # from C import LIBRARY.seq_yyjson_mut_obj_add_int(cobj, cobj, cobj, int) -> bool
    # from C import LIBRARY.seq_yyjson_mut_obj_add_real(cobj, cobj, cobj, float) -> bool
    # from C import LIBRARY.seq_yyjson_mut_obj_add_str(cobj, cobj, cobj, cobj) -> bool
    # from C import LIBRARY.seq_yyjson_mut_obj_add_strn(cobj, cobj, cobj, cobj, int) -> bool
    # from C import LIBRARY.seq_yyjson_mut_obj_add_strcpy(cobj, cobj, cobj, cobj) -> bool
    # from C import LIBRARY.seq_yyjson_mut_obj_add_strncpy(cobj, cobj, cobj, cobj, int) -> bool
    # from C import LIBRARY.seq_yyjson_mut_obj_add_arr(cobj, cobj, cobj) -> cobj
    # from C import LIBRARY.seq_yyjson_mut_obj_add_obj(cobj, cobj, cobj) -> cobj
    # from C import LIBRARY.seq_yyjson_mut_obj_add_val(cobj, cobj, cobj, cobj) -> bool
    
    
    

if __name__ == "__main__":
    ct_init()
    
    # 遍历数组
    # arr_test()
    
    # obj_list_test()
    # write_test()
    with yyjson_mut_doc() as doc:
        doc.add_str("abb", "ab")
        doc.add_int("i32", 13)
        doc.add_float("f", 1356.7)
        doc.add_bool("b", True)
        
        doc.arr_with_bool("arr_bool", [True, False, True, False])
        doc.arr_with_float("arr_float", [123.5,5151.51,15151.5])
        doc.arr_with_int("arr_int", [132,25,15])
        doc.arr_with_str("arr_str", ["abc","sdbb","abeew","bew","中文"])
        
        s = doc.mut_write()
        print(s)
        
    # test()
    
    print('OK')

    # 遍历    
    # yyjson_val *obj; // the object to be traversed
 
    # yyjson_val *key, *val;
    # yyjson_obj_iter iter = yyjson_obj_iter_with(obj);
    # while ((key = yyjson_obj_iter_next(&iter))) {
    #     val = yyjson_obj_iter_get_val(key);
    #     your_func(key, val);
    # }
