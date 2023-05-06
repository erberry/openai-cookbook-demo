from gensim.models import KeyedVectors
import time


# 加载文本模型
print("begin load txt")
start_time = time.time()
wv_model = KeyedVectors.load_word2vec_format('model/tencent-ailab-embedding-zh-d200-v0.2.0-s.txt', binary=False)
end_time = time.time()
run_time = end_time - start_time
print("end load txt：{:.2f}秒".format(run_time))

# 将模型保存为二进制格式
print("begin save bin")
start_time = time.time()
wv_model.save_word2vec_format('model/tencent-ailab-embedding-zh-d200-v0.2.0-s.bin', binary=True)
end_time = time.time()
run_time = end_time - start_time
print("end save bin{:.2f}秒".format(run_time))

# 验证二机制文件是否正常
print("begin load bin")
start_time = time.time()
wv_model = KeyedVectors.load_word2vec_format('model/tencent-ailab-embedding-zh-d200-v0.2.0-s.bin', binary=True)
end_time = time.time()
run_time = end_time - start_time
print("end load bin:{:.2f}秒".format(run_time))