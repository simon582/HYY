//////// Request

struct HyySearchRequest
{
    1:optional string qid,      // 请求id
    2:optional string data,     // 查询举例: 'cat=123' or 'query=胃病'
}


//////// Response
/*
    正文格式:
    <p>段落1</p>
    <img src="aaa.jpg"/>
    <p>段落2</p>
*/

struct HyyDoc
{
    1:optional string doc_id,       // 文档id
    2:optional string title,        // 标题
    3:optional string author,       // 作者
    4:optional string datetime,     // 时间YYYY-mm-dd HH:MM:SS
    5:optional string source,       // 来源
    6:optional string text,         // 正文
    7:optional string source_icon,  // 来源icon
    8:optional string source_desc,  // 来源描述
}

struct HyySearchResponse
{
	1:optional string qid,              // 请求id
	2:optional list<HyyDoc> doc_list    // 查询结果list
}

service HyySearchService {
	HyySearchResponse GetSearchResult(1:HyySearchRequest request)
}
