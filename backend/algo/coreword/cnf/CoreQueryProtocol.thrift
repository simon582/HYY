//////// Request

struct CoreQueryRequest
{
    1:optional string qid,      // 请求id
    2:optional string data,     // 查询举例: '感冒发烧吃什么药'
}


//////// Response

struct CoreQueryResponse
{
	1:optional string qid,              // 请求id
	2:optional list<string> word_list    // 核心词list
}

service CoreQueryService {
	CoreQueryResponse GetCoreWords(1:CoreQueryRequest request)
}
