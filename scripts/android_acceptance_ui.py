#!/usr/bin/env python3
"""ADB UI helper. Credentials come only from an owner-controlled JSON file via PGR_ACCEPTANCE_CREDENTIALS. Never record raw UI labels containing personal data in evidence."""
import subprocess,xml.etree.ElementTree as ET,re,time,sys,json,os
from pathlib import Path
ADB=['adb','-s','emulator-5554']
PACKAGE='pk.vexel.pgrcompanion.debug'
def adb(*args):
    return subprocess.run(ADB+list(args),capture_output=True,text=True,check=True).stdout

def nodes():
    for _ in range(4):
        try:
            adb('shell','uiautomator','dump','/sdcard/closure-window.xml')
            value=adb('shell','cat','/sdcard/closure-window.xml')
            return [node for node in ET.fromstring(value).iter('node') if node.get('package') == PACKAGE]
        except (subprocess.CalledProcessError,ET.ParseError): time.sleep(.5)
    raise RuntimeError('Could not read UI')

def clicknode(node):
    x1,y1,x2,y2=map(int,re.findall(r'\d+',node.attrib['bounds']))
    adb('shell','input','tap',str((x1+x2)//2),str((y1+y2)//2))

def click(text,contains=False):
    matches=[n for n in nodes() if any((text in n.get(a,'') if contains else text==n.get(a,'')) for a in ('text','content-desc'))]
    if not matches: raise RuntimeError('UI control unavailable: '+text)
    clicknode(matches[-1])

def wait(text,timeout=35):
    end=time.monotonic()+timeout
    while time.monotonic()<end:
        if any(text in n.get('text','') for n in nodes()): return
        time.sleep(.7)
    raise RuntimeError('UI did not reach '+text)

def login(role):
    credentials=json.loads(Path(os.environ['PGR_ACCEPTANCE_CREDENTIALS']).read_text())
    wait('Forgot password?')
    for index,value in enumerate(credentials[role]):
        # IME resizing changes field coordinates. Re-read after each keyboard dismissal.
        fields=[n for n in nodes() if n.get('class')=='android.widget.EditText']
        if len(fields)!=2: raise RuntimeError('Expected the sign-in form, not profile inputs')
        clicknode(fields[index])
        adb('shell','input','keyevent','123')
        adb('shell','input','keyevent',*(['67']*128))
        adb('shell','input','text',value)
        adb('shell','input','keyevent','4')
        time.sleep(.3)
    fields=[n for n in nodes() if n.get('class')=='android.widget.EditText']
    if len(fields)!=2 or fields[0].get('text')!=credentials[role][0]:
        raise RuntimeError('Username input verification failed; credentials were not submitted')
    click('Sign in')

if __name__=='__main__':
    if sys.argv[1]=='login': login(sys.argv[2])
    elif sys.argv[1]=='click': click(sys.argv[2])
    elif sys.argv[1]=='labels':
        print('\n'.join(n.get('text','') for n in nodes() if n.get('text') and n.get('password')!='true'))

def idle(timeout=45):
    end=time.monotonic()+timeout
    while time.monotonic()<end:
        current=nodes()
        if not any(n.get('class')=='android.widget.ProgressBar' for n in current): return
        time.sleep(.7)
    raise RuntimeError('UI remained busy')

def clickscroll(text):
    for _ in range(6):
        try: click(text);return
        except RuntimeError: adb('shell','input','swipe','500','1600','500','500','350')
    raise RuntimeError('Scrollable control unavailable: '+text)
