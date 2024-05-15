from requests_html import HTMLSession
import re
import csv

session = HTMLSession()

urls = [
    'http://www.moe.gov.cn/jyb_sjzl/moe_560/2022/quanguo/202401/t20240110_1099539.html',
    # 可以在这里添加更多网址
]

# 定义正则表达式模式
pattern_main = re.compile(r"1\.研究生\sPostgraduates.*?本\s科\sNormal\sCourses", re.DOTALL)
pattern_detail = re.compile(r"""
    1\.研究生\sPostgraduates\n
    (?P<graduates_pg>\d+)\n
    (?P<entrants_pg>\d+)\n
    (?P<enrolment_pg>\d+)\n
    博\s士\sDoctor´s\sDegree\n
    (?P<graduates_phd>\d+)\n
    (?P<entrants_phd>\d+)\n
    (?P<enrolment_phd>\d+)\n
    硕\s士\sMaster´s\sDegree\n
    (?P<graduates_masters>\d+)\n
    (?P<entrants_masters>\d+)\n
    (?P<enrolment_masters>\d+)\n
    2\.普通本科\sUndergraduates\n
    (?P<graduates_ug>\d+)\n
    (?P<entrants_ug>\d+)\n
    (?P<enrolment_ug>\d+)\n
    3\.职业本专科\sVocational\sUndergraduate\n
    (?P<graduates_voc>\d+)\n
    (?P<entrants_voc>\d+)\n
    (?P<enrolment_voc>\d+)
""", re.VERBOSE)

# 遍历每个网址
for i, url in enumerate(urls, start=1):
    try:
        r = session.get(url)
        r.raise_for_status()  # 检查请求是否成功

        # 获取页面文本内容
        page_text = r.html.text

        # 查找主模式匹配
        main_match = pattern_main.search(page_text)

        if main_match:
            extracted_text = main_match.group(0)

            # 查找详细模式匹配
            detail_match = pattern_detail.search(extracted_text)

            if detail_match:
                data = {
                    "Postgraduates": [
                        detail_match.group("graduates_pg"),
                        detail_match.group("entrants_pg"),
                        detail_match.group("enrolment_pg")
                    ],
                    "PhD": [
                        detail_match.group("graduates_phd"),
                        detail_match.group("entrants_phd"),
                        detail_match.group("enrolment_phd")
                    ],
                    "Master's": [
                        detail_match.group("graduates_masters"),
                        detail_match.group("entrants_masters"),
                        detail_match.group("enrolment_masters")
                    ],
                    "Undergraduates": [
                        detail_match.group("graduates_ug"),
                        detail_match.group("entrants_ug"),
                        detail_match.group("enrolment_ug")
                    ],
                    "Vocational": [
                        detail_match.group("graduates_voc"),
                        detail_match.group("entrants_voc"),
                        detail_match.group("enrolment_voc")
                    ]
                }

                # 使用网址索引生成唯一的文件名
                output_filename = f'output_{i}.csv'

                # 将数据写入 CSV 文件
                with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Category", "Graduates", "Entrants", "Enrolment"])
                    for category, numbers in data.items():
                        writer.writerow([category] + numbers)

                print(f"数据已保存到 {output_filename} 文件中 for URL {url}")
            else:
                print(f"详细模式未匹配: {url}")
        else:
            print(f"主模式未匹配: {url}")
    except Exception as e:
        print(f"处理URL时出错: {url}, 错误: {e}")

