# corpus_compare

## 处理步骤
### 转换格式
* Input: 位于 data 目录下的 json line 格式的语料（多个）文件
* Output: data.conllx
* Script: convert_to_corpus.py
### 按照领域分组
* Input: data.conllx
* Output: 位于 domain_data 目录下文件名为领域名的（多个）文件
* Script: group_by_domain.py
### 比较数据
* Input: 
    * model/deliverable_model (模型数据)
    * 位于 domain_data 目录下文件名为领域名的（多个）文件
* Output: pickle 格式的 compare_result.pkl
* Script: compare_corpus.py
### 输出报告
输出报告的格式和内容，可以从 output_format 模块里找，也可以仿照已有接口实现自定义格式

* Input: pickle 格式的 compare_result.pkl
* Output: 位于 report 目录下文件名为领域名的（多个）文件
* Script: output_report.py
