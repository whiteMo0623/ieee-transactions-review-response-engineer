"""Isolated regression checks for initialization and the lightweight artifact contract."""
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m
A = load('audit_review_case')
I = load('init_review_case')


def docx(path, text='before', marker='before'):
    path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(path, 'w', ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"/>')
        z.writestr('word/document.xml', '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p><w:r><w:t>' + text + '</w:t></w:r></w:p></w:body></w:document>')
        z.writestr('docProps/core.xml', '<metadata>' + marker + '</metadata>')


class CaseTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.case = self.root / 'cases' / 'R2-C4'
        self.case.mkdir(parents=True)
        self.word = self.root / 'response.docx'
        docx(self.word, 'after')
        docx(self.root / 'response.before-R2-C4.docx')
        self.fields = dict(comment_id='R2-C4', experiment_required=False,
                           code_files=[], result_files=[], approved_artifacts={}, word_file=str(self.word))
        self.sections = {h:'Verified or not applicable: this case uses existing evidence.' for h in A.REQUIRED_HEADINGS}
        self.write_plan()

    def write_plan(self):
        text = '---\n' + '\n'.join(k + ': ' + json.dumps(v) for k,v in self.fields.items()) + '\n---\n\n'
        text += '\n\n'.join(h+'\n\n'+v for h,v in self.sections.items())
        (self.case/'response-plan.md').write_text(text)

    def errors(self):
        self.write_plan()
        return A.audit(self.case)

    def test_valid_case(self):
        self.assertEqual(self.errors(), [])

    def test_missing_word_and_empty_sections_fail(self):
        self.fields['word_file'] = None
        self.sections = {h:'<!-- completed? -->' for h in A.REQUIRED_HEADINGS}
        errors=self.errors()
        self.assertTrue(any('word_file' in e for e in errors))
        self.assertEqual(sum('Empty section' in e for e in errors), 6)

    def test_author_placeholder_but_not_quoted_review_todo(self):
        self.sections[A.REQUIRED_HEADINGS[0]]='> Please clarify the TODO marker in the code.'
        self.assertEqual(self.errors(), [])
        self.sections[A.REQUIRED_HEADINGS[-1]]='<!-- TODO -->'
        self.assertTrue(any('placeholder' in e for e in self.errors()))

    def test_config_does_not_implicitly_count_as_result(self):
        exp=self.case/'experiment'; exp.mkdir()
        (exp/'run.py').write_text('print(1)')
        (exp/'config.json').write_text('{"epochs": 100}')
        self.fields.update(experiment_required=True, code_files=['experiment/run.py'])
        self.assertTrue(any('result_files' in e for e in self.errors()))

    def test_external_entry_and_result_without_copy(self):
        (self.root/'train.py').write_text('print(1)')
        (self.root/'results.csv').write_text('metric,value\naccuracy,0.7\n')
        self.fields.update(experiment_required=True, code_files=['../../train.py'], result_files=[str(self.root/'results.csv')])
        self.assertEqual(self.errors(), [])
        self.assertFalse((self.case/'experiment').exists())

    def test_reuse_figure_with_false_flag(self):
        exp=self.case/'experiment';exp.mkdir();(exp/'figure.png').write_bytes(b'fixture')
        self.assertEqual(self.errors(), [])

    def test_result_validation(self):
        p=self.case/'result.json';self.fields['result_files']=['result.json']
        for content in ['', '{}', '[]', '{bad']:
            with self.subTest(content=content):
                p.write_text(content);self.assertTrue(self.errors())
        p.write_text('{"metric": 0}')
        self.assertEqual(self.errors(), [])
        p.unlink();self.assertTrue(self.errors())

    def test_csv_requires_data(self):
        p=self.case/'result.csv';p.write_text('metric,value\n');self.fields['result_files']=['result.csv']
        self.assertTrue(self.errors())
        p.write_text('metric,value\nerror,0\n');self.assertEqual(self.errors(), [])

    def test_explicit_extra_artifacts(self):
        for name in ('notes','qa'):
            (self.case/name).mkdir()
        (self.case/'qa/page-1.png').write_bytes(b'fixture')
        (self.case/'evidence-ledger.json').write_text('{}')
        self.assertTrue(self.errors())
        self.fields['approved_artifacts']={'notes':'User requested notes','qa':'User requested QA pages','evidence-ledger.json':'User requested ledger'}
        self.assertEqual(self.errors(), [])
        self.fields['approved_artifacts']={'.':'blanket exemption'}
        self.assertTrue(any('child path' in e for e in self.errors()))

    def test_word_inside_case_and_unwanted_copy(self):
        self.fields['word_file']='response.docx'
        docx(self.case/'response.docx','after')
        docx(self.case/'response.before-R2-C4.docx')
        docx(self.case/'response.before-R1-C1.docx')
        self.assertEqual(self.errors(), [])
        docx(self.case/'duplicate.docx')
        self.assertTrue(any('Unexpected DOCX' in e for e in self.errors()))

    def test_word_validation_and_missing_backup(self):
        self.word.write_bytes(b'not a DOCX');self.assertTrue(self.errors())
        docx(self.word,'after')
        (self.root/'response.before-R2-C4.docx').unlink();self.assertTrue(self.errors())

    def test_metadata_only_change_is_not_claimed_as_content_verification(self):
        docx(self.word,'before',marker='changed metadata only')
        self.assertEqual(self.errors(), [])
        self.write_plan()
        p=subprocess.run([sys.executable,'-B',str(ROOT/'scripts/audit_review_case.py'),str(self.case)],capture_output=True,text=True)
        self.assertEqual(p.returncode,0)
        self.assertIn('do not prove target edits',p.stdout)

    def test_metadata_is_only_read_from_frontmatter(self):
        self.fields['word_file']=None
        self.sections[A.REQUIRED_HEADINGS[-1]]='word_file: '+json.dumps(str(self.word))
        self.assertTrue(any('word_file is required' in e for e in self.errors()))
        with self.assertRaises(ValueError):A.metadata('---\nword_file: null\nword_file: "x"\n---\n')
        with self.assertRaises(ValueError):A.metadata('---\ncode_files: [broken\n---\n')

    def test_cleanup_then_rerun(self):
        cache=self.case/'__pycache__';cache.mkdir()
        self.assertTrue(self.errors());cache.rmdir();self.assertEqual(self.errors(), [])

    def init_args(self, cid='R1-C1'):
        code=self.root/'code';code.mkdir(exist_ok=True)
        for n in ('paper.tex','paper.pdf','reviews.txt'):(self.root/n).write_text('input fixture')
        return [cid,'--root',str(self.root/'new-cases'),'--paper-tex',str(self.root/'paper.tex'),'--paper-pdf',str(self.root/'paper.pdf'),'--code-root',str(code),'--review-comments',str(self.root/'reviews.txt'),'--comment-text','Please clarify the protocol.']

    def run_init(self, args):
        return subprocess.run([sys.executable,'-B',str(ROOT/'scripts/init_review_case.py'),*args],capture_output=True,text=True)

    def test_first_case_without_previous_directory(self):
        args=self.init_args()+['--previous-cases',str(self.root/'new-cases')]
        p=self.run_init(args);self.assertEqual(p.returncode,0,p.stderr)
        fields=A.metadata((self.root/'new-cases/R1-C1/response-plan.md').read_text())
        self.assertIsNone(fields['previous_cases'])
        self.assertIsNone(fields['code_revision'])

    def test_git_with_no_commit(self):
        args=self.init_args()
        subprocess.run(['git','init','-q',str(self.root/'code')],check=True)
        p=self.run_init(args);self.assertEqual(p.returncode,0,p.stderr)
        self.assertIsNone(A.metadata((self.root/'new-cases/R1-C1/response-plan.md').read_text())['code_revision'])

    def test_git_unavailable_or_timed_out(self):
        for exc in [FileNotFoundError(),subprocess.TimeoutExpired('git',10)]:
            with self.subTest(exc=type(exc).__name__),patch.object(I.subprocess,'run',side_effect=exc):
                self.assertIsNone(I.git_revision(self.root))

    def test_bad_ids_have_no_side_effect(self):
        for cid in ['../outside','/absolute','R1/C1','R1\\C1','..','CON','a'*65]:
            with self.subTest(cid=cid):
                p=self.run_init(self.init_args(cid));self.assertNotEqual(p.returncode,0)
                self.assertFalse((self.root/'new-cases').exists())
        self.assertFalse((self.root/'outside').exists())

    def test_invalid_input_leaves_no_case(self):
        args=self.init_args();args[args.index('--paper-pdf')+1]=str(self.root/'missing.pdf')
        self.assertNotEqual(self.run_init(args).returncode,0)
        self.assertFalse((self.root/'new-cases').exists())

    def test_resume_preserves_bytes_and_rejects_wrong_identity(self):
        args=self.init_args();self.assertEqual(self.run_init(args).returncode,0)
        p=self.root/'new-cases/R1-C1/response-plan.md';p.write_text(p.read_text()+'\nUser notes remain.\n')
        before=p.read_bytes()
        self.assertNotEqual(self.run_init(args).returncode,0)
        resumed=['R1-C1','--root',str(self.root/'new-cases'),'--resume']
        self.assertEqual(self.run_init(resumed).returncode,0)
        self.assertEqual(before,p.read_bytes())
        p.write_text(p.read_text().replace('comment_id: "R1-C1"','comment_id: "R2-C9"'))
        self.assertNotEqual(self.run_init(resumed).returncode,0)


if __name__ == '__main__':
    unittest.main()
