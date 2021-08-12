# coding:utf-8

import sys, os
import time
import datetime
from io import StringIO
import unittest
from xml.sax import saxutils

TestResult = unittest.TestResult

class _TestResult(TestResult):
    # note: _TestResult is a pure representation of results.
    # It lacks the output and reporting ability compares to unittest._TextTestResult.
    def __init__(self, verbosity=1):
        TestResult.__init__(self)
        self.stdout0 = None
        self.stderr0 = None
        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0
        self.verbosity = verbosity

        self.result = []
        # 增加一个测试通过率 --Findyou
        self.passrate = float(0)

    def startTest(self, test):
        TestResult.startTest(self, test)
        # just one buffer for both stdout and stderr
        self.outputBuffer = StringIO()
        stdout_redirector.fp = self.outputBuffer
        stderr_redirector.fp = self.outputBuffer
        self.stdout0 = sys.stdout
        self.stdout0 = sys.stdout
        sys.stdout = stdout_redirecctor
        sys.stderr = stderr_redirector


    def complete_output(self):
        '''
        Disconnect output redirection and return buffer.
        Safe to call multiple times.
        :return:
        '''
        if self.stdout0:
            sys.stdout = self.stdout0
            sys.stderr = self.stderr0
            self.stdout0 = None
            self.stderr0 = None
        return self.outputBuffer.getvalue()


    def stopTest(self, test):
        '''
        Usually one of addSuccess, addError or addFailure would have been called.
        But there are some path in unittest that would bypass this.
        We must disconnect stdout in stopTest(), which is guaranteed to be called.
        :param test:
        :return:
        '''
        self.complete_output()


    def addSuccess(self, test):
        self.success_count += 1
        TestResult.addSuccess(self, test)
        output = self.complete_output()
        self.result.append((0, test, output, ''))
        if self.verbosity > 1:
            sys.stderr.write('ok')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('.')

    def addError(self, test, err):
        self.error_count += 1
        TestResult.addError(self, test, err)
        _, _exc_str = self.errors[-1]
        output = self.complete_output()
        self.result.append((2, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('E ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('E')


    def addFailure(self, test, err):
        self.failure_count += 1
        TestResult.addFailure(self, test, err)
        _, _exc_str = self.failures[-1]
        output = self.complete_output()
        self.result.append((1, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('F   ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('F')


class HTMLTestRunner(Template_mixin):
    def __init__(self, stream=sys.stdout, verbosity=1, title=None, description=None, tester=None):
        self.stream = stream
        self.verbosity = verbosity
        if title is None:
            self.title = self.DEFAULT_TITLE
        else:
            self.title = title
        if description is None:
            self.description = self.DEFAULT_DESCRIPTION
        else:
            self.description = description
        if tester is None:
            self.tester = self.DEFAULT_TESTER
        else:
            self.tester = tester

        self.startTime = datetime.datetime.now()


    def run(self, test):
        '''
        Run the given test case or test suite.
        :param test:
        :return:
        '''
        result = _TestResult(self.verbosity)
        test(result)
        self.stopTime = datetime.datetime.now()
        self.generateReport(test, result)
        print(sys.stderr, '\nTime Elapsed: %s' % (self.stopTime - self.startTime))
        return result


    def sortResult(self, result_list):
        '''
        unittest does not seems to run in any particular order.
        Here at least we want to group them together by class.
        :param result_list:
        :return:
        '''
        rmap = {}
        classes = []
        for n, t, o, e in result_list:
            cls = t.__class__
            if not cls in rmap:
                rmap[cls] = []
                classes.append(cls)
            rmap[cls].append((n, t, o, e))
        r = [(cls, rmap[cls]) for cls in classes]
        return r

    # 替换测试结果为status为通过率
    def getReportAttributes(self, result):
        '''
        Return report attributes as a list of (name, value).
        Override this to add custom attributes.
        :param result:
        :return:
        '''
        startTime = str(self.startTime)[:19]
        duration = str(self.stopTime - self.startTime)
        status = []
        status.append('共 %s' % (result.success_count + result.failure_count +result.error_count))
        if result.success_count: status.append('通过 %s' % result.success_count)
        if result.failure_count: status.append('失败 %s' % result.failure_count)
        if result.error_count: status.append('错误 %s' % result.error_count)
        if status:
            status = ','.join(status)
            self.passrate = str("%.2f%%" %
                                (float(result.success_count) /
                                float(result.success_count + result.failure_count + result.error_count) * 100))
        else:
            status = 'none'
        return [
            (u'测试人员', self.tester),
            (u'开始时间', startTime),
            (u'合计耗时', duration),
            (u'测试结果', status + ",通过率= " + self.passrate),
        ]


    def generateReport(self, test, result):
        report_attrs = self.getReportAttributes(result)
        generator = 'HTMLTestRunner %s' % __version__
        stylesheet = self._generate_stylesheet()
        heading = self._generate_heading(report_attrs)
        report = self._generate_report(result)
        ending = self._generate_ending()
        output = self.HTML_TMPL % dict(
            tltle = saxutils.escape(self.title),
            generator = generator,
            stylesheet = stylesheet,
            heading = heading,
            report = report,
            ending = ending,
        )
        self.stream.write(output.encode('utf8'))


    def _generate_stylesheet(self):
        return self.STYLESHEET_TMPL

    # 增加Tester显示
    def _generate_heading(self, report_attrs):
        a_lines = []
        for name, value in report_attrs:
            line = self.HEADING_ATTRIBUTE_TMPL % dict(
                name = saxutils.escape(name),
                value = saxutils.escape(value),
            )
            a_lines.append(line)
        heading = self.HEADING_TMPL % dict(
            title = saxutils.escape(self.title),
            parameters = ''.join(a_lines),
            description = saxutils.escape(self.description),
            tester = saxutils.escape(self.tester),
        )
        return heading

    # 生成报告
    def _generate_report(self, result):
        rows = []
        sortedResult = self.sortResult(result.result)
        for cid, (cls, cls_results) in enumerate(sortedResult):
            # subtotal for a class
            np = nf = ne = 0
            for n, t, o, e in cls_results:
                if n == 0: np += 1
                elif n == 1: nf += 1
                else:
                    ne += 1

            # format class description
            if cls.__module__ == "__main__":
                name = cls.__name__
            else:
                name = "%s.%s" % (cls.__module__, cls.__name__)
            doc = cls.__doc__ and cls.__doc__.split("\n")[0] or ""
            desc = doc and '%s: %s' % (name, doc) or name

            row = self.REPORT_CLASS_TMPL % dict(
                style = ne > 0 and 'errorClass' or nf > 0 and 'failClass' or 'passClass',
                desc = desc,
                count = np + nf + ne,
                Pass = np,
                fail = nf,
                error = ne,
                cid = 'c%s' % (cid + 1),
            )
            rows.append(row)

            for tid, (n, t, o, e) in enumerate(cls_results):
                self._generate_report_test(rows, cid, tid, n, t, o, e)

        report = self.REPORT_TMPL % dict(
            test_list = ''.join(rows),
            count = str(result.success_count + result.failure_count + result.error_count),
            Pass = str(result.success_count),
            fail = str(result.failure_count),
            error = str(result.error_count),
            passrate = self.passrate,
        )
        return report


    def _generate_report_test(self, rows, cid, tid, n, t, o, e):
        has_output = bool(o or e)
        # ID修改点为下划线，支持Bootstrap折叠展开特效
        tid = (n == 0 and 'p' or 'f') + 't%s_%s' % (cid+1, tid+1)
        name = t.id().split('.')[-1]
        doc = t.shortDescription() or ""
        desc = doc and ('%s: %s' % (name, doc)) or name
        tmpl = has_output and self.REPORT_TEST_WITH_OUTPUT_TMPL or self.REPORT_TEST_NO_OUTPUT_TMPL

        # UTF-8 支持中文
        if isinstance(o, str):
            uo = o
        else:
            uo = o
        if isinstance(e, str):
            ue = e
        else:
            ue = e

        script = self.REPORT_TEST_OUTPUTTMPL % dict(
            id = tid,
            output = saxutils.escape(uo + ue),
        )
        # 插入图片
        unum = str(uo).rfind('screenshot:')
        if ((uo or ue) and unum != -1):
            hiddle_status = ''
            unum = str(uo).rfind('screenshot:')
            image_url = './Images/' + str(uo)[unum + 11:unum + 34].replace(' ','')
        else:
            hiddle_status = '''hidden="hidden"'''
            image_url = ''

        row = tmpl % dict(
            tid = tid,
            Class = (n == 0 and 'hiddenRow' or 'none'),
            style = n == 2 and 'errorCase' or (n ==1 and 'failCase' or 'passCase'),
            desc = desc,
            script = script,
            hidde = hiddle_status,
            image = image_url,
            status = self.STATUS[n],
        )
        rows.append(row)
        if not has_output:
            return


    def _generate_ending(self):
        return self.ENDING_TMPL


##############################################################################
# Facilities for running tests from the command line
##############################################################################

# Note:Reuse unittest.TestProgram to launch test.In the futrue we may
# build our own launcher to support more specific command line
# parameters like test title, CSS, etc.

class TestProgram(unittest.TestProgram):
    '''
    A variation of the unittest.TesrProgram.Please refer to the base
    class for command line parameters.
    '''
    def runTests(self):
        # Pick HTMLTestRunner as the default test runner.
        # base class's testRunner parameter is not useful because means
        # we have to instantiate HTMLTestRunner before we know self.verbosity.
        if self.testRunner is None:
            self.testRunner = HTMLTestRunner(verbosity=self.verbosity)
        unittest.TestProgram.runTests(self)

main = TestProgram

##############################################################################
# Executing this module from the command line
##############################################################################

if __name__ == "__main__":
    main(module=None)






































































































































































