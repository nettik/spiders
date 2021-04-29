import re


class Tool:
    tbody_pattern = re.compile("<tbody>(.*?)</tbody>", re.DOTALL)
    tr_pattern = re.compile("<tr>(.*?)</tr>", re.DOTALL)
    td_pattern = re.compile("<td.*?>(.*?)</td>")
    title_pattern = re.compile("<a.*?>(.*?)</a>")
    year_pattern = re.compile("(\d{4})")
