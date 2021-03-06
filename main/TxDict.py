import urllib.request
import json


class TxDict:
    def __init__(self, apikey, wordlst):
        self.apikey = apikey
        self.wordlst = wordlst  # 待生成中文释义的单词列表
        self.url = 'http://api.tianapi.com/txapi/enwords/index?key=' + self.apikey + '&word='
        self.result = {}  # 生成数据的结果 {'word':'definition'}
        self.error_rprt = []
        self.error_info = {
            100: ['内部服务器错误', '出现此错误码请及时反馈或等待修复'],
            110: ['接口暂时维护中', '接口暂时关闭维护中，请注意相关公告'],
            120: ['IP请求来源受限', '设置了IP白名单，来源IP不在白名单内'],
            130: ['分钟请求频率超限', 'API超出了分钟调用最大频率被暂时限制'],
            140: ['API没有调用权限', '请检查接口是否被自行停用或被官方禁用'],
            150: ['接口可用次数不足', '接口可用次数不足，请在接口列表查看'],
            160: ['账号未申请该接口', '请先在对应的接口文档页面申请接口'],
            170: ['Referer请求来源受限', '设置了Referer白名单，来源Referer不在白名单内'],
            230: ['key错误或为空', '请检查apikey是否填写错误'],
            240: ['缺少key参数', '请检查是否传递了key参数，如变量请检查是否赋值'],
            250: ['数据返回为空', '数据查询或转换失败，请确保输入值正确或重试'],
            260: ['关键词不得为空', '请检查word参数是否传递了空值'],
            270: ['缺少有效数据', '接口需要传递数据，请参考接口文档的说明'],
            280: ['缺少必要的参数', '缺少必填的参数，请根据接口文档检查'],
            290: ['超过最大输入字节限制', '超出最大字符，请查看对应的接口文档说明']
        }

    def show_error_report(self):
        # 列出查询失败的单词 如果有
        if self.error_rprt:
            print("[!] 以下单词" + self.error_info[250][1])
            for e in self.error_rprt:
                print('[→] ' + e)

    def generate_error_info(self, resp, word):
        if resp['code'] == 250:  # 非严重错误
            self.result[word] = 'Error250'  # 为查询释义失败的单词添加失败标志
            self.error_rprt.append(word)  # 添加至错误报告 提示出现错误↓ 无返回值
            print('[!]', str((self.wordlst.index(word)) + 1) + '/' + str(len(self.wordlst)), word, 'Error-250')
        else:  # 严重的错误 无法继续进行其他单词释义查询
            print('[×]', str((self.wordlst.index(word)) + 1) + '/' + str(len(self.wordlst)),
                  word, resp['msg'] + ' ' + self.error_info[resp['code']][1])
            return True  # 显示终止时的进度 单词 错误信息 并返回True

    def get_definition(self):
        for word in self.wordlst:
            resp = json.loads(urllib.request.urlopen(self.url + word).read().decode())
            if 'newslist' in resp:  # newslist键在api反馈中表示操作成功
                self.result[word] = resp['newslist'][0]['content'].split('|')  # 储存结果 显示进度↓
                print('[√]', str((self.wordlst.index(word)) + 1) + '/' + str(len(self.wordlst)), word)
            else:
                if self.generate_error_info(resp, word):  # 有返回值代表严重错误 无返回值代表错误不影响主程序运行
                    break  # 无法继续使用API 停止生成释义

        return self.result


'''
td = TxDict('1dec8cb373f09df013042e4d5e8c21ef', ['cookie', 'need', 'fuck'])
td.get_definition()
print(td.result)

{'code': 250, 'msg': '数据返回为空'}
{'code': 230, 'msg': 'key错误或为空'}
{'code': 200, 'msg': 'success', 'newslist': [{'word': 'hello', 'content': 'i:喂,欸,你好,哎|v:你好'}]}

word = 'ssafddsaf'
APIKEY = '1dec8cb373f09df013042e4d5e8c21ef'
url = 'http://api.tianapi.com/txapi/enwords/index?key=' + APIKEY + '&word=' + word

resp = urllib.request.urlopen(url)
content = resp.read()
if content:
    content = json.loads(content.decode())
    print(content)
    print(type(content))
    print("错误代码：", content['code'])
    print("信息：", content['msg'])
    print("搜索词：", content['newslist'][0]['word'])
    print("内容：", content['newslist'][0]['content'])
'''
