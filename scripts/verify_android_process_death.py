#!/usr/bin/env python3
"""Synthetic only: kill on instrumentation acknowledgment, then verify in a fresh process."""
import argparse
import select
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument('--serial', default='emulator-5554')
args = parser.parse_args()
adb = ['adb', '-s', args.serial]
package = 'pk.vexel.pgrcompanion.debug'
runner = package + '.test/androidx.test.runner.AndroidJUnitRunner'

def command(method):
    return adb + ['shell', 'am', 'instrument', '-w', '-e', 'storageAcceptance', 'synthetic-only', '-e', 'class', 'pk.vexel.pgrcompanion.UploadDurabilityTest#' + method, runner]

def verify(method):
    result = subprocess.run(command(method), capture_output=True, text=True, timeout=60)
    print(result.stdout, flush=True)
    if result.returncode or 'OK (1 test)' not in result.stdout:
        raise RuntimeError('Verification failed: ' + method)

for stage, acknowledgment, check in [
    ('stageAndWaitForHostKill', 'STAGE_ACK', 'verifyAfterHostKill'),
    ('interruptBeforeAcknowledgment', 'PRE_ACK', 'verifyPreAckCleanup'),
    ('uploadAndWaitForHostKill', 'UPLOAD_IN_FLIGHT', 'verifyAfterHostKill'),
]:
    process = subprocess.Popen(command(stage), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    collected = b''
    deadline = time.monotonic() + 60
    while time.monotonic() < deadline:
        ready, _, _ = select.select([process.stdout], [], [], 1)
        if ready:
            chunk = process.stdout.read(4096)
            if not chunk:
                break
            collected += chunk
            if ('storage_gate=' + acknowledgment).encode() in collected:
                started = time.monotonic()
                subprocess.run(adb + ['shell', 'am', 'force-stop', package], check=True, capture_output=True)
                print(f'{acknowledgment}: host force-stop issued immediately; command completed in {time.monotonic()-started:.3f}s', flush=True)
                break
    else:
        process.terminate()
        raise RuntimeError('No stage acknowledgment: ' + stage)
    if ('storage_gate=' + acknowledgment).encode() not in collected:
        process.terminate()
        raise RuntimeError('Stage failed before acknowledgment: ' + collected.decode(errors='replace'))
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.terminate()
    verify(check)
verify('sourceFailureCleansUpAndReconciliationWaitsForStaging')
verify('metadataCommitFailureDoesNotAcknowledgeOrRetainSource')
print('PASS: post-ack death, pre-ack cleanup, in-flight upload recovery, source failure, staging/reconcile race, metadata failure', flush=True)
