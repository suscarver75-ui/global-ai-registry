const CONSEQUENTIAL = new Set(['PUBLISH','MONEY','CONTRACT','CREDENTIAL']);
const VALID_ACTIONS = new Set(['READ','WRITE','PUBLISH','DELETE','MONEY','CONTRACT','CREDENTIAL','SECURITY']);

export function decidePolicy(command) {
  if (!command || !VALID_ACTIONS.has(command.action_class)) {
    return { decision: 'DENY', reason: 'Unknown or missing action class.' };
  }
  if (command.action_class === 'DELETE') {
    return { decision: 'DENY', reason: 'Destructive delete is denied by default.' };
  }
  if (CONSEQUENTIAL.has(command.action_class) || ['HIGH','CRITICAL'].includes(command.impact)) {
    return { decision: 'REQUIRE_APPROVAL', reason: 'Consequential or high-impact action.' };
  }
  if (command.action_class === 'READ') {
    return { decision: 'ALLOW', reason: 'Low-risk authenticated read may proceed within connector scope.' };
  }
  return { decision: 'REQUIRE_APPROVAL', reason: 'Write/security actions require explicit approval in v1.' };
}
