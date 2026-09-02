import { execFileSync } from 'node:child_process';
import path from 'node:path';

const REPO_ROOT = path.resolve(__dirname, '../../../../');
const COMPOSE_FILE = path.join(REPO_ROOT, 'docker', 'docker-compose.yml');
const ENV_FILE = path.join(REPO_ROOT, '.env');
const RESET_SUBMISSIONS_SCRIPT = [
  'from sims.training.models import ResidentSubmission, ResidentThesis',
  'from sims.users.models import User',
  "resident = User.objects.get(username='resident_user')",
  'ResidentSubmission.objects.filter(resident_training_record__resident_user=resident).delete()',
  'ResidentThesis.objects.filter(resident_training_record__resident_user=resident).delete()',
  "print('resident_user submission workflow reset complete')",
].join('; ');

export function resetFeatureResidentSubmissionState() {
  execFileSync(
    'docker',
    [
      'compose',
      '--env-file',
      ENV_FILE,
      '-f',
      COMPOSE_FILE,
      'exec',
      '-T',
      'backend',
      'python',
      'manage.py',
      'shell',
      '-c',
      RESET_SUBMISSIONS_SCRIPT,
    ],
    {
    cwd: REPO_ROOT,
    stdio: 'inherit',
    }
  );
}
