# 开发实录
D0：为什么今晚用原生SDK手搓而不用LangChain；

先保证链路没有问题，明天换langchain，保证整体项目真实且能过面试。

D1：去重为什么跨调用保留、它明天怎么演化为缓存层。

不太知道……

D2：arxiv换源

D3（function calling承载ReAct）、

D4（Agent自纠）

D5（护栏）

# 踩坑

API-Key泄露：哥们儿真不知道有这回事！Github连夜给我发邮件！

arXiv 406：我差点以为项目彻底完蛋了，还好有AI大人帮我！是因为检索词不行。然后还有一点是
请求的Header头也不行，需要加上自己的User-Agent和联系方式。

S2/OpenAlex共享IP限流→备选记录；

Crossref JATS标签→正则剥离。


