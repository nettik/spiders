import re


class Tool:
    novel_data_pattern = re.compile('<div class="data-txt">.*?<div class="col-b">', re.DOTALL)
    book_name_pattern = re.compile('<h2 class="tit">(.*?)</h2>')
    author_pattern = re.compile('<em>作者：</em><a.*?>(.*?)</a>', re.DOTALL)
    rank_pattern = re.compile('<strong>(.*?)</strong>分')
    state_pattern = re.compile('<em class="(orange|green)">(.*?)</em>')
    book_type_pattern = re.compile('<a href="/shuku/.*?/">(.*?)</a>')
    leading_role_pattern = re.compile('<em>主角：</em>(.*[&nbsp;]{3})', re.DOTALL)
    span_pattern = re.compile('<span><em>(.*?)</em>(.*?)</span>')
    introduction_pattern = re.compile('<div class="article">(.*?)</div>', re.DOTALL)
